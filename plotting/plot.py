import argparse
from os import listdir
import os
from sys import argv
import matplotlib.pyplot as plt
from matplotlib import rcParams
from parameters import *

possible_labels = ["threads","read_prop","value_size","txn_size","num_servers","num_key","distribution", "freshness"]

def read_line(x_axises,y_axises,id_var, id_algorthm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line):
    var = line[id_var]
    algorithm = line[id_algorthm]
    average_latency = line[id_average_latency]
    throughput = line[id_throughput]
    read_latency = line[id_read_latency]
    write_latency = line[id_write_latency]
    latency_99th = line[id_99th_latency]
    latency_95th = line[id_95th_latency]
    if var not in x_axises:
        x_axises.append(var)
    if algorithm not in y_axises:
        y_axises[algorithm] = {}
        if "average_latency" not in y_axises[algorithm]:
            y_axises[algorithm]["average_latency"] = []
        if "throughput" not in y_axises[algorithm]:
            y_axises[algorithm]["throughput"] = []
        if "read_latency" not in y_axises[algorithm]:
            y_axises[algorithm]["read_latency"] = []
        if "write_latency" not in y_axises[algorithm]:
            y_axises[algorithm]["write_latency"] = []
        if "latency_99th" not in y_axises[algorithm]:
            y_axises[algorithm]["latency_99th"] = []
        if "latency_95th" not in y_axises[algorithm]:
            y_axises[algorithm]["latency_95th"] = []
    y_axises[algorithm]["average_latency"].append(average_latency)
    y_axises[algorithm]["throughput"].append(throughput)
    y_axises[algorithm]["read_latency"].append(read_latency)
    y_axises[algorithm]["write_latency"].append(write_latency)
    y_axises[algorithm]["latency_99th"].append(latency_99th)
    y_axises[algorithm]["latency_95th"].append(latency_95th)
    return x_axises,y_axises

def get_separate_y_axis(y_axises):
    y_axis_average_latency = {}
    y_axis_throughput = {}
    y_axis_read_latency = {}
    y_axis_write_latency = {}
    y_axis_99th_latency = {}
    y_axis_95th_latency = {}
    for algorithm in y_axises:
        y_axis_average_latency[algorithm] = y_axises[algorithm]["average_latency"]
        y_axis_throughput[algorithm] = y_axises[algorithm]["throughput"]
        y_axis_read_latency[algorithm] = y_axises[algorithm]["read_latency"]
        y_axis_write_latency[algorithm] = y_axises[algorithm]["write_latency"]
        y_axis_99th_latency[algorithm] = y_axises[algorithm]["latency_99th"]
        y_axis_95th_latency[algorithm] = y_axises[algorithm]["latency_95th"]
    return y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency

def convert_str_to_int(x_axis, y_axises):
    # check if x_axis is a dict
    if isinstance(x_axis, dict):
        for algorithm in x_axis:
            x_axis[algorithm] = [float(x) for x in x_axis[algorithm]]
        if all(all(x.is_integer() for x in x_axis[algorithm]) for algorithm in x_axis):
            for algorithm in x_axis:
                x_axis[algorithm] = [int(x) for x in x_axis[algorithm]]
        for algorithm in y_axises:
            y_axises[algorithm] = [float(y) for y in y_axises[algorithm]]
        if all(all(y.is_integer() for y in y_axises[algorithm]) for algorithm in y_axises):
            for algorithm in y_axises:
                y_axises[algorithm] = [int(y) for y in y_axises[algorithm]]
        return x_axis, y_axises
    
    x_axis = [float(x) for x in x_axis]
    for algorithm in y_axises:
        y_axises[algorithm] = [float(y) for y in y_axises[algorithm]]
    # if the floats have no decimals then convert them to int
    if all(x.is_integer() for x in x_axis):
        x_axis = [int(x) for x in x_axis]
    if all(all(y.is_integer() for y in y_axises[algorithm]) for algorithm in y_axises):
        for algorithm in y_axises:
            y_axises[algorithm] = [int(y) for y in y_axises[algorithm]]
    return x_axis, y_axises

