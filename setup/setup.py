from multiprocessing import Pool
import os


def generate_setup_cmd(key):
    cmd = " \"mkdir -p ~/.ssh && echo " + key + " >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys\""
    return cmd

def run_cmd(h,command):
    print(h)
    os.system("ssh -o StrictHostKeyChecking=no " + h + command)

def run_setup(h,command):
    username, domain = h.split("@")
    cmd = "ssh-keygen -f \"/home/luca/.ssh/known_hosts\" -R \"" +  domain + "\""
    os.system(cmd)
    os.system("ssh -o StrictHostKeyChecking=no " + h + command)

def setup(hosts):
    username, domain = hosts[0].split("@")
    cmd = "ssh-keygen -f \"/home/luca/.ssh/known_hosts\" -R \"" +  domain + "\""
    os.system(cmd)
    os.system(f'ssh -o StrictHostKeyChecking=no {hosts[0]} "ssh-keygen -t rsa -N \"\" -f ~/.ssh/id_rsa"')
    key = os.popen(f'ssh -o StrictHostKeyChecking=no {hosts[0]} remote "cat ~/.ssh/id_rsa.pub"').read()
    cmd = generate_setup_cmd(key)
    with Pool(process=len(hosts)-1) as pool:
        pool.starmap(run_setup, [(h,cmd) for h in hosts[1:]])

    
def build(hosts):
    cmd = " \"sudo apt update ; sudo apt install -y default-jdk ; sudo apt install -y pssh ; sudo apt install -y maven ; git clone git@github.com:lucamul/Eiger-PORT-plus-plus.git ; mv /home/ubuntu/Eiger-PORT-plus-plus/* /home/ubuntu/ ; sudo rm -r /home/ubuntu/Eiger-PORT-plus-plus/ ; cd /home/ubuntu/kaiju ; mvn package ; cd /home/ubuntu/kaiju/contrib/YCSB ; mvn package ; \""
    with Pool(processes=len(hosts)) as pool:
        pool.starmap(run_cmd, [(host, cmd) for host in hosts])

hosts = [
    
]

if __name__ == "__main__":
    setup(hosts)
    build(hosts)