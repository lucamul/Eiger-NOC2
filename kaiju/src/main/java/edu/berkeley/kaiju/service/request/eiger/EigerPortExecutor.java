package edu.berkeley.kaiju.service.request.eiger;

import java.io.IOException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.NavigableMap;
import java.util.Vector;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.collect.Maps;
import com.google.common.collect.Queues;
import com.google.common.collect.Sets;
import com.yammer.metrics.Histogram;
import com.yammer.metrics.MetricRegistry;
import com.yammer.metrics.Timer;

import edu.berkeley.kaiju.config.Config;
import edu.berkeley.kaiju.data.DataItem;
import edu.berkeley.kaiju.exception.ClientException;
import edu.berkeley.kaiju.exception.KaijuException;
import edu.berkeley.kaiju.monitor.MetricsManager;
import edu.berkeley.kaiju.net.routing.OutboundRouter;
import edu.berkeley.kaiju.service.MemoryStorageEngine;
import edu.berkeley.kaiju.service.request.RequestDispatcher;
import edu.berkeley.kaiju.service.request.message.KaijuMessage;
import edu.berkeley.kaiju.service.request.message.request.EigerCheckCommitRequest;
import edu.berkeley.kaiju.service.request.message.request.EigerCommitRequest;
import edu.berkeley.kaiju.service.request.message.request.EigerGetAllRequest;
import edu.berkeley.kaiju.service.request.message.request.EigerPutAllRequest;
import edu.berkeley.kaiju.service.request.message.response.EigerPreparedResponse;
import edu.berkeley.kaiju.service.request.message.response.KaijuResponse;
import edu.berkeley.kaiju.util.Timestamp;

public class EigerPortExecutor implements IEigerExecutor{
    private static Logger logger = LoggerFactory.getLogger(EigerExecutor.class);

    private RequestDispatcher dispatcher;
    private MemoryStorageEngine storageEngine;

    private ConcurrentMap<Long, EigerPendingTransaction> pendingTransactionsCoordinated = Maps.newConcurrentMap();
    private ConcurrentMap<Long, EigerPutAllRequest> pendingTransactionsNonCoordinated = Maps.newConcurrentMap();

    ReentrantLock pendingTransactionsLock = new ReentrantLock();
    private ConcurrentMap<String, Collection<Long>> pendingTransactionsPerKey = Maps.newConcurrentMap();
    private ConcurrentSkipListSet<Long> pending = new ConcurrentSkipListSet<Long>();
    private ConcurrentMap<Long,Long> tidToPendingTime = Maps.newConcurrentMap();
    // a roughly time-ordered queue of KVPs to GC; exact real-time ordering not necessary for correctness
    private BlockingQueue<CommittedGarbage> candidatesForGarbageCollection = Queues.newLinkedBlockingQueue();

    private static Histogram commitChecksNumKeys = MetricsManager.getRegistry().histogram(MetricRegistry.name(EigerExecutor.class,
                                                                                               "commit-check-num-keys",
                                                                                               "count"));

    private static Histogram commitCheckNumServers = MetricsManager.getRegistry().histogram(MetricRegistry.name(EigerExecutor.class,
                                                                                                 "commit-check-servers",
                                                                                                 "count"));

    private static Timer commitCheckReadTimer = MetricsManager.getRegistry().timer(MetricRegistry.name(EigerExecutor.class,
                                                                                        "commit-check-read-timer",
                                                                                        "latency"));
    Long lst = Timestamp.NO_TIMESTAMP;
    Long latest_commit = Timestamp.NO_TIMESTAMP;
    public EigerPortExecutor(RequestDispatcher dispatcher,
                         MemoryStorageEngine storageEngine) {
        this.dispatcher = dispatcher;
        this.storageEngine = storageEngine;

        new Thread(new Runnable() {
                    @Override
                    public void run() {
                        long currentTime = -1;
                        CommittedGarbage nextStamp = null;
                        while(true) {
                            try {
                                if(nextStamp == null)
                                    nextStamp = candidatesForGarbageCollection.take();
                                if(nextStamp.getExpirationTime() < currentTime ||
                                   (nextStamp.getExpirationTime() < (currentTime = System.currentTimeMillis())) ) {
                                    pendingTransactionsCoordinated.remove(nextStamp.getTimestamp());
                                    nextStamp = null;
                                } else {
                                    Thread.sleep(nextStamp.getExpirationTime()-currentTime);
                                }
                            } catch (InterruptedException e) {}
                        }
                    }
                }, "Eiger-GC-Thread").start();
    }
    
