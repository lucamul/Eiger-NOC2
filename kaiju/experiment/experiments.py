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
                    "iterations" : range(0,5),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [128],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}

read_prop = {
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
                    "readprop" : [0,0.3,0.5,0.7,.9,1],
                    "iterations" : range(0,5),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [128],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}

value_size = {
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
                    "iterations" : range(0,5),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [1,10,100,1000,10000],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}

txn_len = {
    "serversList" : [(8,8)],
                    "txnlen" : [1,2,4,8,16,32,64,128],
                    "threads" : [32],
                    "numseconds" : 60,
                    "configs" : [
                                  "EIGER",
                                  "EIGER_PORT",
                                  "EIGER_PORT_PLUS",
                                  "EIGER_PORT_PLUS_PLUS"
                                ],
                    "readprop" : [.9],
                    "iterations" : range(0,5),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [128],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}

freshness = {
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
                    "iterations" : range(0,5),
                    "freshness" : 1,
                    "numkeys" : [1000000],
                    "valuesize" : [128],
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
                    "iterations" : range(0,5),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [128],
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
                    "iterations" : range(0,5),
                    "freshness" : 0,
                    "numkeys" : [1000000],
                    "valuesize" : [128],
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
                "freshness" : freshness,     
                "txn_len" : txn_len,
                "value_size" : value_size,
                "read_prop" : read_prop,          
}