
__author__ = """hafiz muhammad gulzar hmgulzar88@gmail.com"""

import networkx,mininet.topo,os 
from networkx.utils import is_string_like
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, output
from mininet.node import Host, Controller, RemoteController
from mininet.util import irange, custom, quietRun, dumpNetConnections
from mininet.cli import CLI
from time import sleep, time
from multiprocessing import Process
from subprocess import Popen
from mininet.log import setLogLevel
import random
from functools import partial
import argparse
import sys
import os
import signal
import httplib

links_descr = {}
class uniTopo (Topo):
    scale = 10000
    
    def __init__( self, path=os.getcwd()+'/isis-uninett.net' ):
        "Creates uninett  Topology into mininet"
    
        # Initialize topology
        Topo.__init__( self )
	fh=open(path,mode='r')
	lines = fh.readlines()
        import shlex
        if is_string_like(lines): lines=iter(lines.split('\n'))
        lines = iter([line.rstrip('\n') for line in lines])
        while lines:
            try:
                l=lines.next()
                l=l.lower()
            except: #EOF
                break
            if l.startswith("#"):
                continue
            if l.startswith("*network"):
                label,name=l.split()
                toponame=name
            if l.startswith("*vertices"):
                nodelabels={}
                l,nnodes=l.split()
                while not l.startswith("*arcs"):
                    if l.startswith('#'):
                        l = lines.next()
                        l = l.lower()
                        continue
                    if l.startswith('*'):
                        l = lines.next()
                        l = l.lower()
                        continue
                    splitline=shlex.split(l)                    
                    id, label = splitline[0:2]                  
                    nodelabels[id]='s'+id		
                    attr={'id':id}                
                    if len(splitline) > 2:
                        id,label,x,y=splitline[0:4]                
                        extras={'id':id,'x':x,'y':y}
			attr.update(extras)
		                
                    s1 = self.addSwitch('s'+id,**attr)                    
		    h1 = self.addHost('h'+id)
                    self.addLink(h1,s1,bw=100)
                    l = lines.next()
                    l = l.lower()
            if l.startswith("*arcs"):
                for l in lines:
                    if not l: break
                    if l.startswith('#'): continue
                    splitline=shlex.split(l)
                    ui,vi,w=splitline[0:3]
                    u=nodelabels.get(ui,ui)
                    v=nodelabels.get(vi,vi)
		    link_label = splitline[4]
		    #print link_descr
                    link_opts={'value':float(w)}
                    extra_attr=zip(splitline[3::2],splitline[4::2])
                    link_opts.update(extra_attr)
                    cap = int(splitline[6])
		    scaledCap = cap/self.scale
		    addedLink = self.addLink(v,u,bw=scaledCap)
		    links_descr[link_label] = addedLink
		    #print links_descr[link_label]	
		   

        
          		
#topos = { 'unitopo': ( lambda: uniTopo() ) }

def loadTraffic(host,url,net):
	conn = httplib.HTTPConnection(host)
	conn.request("GET",url)
	r1 = conn.getresponse()
	if r1.status !=200:
		conn.close()
		return {}
	data1 = r1.read()
	if not data1:
		conn.close()
		return {}
	conn.close()

	loads_by_descr = {}
	retloads = {}
	for line in data1.split('\n'):
		if not line: continue
		tokens = line.split()
		descr = tokens[0].strip()
		avgIn = tokens[3].strip()
		avgOut = tokens[4].strip()
		if links_descr.has_key(descr):
			host1,host2 = links_descr[descr]
			h1,h2 = net.get(host1,host2)			
			net.iperf((h1,h2),l4Type='UDP',udpBw=avgOut)
			net.iperf((h2,h1),l4Type='UDP',udpBw=avgIn)

def startMininetTopo():
	topo = uniTopo()
	net = Mininet(topo=topo, link=TCLink,controller=partial (RemoteController, ip='10.0.2.15'))
	net.start()
	#net.startTerms()
	print "background process"
	loadTraffic('drift.uninett.no','/nett/ip-nett/load-now',net)
	CLI(net)
	net.stop()

def main():
	startMininetTopo()
	return

if __name__ == '__main__':
	setLogLevel('info')
	main()