    @Override
    public void processMessage(EigerPutAllRequest putAllRequest)
            throws KaijuException, IOException, InterruptedException {

        if(putAllRequest.is_get) getAll(putAllRequest);
        else putAll(putAllRequest);
    }

    public void putAll(EigerPutAllRequest putAllRequest)throws KaijuException, IOException, InterruptedException{
        long transactionID = putAllRequest.keyValuePairs.values().iterator().next().getTimestamp();
        if(OutboundRouter.ownsResource(putAllRequest.coordinatorKey.hashCode())) {
            if(!pendingTransactionsCoordinated.containsKey(transactionID)) {
                pendingTransactionsCoordinated.putIfAbsent(transactionID, new EigerPendingTransaction());
            }

            pendingTransactionsCoordinated.get(transactionID).setCoordinatorState(putAllRequest.totalNumKeys,
                                                                                  putAllRequest.senderID,
                                                                                  putAllRequest.requestID);
        }

        assert(!pendingTransactionsNonCoordinated.containsKey(transactionID));
        pendingTransactionsNonCoordinated.put(transactionID, putAllRequest);
        Long pending_t = Timestamp.assignNewTimestamp();
        pending.add(pending_t);
        tidToPendingTime.putIfAbsent(transactionID, pending_t);
        dispatcher.requestOneWay(putAllRequest.coordinatorKey.hashCode(), new EigerPreparedResponse(transactionID,
                                                                                                    putAllRequest
                                                                                                            .keyValuePairs
                                                                                                            .size(),
                                                                                                    pending_t));
    }

    public void getAll(EigerPutAllRequest getAllRequest)throws KaijuException, IOException, InterruptedException{
        Map<String,DataItem> result = new HashMap<String,DataItem>();
        for(Map.Entry<String,DataItem> entry : getAllRequest.keyValuePairs.entrySet()){
            Long version = storageEngine.getHighestCommittedNotGreaterThan(entry.getKey(),entry.getValue().getTimestamp());
            Long latestByClient = storageEngine.getHighestCommittedPerCid(entry.getKey(), entry.getValue().getCid(), version);
            if(latestByClient != Timestamp.NO_TIMESTAMP){
                result.put(entry.getKey(), storageEngine.getByTimestamp(entry.getKey(), latestByClient));
                continue;
            }
            

            DataItem ver = storageEngine.getByTimestamp(entry.getKey(), version);
            if(version == Timestamp.NO_TIMESTAMP || ver.getTimestamp() == Timestamp.NO_TIMESTAMP){
                 result.put(entry.getKey(), DataItem.getNullItem());
                 continue;
            }
            if(!ver.getCid().equals(entry.getValue().getCid())){
                result.put(entry.getKey(), ver);
                continue;
            }

            result.put(entry.getKey(), find_isolated(ver,entry.getKey()));
        }

        KaijuResponse response = new KaijuResponse(result);
        response.setHct(this.lst);
        dispatcher.sendResponse(getAllRequest.senderID, getAllRequest.requestID, response);

    }

