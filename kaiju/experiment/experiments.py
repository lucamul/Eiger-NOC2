default = {
    "serversList" : [(8,8)],
                    "txnlen" : [5],
                    "threads" : [32],
                    "numseconds" : 60,
                    "configs" : [
                                  "EIGER",
                                  "EIGER_PORT",
                                  "EIGER_PORT_PLUS",
                                  "EIGER_PORT_PLUS_PLUS"
                                ],
                    "readprop" : [.9],
                    "iterations" : range(0,1),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}

num_clients = {
    "serversList" : [(8,8)],
                    "txnlen" : [5],
                    "threads" : [2,4,8,16,32,64,128,256,512],
                    "numseconds" : 60,
                    "configs" : [
                                  "EIGER",
                                  "EIGER_PORT",
                                  "EIGER_PORT_PLUS",
                                  "EIGER_PORT_PLUS_PLUS"
                                ],
                    "readprop" : [.9],
                    "iterations" : range(0,1),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}


num_servers = {
    "serversList" : [(2,2),(4,4),(8,8),(16,16),(32,32)],
                    "txnlen" : [5],
                    "threads" : [32],
                    "numseconds" : 60,
                    "configs" : [
                                  "EIGER",
                                  "EIGER_PORT",
                                  "EIGER_PORT_PLUS",
                                  "EIGER_PORT_PLUS_PLUS"
                                ],
                    "readprop" : [.9],
                    "iterations" : range(0,1),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}


experiments = { 
                "default" : default,
                "num_clients" : num_clients,
                "num_servers" : num_servers,               
}