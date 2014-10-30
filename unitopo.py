"""
Read graphs in Pajek format.

See http://vlado.fmf.uni-lj.si/pub/networks/pajek/doc/draweps.htm
for format information.

This implementation handles only directed and undirected graphs including
those with self loops and parallel edges.  

Adapted by Morten Knutsen (morten.knutsen@uninett.no).
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
#    Copyright (C) 2008 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Distributed under the terms of the GNU Lesser General Public License
#    http://www.gnu.org/copyleft/lesser.html
import networkx,mininet.topo 
from networkx.utils import is_string_like
from mininet.topo import Topo

class uniTopo (Topo):

    
    def __init__( self, path='/home/gulzi/mininet/custom/isis-uninett.net' ):
        "Create Topology"
    
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
                    #print splitline
                    id, label = splitline[0:2]
                    #G.add_node(label)
                    nodelabels[id]='s'+id		
                    attr={'id':id}                
                    if len(splitline) > 2:
                        id,label,x,y=splitline[0:4]                
                        extras={'id':id,'x':x,'y':y}
			attr.update(extras)
                    s1 = self.addSwitch('s'+id,**attr)
                    h1 = self.addHost('h'+id)
                    self.addLink(h1,s1)
                    #extra_attr=zip(splitline[4::2],splitline[5::2])
                    #print extra_attr
                    #G.node_attr[label].update(extra_attr)
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
                    link_opts={'value':float(w)}
                    extra_attr=zip(splitline[3::2],splitline[4::2])
                    link_opts.update(extra_attr)
                    cap = int(splitline[6])
                    self.addLink(u,v)    


topos = { 'mytopo': ( lambda: uniTopo() ) }