    private DataItem find_isolated(DataItem ver, String key) {
        Long gst = ver.getPrepTs();
        Long commit_t = ver.getTimestamp();
        if(gst >= commit_t) return ver;
        if(!storageEngine.eigerMap.containsKey(key)) return ver;
        NavigableMap<Long,DataItem> subMap = storageEngine.eigerMap.get(key).subMap(gst, commit_t).descendingMap();
        Iterator<NavigableMap.Entry<Long, DataItem> > itr = subMap.entrySet().iterator();
        while(itr.hasNext()){
            NavigableMap.Entry<Long, DataItem> entry = itr.next();
            while(entry.getValue().getCid() == ver.getCid()) {
                ver = entry.getValue();
                Long new_gst = ver.getPrepTs();
                Long new_commit_t = ver.getTimestamp();
                if(new_gst >= commit_t) return ver;
                if(!storageEngine.eigerMap.containsKey(key)) return ver;
                subMap = storageEngine.eigerMap.get(key).subMap(new_gst, new_commit_t).descendingMap();
                itr = subMap.entrySet().iterator();
                if(!itr.hasNext()) {
                    return ver;
                }
                entry = itr.next();
            }
            return entry.getValue();
        }
        return ver;
    }    

    @Override
    public void processMessage(EigerPreparedResponse preparedNotification)
            throws KaijuException, IOException, InterruptedException {
                if(!pendingTransactionsCoordinated.containsKey(preparedNotification.transactionID)) {
                    EigerPendingTransaction newTxn =new EigerPendingTransaction();
                    pendingTransactionsCoordinated.putIfAbsent(preparedNotification.transactionID, newTxn);
                }
        
                EigerPendingTransaction ept = pendingTransactionsCoordinated.get(preparedNotification.transactionID);
        
                ept.recordPreparedKeys(preparedNotification.senderID, preparedNotification.numKeys, preparedNotification.preparedTime);
        
                if(ept.shouldCommit()) {
                    commitEigerPendingTransaction(preparedNotification.transactionID, ept);
                }
        
    }

    private void commitEigerPendingTransaction(long transactionID, EigerPendingTransaction ept) throws IOException, InterruptedException{
        Map<Integer, KaijuMessage> toSend = Maps.newHashMap();
        for(int serverToNotify : ept.getServersToNotifyCommit()) {
            toSend.put(serverToNotify, new EigerCommitRequest(transactionID, ept.getCommitTime()));
        }
        Long commitTime = ept.getCommitTime();
        dispatcher.multiRequestOneWay(toSend);
        if(tidToPendingTime.containsKey(transactionID) && pending.contains(tidToPendingTime.get(transactionID))){
            pending.remove(tidToPendingTime.get(transactionID));
            tidToPendingTime.remove(transactionID);
        }
        if(commitTime > this.latest_commit) this.latest_commit = commitTime;
        Long tmp = this.pending.pollFirst();
        if(tmp == null) this.lst = this.latest_commit;
        else this.lst = tmp;

        KaijuResponse response = new KaijuResponse();
        response.setHct(this.lst);
        dispatcher.sendResponse(ept.getClientID(), ept.getClientRequestID(), response);
        candidatesForGarbageCollection.add(new CommittedGarbage(transactionID, System.currentTimeMillis()+Config.getConfig().overwrite_gc_ms));
    }
    
    @Override
    public void processMessage(EigerCommitRequest commitNotification)
            throws KaijuException, IOException, InterruptedException {
        nonCoordinatorMarkCommitted(commitNotification.transactionID, commitNotification.commitTime);
        
    }

    private void nonCoordinatorMarkCommitted(long transactionID, Long commitTime) throws KaijuException, IOException {
        EigerPutAllRequest preparedRequest = pendingTransactionsNonCoordinated.get(transactionID);

        if(preparedRequest == null) {
            return;
        }

        Map<String, DataItem> toCommit = Maps.newHashMap();

        for(String key : preparedRequest.keyValuePairs.keySet()) {
            DataItem item = preparedRequest.keyValuePairs.get(key);
            DataItem new_item =  new DataItem(commitTime, item.getValue());
            new_item.setCid(item.getCid());
            new_item.setPrepTs(item.getPrepTs());
            toCommit.put(key,new_item);

            //logger.info(String.format("%d: COMMITTING %s [%s] at time %d\n", Config.getConfig().server_id, key, Arrays.toString(item.getValue().array()), commitNotification.commitTime));
        }

        storageEngine.putAll(toCommit);
        if(!OutboundRouter.ownsResource(preparedRequest.coordinatorKey.hashCode())){
            if(tidToPendingTime.containsKey(transactionID) && pending.contains(tidToPendingTime.get(transactionID))){
                pending.remove(tidToPendingTime.get(transactionID));
                tidToPendingTime.remove(transactionID);
            }
            if(commitTime > this.latest_commit) this.latest_commit = commitTime;
            Long tmp = this.pending.pollFirst();
            if(tmp == null) this.lst = this.latest_commit;
            else this.lst = tmp;
        }
    }

