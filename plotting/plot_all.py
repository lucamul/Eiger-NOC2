import os

dirs = {
    "freshness" : "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/results/freshness-2023-04-05-09-32-39.csv",
    "threads" : "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/results/num_clients-2023-04-05-16-40-00.csv",
    "num_servers" : "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/results/num_servers-2023-04-05-20-52-39.csv",
    "read_prop" : "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/results/read_prop-2023-04-06-02-19-04.csv",
    "txn_size" : "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/results/txn_len-2023-04-06-10-21-03.csv",
    "value_size" : "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/results/value_size-2023-04-06-16-00-08.csv"
}

def plot_all():
    for name, path in dirs.items():
        os.system("python3 plot.py --dir " + path + " --experiment " + name)


if __name__ == "__main__":
    plot_all()