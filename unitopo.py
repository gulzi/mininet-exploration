
__author__ = """hafiz muhammad gulzar hmgulzar88@gmail.com"""

import networkx,mininet.topo,os 
from networkx.utils import is_string_like
from mininet.topo import Topo
from mininet.link import TCLink
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
                    idz, label = splitline[0:2]
		    print label                  
                    nodelabels[idz]='s'+idz		
                    #attr={'id':id}                
                    #if len(splitline) > 2:
                        #id,label,x,y=splitline[0:4]                
                        #extras={'id':id,'x':x,'y':y}
			#attr.update(extras)
		                
                    s1 = self.addSwitch('s'+idz)                    
		    h1 = self.addHost('h'+idz)
                    self.addLink(h1,s1)
                    l = lines.next()
                    l = l.lower()
            if l.startswith("*arcs"):
                for l in lines:
                    if not l: break
                    if l.startswith('#'): continue
                    splitline=shlex.split(l)
                    ui,vi,w=splitline[0:3]
                    u=nodelabels.get(ui)
                    v=nodelabels.get(vi)
                    link_opts={'value':float(w)}
                    extra_attr=zip(splitline[3::2],splitline[4::2])
                    link_opts.update(extra_attr)
                    cap = int(splitline[6])
		    scaledCap = cap/self.scale
		    if self.isSwitch(u):
			print "yes"
			if self.isSwitch(v):
				print "again yes"
				if v.connectionsTo(u):continue
				else:
					a = self.addLink(v,u)
	            
          		
topos = { 'unitopo': ( lambda: uniTopo() ) }