def generate_plot(x_axis, y_axises, title, x_label, y_label, directory, barPlot = False):
    if barPlot:
        _, y_axises = convert_str_to_int([], y_axises)
        fig, ax = plt.subplots()

        x_positions = np.arange(len(x_axis))  # create an array of x positions for each set of bars

        for i, algorithm in enumerate(y_axises):
            offset = i * bar_width
            ax.bar(x=x_positions + offset, height=y_axises[algorithm], width=bar_width, label=names[algorithm], color=colors[algorithm])
        
        mid_pos = (len(y_axises) - 1) / 2.0

        # Set the tick position to the middle position of the middle bar
        ax.set_xticks(x_positions + (mid_pos * bar_width))

        ax.set_title(title, **title_info)
        ax.set_xlabel(x_label, fontsize=axis_font)
        ax.set_ylabel(y_label, fontsize=axis_font)
        ax.tick_params(axis='both', which='major', labelsize=tick_font)
        ax.set_xticklabels(x_axis, fontsize=tick_font)
        ax.legend()
        plt.grid(haveGrid)
        title_no_spaces = title.replace(" ", "_")
        filename = os.path.basename(directory)

        dir_name = filename.replace(".csv", "")

        new_dir_path = os.path.join(saveTo, dir_name)

        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
        
        dir_name += "/"
        plt.savefig(saveTo + dir_name + title_no_spaces + ".pdf")
        if showPlot:
            plt.show()
        return
    x_axis, y_axises = convert_str_to_int(x_axis, y_axises)
    fig, ax = plt.subplots()
    for algorithm in y_axises:
        # if x_axis is a dict
        if isinstance(x_axis, dict):
            ax.plot(x_axis[algorithm], y_axises[algorithm], label=names[algorithm], color=colors[algorithm], marker=markers[algorithm], markersize=marker_size, linewidth=line_width)
        else:
            ax.plot(x_axis, y_axises[algorithm], label=names[algorithm], color=colors[algorithm], marker=markers[algorithm], markersize=marker_size, linewidth=line_width)
    ax.set_title(title, **title_info)
    ax.set_xlabel(x_label, fontsize=axis_font)
    ax.set_ylabel(y_label, fontsize=axis_font)
    ax.tick_params(axis='both', which='major', labelsize=tick_font)
    ax.legend()
    plt.grid(haveGrid)
    title_no_spaces = title.replace(" ","_")
    filename = os.path.basename(directory)

    dir_name = filename.replace(".csv", "")

    new_dir_path = os.path.join(saveTo, dir_name)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    
    dir_name += "/"
    
    plt.savefig(saveTo+dir_name+title_no_spaces+".pdf")
    
    if showPlot:
        plt.show()
    return

def plot_freshness(directory):
    with open(directory,"r") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        x_axis = staleness_string
        id_algorithm = header.split(",").index("algorithm")
        ids = []
        for i in range(len(x_axis)):
            ids.append(header.split(",").index(x_axis[i]))
        y_axises = {}
        for line in lines[1:]:
            line = line.split(",")
            algorithm = line[id_algorithm]
            y_axis = []
            for i in ids:
                y_axis.append(line[i])
            y_axises[algorithm] = y_axis
        generate_plot(x_axis, y_axises, "Data Staleness" ,"Staleness (ms)", "Read Staleness CDF")

