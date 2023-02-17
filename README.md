This repo contains the prototype from the EIGER-PORT++ project. It takes as base the repository from the SIGMOD 2014 paper titled [Scalable Atomic Visibility with RAMP Transactions](http://www.bailis.org/papers/ramp-sigmod2014.pdf) and enhances it to also run experiments on EIGER-PORT, EIGER-PORT+ and EIGER-PORT++, alongside the enhancements provided by the ORA repository.

### Setting up the CloudLab cluster
On CloudLab start an experiment with an OpenStack profile. Select link-speed 1Gbps and the required number of nodes (clients + servers) (use d710 from Emulab). Please note that the results were calculated using 8 servers and 8 clients unless otherwise specified.

Once the CloudLab experiment is ready access to the OpenStack Dashboard as explained by cloudlab and create 16 nodes of size m1.large using the bionic-server image. Make sure to insert the following bash script in the configuration option:

        #!bin/bash

        sudo apt update
        sudo apt install -y default-jdk
        sudo apt install -y pssh
        sudo apt install -y maven

Then do the same with 1 m1.medium instance instead of large which we will refer to as Host and is the machine from which we will run our experiment.
Assign a floating IP to the Host machine, copy the codebase on it and SSH to it. 
The codebase should be copied so that in /home/ubuntu 3 folders appear:
- kaiju
- hosts
- results
Access the files all-cliens-txt and write there the IP addresses of all client machines, same for all-servers.txt. Finally in all-hosts.txt write all clients and all servers.
Now use the commmand:
    for h in IP_address_1 IP_address_2 etc. ; { ssh-copy-id ubuntu@$h ; }
substituting IP address for all the IPs of all clients and server instances as listed on OpenStack. And enter the same password used to access OpenStack. (this is to avoid needing the password every time).
Then compile the codebase by running the following 2 commands:
    cd ./kaiju
    mvn package
Finally copy the codebase to all machines. You can do so by using:
    cd /home/ubuntu
    for h in IP_address_1 IP_address_2 etc ; { scp -prq ./* ubuntu@$h:/home/ubuntu ; }

### Running an experiment
In experiment.py you find different experiments you can run that come from the RAMP paper. You can similarly expand and modify these experiments by altering the lists of parameters in the dictionary. For example the "tsize_test" is a test of varying transaction size. To run any experiment change to /home/ubuntu/experiment folder and run:

    python setup_hosts.py --color -c us-west-2 -nc 5 -ns 5 --experiment port --tag example

The logs will be uploaded in the output folder.

You may use python3 process_results.py name_of_result_repo to generate a csv file containing all the data from latency and throughput.

### Running an experiment on Data Freshness
To run data freshness please turn the freshness_test variable in Config.java to 1, there is also an option to do so in the starting script or you can do it manually then compile. The freshness will be logged in the servers logs.

### Further questions
Please refer to the RAMP github for further information on the codebase.