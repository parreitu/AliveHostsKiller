#!/usr/bin/python
"""
Author: Pedro Arreitunandia

You can use this scripts to force the shutdown of Windows hosts in distinct networks

The user must have admin permissions in remote clients. 

We use this script all nights to shutdown alive computers on our network.

Code and the last version: https://github.com/parreitu/AliveHostsKiller

"""

import logging
import nmap
import os

# Here we configure the logger parameters
logger = logging.getLogger('AliveHostsKiller') 
handler = logging.FileHandler('/tmp/AliveHostsKiller.log') 
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s') 
handler.setFormatter(formatter) 
logger.addHandler(handler) 
logger.setLevel(logging.INFO)

# You can put in the white_liste the hosts that you permit to be alive.
# white_list=["192.168.1.1","192.168.1.5"]
white_list=[]

# The user must have admin permissions in the remote host
user="root" 
password="YOURPASSWORD"


# You have define the networks to be checked. You have to edit and put your own networks
networks = ["192.168.10.0/24","192.168.11/24","192.168.12.0/24"]

# We will use nmap to check the network
nm = nmap.PortScanner()

for i in range(len(networks)): 
    # The log will be written in the file /tmp/AliveHostsKiller.log
    logger.info('------------------------------------')
    logger.info( "Network: %s",  networks[i] )
    logger.info('------------------------------------')

    # We use nmap on the selected network
    nm.scan(hosts=networks[i], arguments='-sP')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

    for host,status in hosts_list:
        if (status == "up") and not (host in white_list):            
            # Only for the alive hosts that aren't in the while list
            logger.info( "Host IP address: %s",  host )
            command = 'net rpc SHUTDOWN -C "This system was left on after hours and is being shutdown" -f -I '+host+' -U '+user+'%'+password
            # !!!!!!!!!!!!!!!! 
            # Caution! Uncomment this line throws the shutdown command to the host
            #os.system(command)