def plot_threads(directory):
    with open(directory,"r") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        id_threads = header.split(",").index("threads")
        id_algorithm = header.split(",").index("algorithm")
        id_average_latency = header.split(",").index("average_latency")
        id_throughput = header.split(",").index("throughput")
        id_read_latency = header.split(",").index("read_latency")
        id_write_latency = header.split(",").index("write_latency")
        id_99th_latency = header.split(",").index("99th_latency")
        id_95th_latency = header.split(",").index("95th_latency")
        y_axises = {}
        x_axises = []
        for line in lines[1:]:
            line = line.split(",")
            x_axises, y_axises = read_line(x_axises,y_axises,id_threads, id_algorithm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line)
        y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency = get_separate_y_axis(y_axises)
        generate_plot(x_axises, y_axis_average_latency, "Number of Clients vs. Average Latency", "Number of Client Threads", "Average Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_throughput, "Number of Clients vs. Throughput", "Number of Client Threads", "Throughput (ops/s)",directory,True)
        generate_plot(x_axises, y_axis_read_latency, "Number of Clients vs. Read Latency", "Number of Client Threads", "Read Latency (ms)", directory,True)
        generate_plot(x_axises, y_axis_write_latency, "Number of Clients vs. Write Latency", "Number of Client Threads", "Write Latency (ms)", directory,True)
        generate_plot(x_axises, y_axis_99th_latency, "Number of Clients vs. 99th Latency", "Number of Client Threads", "99th Latency (ms)", directory,True)
        generate_plot(x_axises, y_axis_95th_latency, "Number of Clients vs. 95th Latency", "Number of Client Threads", "95th Latency (ms)", directory,True)
        generate_plot(y_axis_throughput, y_axis_average_latency, "Throughput vs. Average Latency", "Throughput (ops/s)", "Average Latency (ms)", directory)
        generate_plot(y_axis_throughput, y_axis_read_latency, "Throughput vs. Read Latency", "Throughput (ops/s)", "Read Latency (ms)",directory)
        generate_plot(y_axis_throughput, y_axis_write_latency, "Throughput vs. Write Latency", "Throughput (ops/s)", "Write Latency (ms)",directory)
    return

def plot_read_prop(directory):
    with open(directory,"r") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        id_read_prop = header.split(",").index("read_prop")
        id_algorithm = header.split(",").index("algorithm")
        id_average_latency = header.split(",").index("average_latency")
        id_throughput = header.split(",").index("throughput")
        id_read_latency = header.split(",").index("read_latency")
        id_write_latency = header.split(",").index("write_latency")
        id_99th_latency = header.split(",").index("99th_latency")
        id_95th_latency = header.split(",").index("95th_latency")
        y_axises = {}
        x_axises = []
        for line in lines[1:]:
            line = line.split(",")
            x_axises, y_axises = read_line(x_axises,y_axises,id_read_prop, id_algorithm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line)
        y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency = get_separate_y_axis(y_axises)
        generate_plot(x_axises, y_axis_average_latency, "Read Proportion vs. Average Latency", "Read Proportion", "Average Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_throughput, "Read Proportion vs. Throughput", "Read Proportion", "Throughput (ops/s)",directory,True)
        generate_plot(x_axises, y_axis_read_latency, "Read Proportion vs. Read Latency", "Read Proportion", "Read Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_write_latency, "Read Proportion vs. Write Latency", "Read Proportion", "Write Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_99th_latency, "Read Proportion vs. 99th Latency", "Read Proportion", "99th Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_95th_latency, "Read Proportion vs. 95th Latency", "Read Proportion", "95th Latency (ms)",directory,True)
    return

def plot_value_size(directory):
    with open(directory,"r") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        id_value_size = header.split(",").index("value_size")
        id_algorithm = header.split(",").index("algorithm")
        id_average_latency = header.split(",").index("average_latency")
        id_throughput = header.split(",").index("throughput")
        id_read_latency = header.split(",").index("read_latency")
        id_write_latency = header.split(",").index("write_latency")
        id_99th_latency = header.split(",").index("99th_latency")
        id_95th_latency = header.split(",").index("95th_latency")
        y_axises = {}
        x_axises = []
        for line in lines[1:]:
            line = line.split(",")
            x_axises, y_axises = read_line(x_axises,y_axises,id_value_size, id_algorithm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line)
        y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency = get_separate_y_axis(y_axises)
        generate_plot(x_axises, y_axis_average_latency, "Value Size vs. Average Latency", "Value Size", "Average Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_throughput, "Value Size vs. Throughput", "Value Size", "Throughput (ops/s)",directory,True)
        generate_plot(x_axises, y_axis_read_latency, "Value Size vs. Read Latency", "Value Size", "Read Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_write_latency, "Value Size vs. Write Latency", "Value Size", "Write Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_99th_latency, "Value Size vs. 99th Latency", "Value Size", "99th Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_95th_latency, "Value Size vs. 95th Latency", "Value Size", "95th Latency (ms)",directory,True)
    return
def plot_txn_size(directory):
    with open(directory,"r") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        id_txn_size = header.split(",").index("txn_size")
        id_algorithm = header.split(",").index("algorithm")
        id_average_latency = header.split(",").index("average_latency")
        id_throughput = header.split(",").index("throughput")
        id_read_latency = header.split(",").index("read_latency")
        id_write_latency = header.split(",").index("write_latency")
        id_99th_latency = header.split(",").index("99th_latency")
        id_95th_latency = header.split(",").index("95th_latency")
        y_axises = {}
        x_axises = []
        for line in lines[1:]:
            line = line.split(",")
            x_axises, y_axises = read_line(x_axises,y_axises,id_txn_size, id_algorithm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line)
        y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency = get_separate_y_axis(y_axises)
        generate_plot(x_axises, y_axis_average_latency, "Transaction Size vs. Average Latency", "Transaction Size", "Average Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_throughput, "Transaction Size vs. Throughput", "Transaction Size", "Throughput (ops/s)",directory,True)
        generate_plot(x_axises, y_axis_read_latency, "Transaction Size vs. Read Latency", "Transaction Size", "Read Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_write_latency, "Transaction Size vs. Write Latency", "Transaction Size", "Write Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_99th_latency, "Transaction Size vs. 99th Latency", "Transaction Size", "99th Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_95th_latency, "Transaction Size vs. 95th Latency", "Transaction Size", "95th Latency (ms)",directory,True)
    return
def plot_num_servers(directory):
    with open(directory,"r") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        id_num_servers = header.split(",").index("num_servers")
        id_algorithm = header.split(",").index("algorithm")
        id_average_latency = header.split(",").index("average_latency")
        id_throughput = header.split(",").index("throughput")
        id_read_latency = header.split(",").index("read_latency")
        id_write_latency = header.split(",").index("write_latency")
        id_99th_latency = header.split(",").index("99th_latency")
        id_95th_latency = header.split(",").index("95th_latency")
        y_axises = {}
        x_axises = []
        for line in lines[1:]:
            line = line.split(",")
            x_axises, y_axises = read_line(x_axises,y_axises,id_num_servers, id_algorithm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line)
        y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency = get_separate_y_axis(y_axises)
        generate_plot(x_axises, y_axis_average_latency, "Number of Servers vs. Average Latency", "Number of Servers", "Average Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_throughput, "Number of Servers vs. Throughput", "Number of Servers", "Throughput (ops/s)",directory,True)
        generate_plot(x_axises, y_axis_read_latency, "Number of Servers vs. Read Latency", "Number of Servers", "Read Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_write_latency, "Number of Servers vs. Write Latency", "Number of Servers", "Write Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_99th_latency, "Number of Servers vs. 99th Latency", "Number of Servers", "99th Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_95th_latency, "Number of Servers vs. 95th Latency", "Number of Servers", "95th Latency (ms)",directory,True)
    return

def plot_num_key(directory):
    with open(directory,"r") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        id_num_key = header.split(",").index("num_key")
        id_algorithm = header.split(",").index("algorithm")
        id_average_latency = header.split(",").index("average_latency")
        id_throughput = header.split(",").index("throughput")
        id_read_latency = header.split(",").index("read_latency")
        id_write_latency = header.split(",").index("write_latency")
        id_99th_latency = header.split(",").index("99th_latency")
        id_95th_latency = header.split(",").index("95th_latency")
        y_axises = {}
        x_axises = []
        for line in lines[1:]:
            line = line.split(",")
            x_axises, y_axises = read_line(x_axises,y_axises,id_num_key, id_algorithm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line)
        y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency = get_separate_y_axis(y_axises)
        generate_plot(x_axises, y_axis_average_latency, "Number of Keys vs. Average Latency", "Number of Keys", "Average Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_throughput, "Number of Keys vs. Throughput", "Number of Keys", "Throughput (ops/s)",directory,True)
        generate_plot(x_axises, y_axis_read_latency, "Number of Keys vs. Read Latency", "Number of Keys", "Read Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_write_latency, "Number of Keys vs. Write Latency", "Number of Keys", "Write Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_99th_latency, "Number of Keys vs. 99th Latency", "Number of Keys", "99th Latency (ms)",directory,True)
        generate_plot(x_axises, y_axis_95th_latency, "Number of Keys vs. 95th Latency", "Number of Keys", "95th Latency (ms)",directory,True)
    return
def plot_distribution(directory):
    with open(directory,"f") as f:
        lines = f.readlines()
        header = lines[0].rstrip("\n")
        id_distribution = header.split(",").index("distribution")
        id_algorithm = header.split(",").index("algorithm")
        id_average_latency = header.split(",").index("average_latency")
        id_throughput = header.split(",").index("throughput")
        id_read_latency = header.split(",").index("read_latency")
        id_write_latency = header.split(",").index("write_latency")
        id_99th_latency = header.split(",").index("99th_latency")
        id_95th_latency = header.split(",").index("95th_latency")
        y_axises = {}
        x_axises = []
        for line in lines[1:]:
            line = line.split(",")
            x_axises, y_axises = read_line(x_axises,y_axises,id_distribution, id_algorithm, id_average_latency, id_throughput,id_read_latency,id_write_latency,id_99th_latency,id_95th_latency,line)
        y_axis_average_latency,y_axis_throughput,y_axis_read_latency,y_axis_write_latency,y_axis_99th_latency,y_axis_95th_latency = get_separate_y_axis(y_axises)
        generate_plot(x_axises, y_axis_average_latency, "Distribution vs. Average Latency", "Distribution", "Average Latency (ms)",directory,barPlot=True)
        generate_plot(x_axises, y_axis_throughput, "Distribution vs. Throughput", "Distribution", "Throughput (ops/s)",directory,barPlot=True)
        generate_plot(x_axises, y_axis_read_latency, "Distribution vs. Read Latency", "Distribution", "Read Latency (ms)",directory, barPlot=True)
        generate_plot(x_axises, y_axis_write_latency, "Distribution vs. Write Latency", "Distribution", "Write Latency (ms)",directory,barPlot=True)
        generate_plot(x_axises, y_axis_99th_latency, "Distribution vs. 99th Latency", "Distribution", "99th Latency (ms)",directory,barPlot=True)
        generate_plot(x_axises, y_axis_95th_latency, "Distribution vs. 95th Latency", "Distribution", "95th Latency (ms)",directory,barPlot=True)
    return

def plot(ylabel, directory):
    if ylabel == "threads":
        plot_threads(directory)
    elif ylabel == "read_prop":
        plot_read_prop(directory)
    elif ylabel == "value_size":
        plot_value_size(directory)
    elif ylabel == "txn_size":
        plot_txn_size(directory)
    elif ylabel == "num_servers":
        plot_num_servers(directory)
    elif ylabel == "num_key":
        plot_num_key(directory)
    elif ylabel == "distribution":
        plot_distribution(directory)
    elif ylabel == "freshness":
        plot_freshness(directory)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, help="Directory to plot from")
    parser.add_argument("--experiment", type=str, help="Type of experiment, i.e. parameter we are varying, possible values are: " + str(possible_labels))
    args = parser.parse_args()
    directory = args.dir
    ylabel = args.experiment
    if ylabel not in possible_labels:
        print("Invalid experiment")
        print("Possible experiments are: ", possible_labels)
        exit(1)
    plot(ylabel, directory)