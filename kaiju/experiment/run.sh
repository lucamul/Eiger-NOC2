TAG="testscalabilty"
EXPERIMENT="{ "serversList" : [(5,5)],
                    "txnlen" : [4],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ "READ_COMMITTED",
                                  "READ_ATOMIC_STAMP", 
                                  "EIGER",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_BLOOM",
                                  "LWLR",
                                  "LWSR",
                                  "LWNR" ],
                    "readprop" : [0.95],
                    "iterations" : range(0,3),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : "zipfian",
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }"

mkdir -p multiset
python setup_hosts.py --color -c us-west-2 --experiment $EXPERIMENT --tag $TAG --output multitest/$EXPERIMENT
