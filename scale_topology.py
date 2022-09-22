#!/usr/bin/env python

__author__ = "Aravind"
__email__ = "aprabh@juniper.net"

"""
This script is used to generate a scaled topology of a PE and a service chain function
"""

import sys
import yaml
import docker
import netaddr

parser =  argparse.ArgumentParser()
parser.add_argument("-n", action='store', dest='num', help='number of PE with service chain')
args = parser.parse_args()

def Gentopology(NUM_PE):
    list_nodes = []
    for i in range(0, NUM_PE):
        nodes = {}
        nodes["name"] = "pe_{}".format(i)
        nodes["image"] = "crpd:latest"
        nodes["volume"][0]["name"] = "config"
        nodes["volume"][0]["path"] = "/config"
        nodes["volume"][1]["name"] = "varlog"
        nodes["volume"][1]["path"] = "/var/log"
        for linknum in range(0,1):
            nodes["image"]["link"][linknum]["name"] = "sc_{}".format(i) 
            # use a /30 network (use odd)
            nodes["image"]["link"][linknum]["prefix"] = "192.168.1.1"
        list_nodes.append(nodes)
    #Create the Service chain nodes
    for j in range(0, NUM_PE):
        nodes = {}
        nodes["name"] = "sc_{}".format(j)
        nodes["image"] = "crpd:latest"
        nodes["volume"][0]["name"] = "config"
        nodes["volume"][0]["path"] = "/config"
        nodes["volume"][1]["name"] = "varlog"
        nodes["volume"][1]["path"] = "/var/log"
        for linknum in range(0,1):
            nodes["image"]["link"][linknum]["name"] = "pe_{}".format(j)
            # use a /30 network (use even)
            nodes["image"]["link"][linknum]["prefix"] = "192.168.1.2"
        list_nodes.append(nodes)
    
    with open("scale_topo_bmp.yml", "w") as f:
        f.write(yaml.safe_dump(list_nodes, default_flow_style=False))

def main():
    print("Generating a scaled topology for service chain discovery poc")
    Gentopology(int(args.num))

if __name__ == "__main__":
    main()
        