    @Override
    public void processMessage(EigerGetAllRequest getAllRequest)
            throws KaijuException, IOException, InterruptedException {
        throw new ClientException("This method should not be reached in Eiger-PORT");
    }

    @Override
    public void processMessage(EigerCheckCommitRequest checkCommitRequest)
            throws KaijuException, IOException, InterruptedException {
        throw new ClientException("This method should not be reached in Eiger-PORT");
    }

    class EigerPendingTransaction {
        private AtomicInteger numKeysSeen;
        private int numKeysWaiting;
        private Vector<Integer> serversToNotifyCommit = new Vector<Integer>();
        private int clientID = -1;
        private int clientRequestID = -1;
        AtomicBoolean readyToCommit = new AtomicBoolean(false);
        AtomicBoolean committed = new AtomicBoolean(false);

        private long highestPreparedTime = -1;

        ReentrantLock commitTimeLock = new ReentrantLock();

        public EigerPendingTransaction() {
            this.numKeysSeen = new AtomicInteger(0);
        }

        public void setCoordinatorState(int numKeysWaiting, int clientID, int clientRequestID) {
            this.numKeysWaiting = numKeysWaiting;
            this.clientID = clientID;
            this.clientRequestID = clientRequestID;
        }

        public synchronized boolean shouldCommit() {
            boolean ret = readyToCommit.getAndSet(false);
            if(ret)
                committed.set(true);
            return ret;
        }

        public synchronized boolean hasCommitted() {
            commitTimeLock.lock();
            if(!committed.get())
                highestPreparedTime = Timestamp.assignNewTimestamp(highestPreparedTime);
            commitTimeLock.unlock();

            return committed.get();
        }

        public long getCommitTime() {
            return highestPreparedTime;
        }

        public Collection<Integer> getServersToNotifyCommit() {
            return serversToNotifyCommit;
        }

        public int getClientID() {
            assert (clientID != -1);
            return clientID;
        }

        public int getClientRequestID() {
            assert (clientRequestID != -1);
            return clientRequestID;
        }

        public synchronized void recordPreparedKeys(int server, int numKeys, long preparedTime) {
            if(highestPreparedTime < preparedTime)
                highestPreparedTime = Timestamp.assignNewTimestamp(preparedTime);
            serversToNotifyCommit.add(server);
            numKeysSeen.getAndAdd(numKeys);

            if(numKeysSeen.get() == numKeysWaiting)
                readyToCommit.set(true);
        }

    }

    private class CommittedGarbage {
           private long timestamp;
           private long expirationTime = -1;

           public CommittedGarbage(long timestamp, long expirationTime) {
               this.timestamp = timestamp;
               this.expirationTime = expirationTime;
           }

           public long getExpirationTime(){
               return expirationTime;
           }

           private long getTimestamp() {
               return timestamp;
           }

           @Override
           public int hashCode() {
               return Long.valueOf(timestamp).hashCode();
           }

           @Override
           public boolean equals(Object obj) {
               if (obj == null)
                    return false;
                if (obj == this)
                    return true;
                if (!(obj instanceof CommittedGarbage))
                    return false;

                CommittedGarbage rhs = (CommittedGarbage) obj;
                return rhs.getTimestamp() == timestamp ;
           }
       }
}
