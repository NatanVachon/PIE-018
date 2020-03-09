# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:49:47 2020

@author: Simon
"""

import networkx as nx
import matplotlib.pyplot as plt

options = {
    'arrowstyle': '-|>',
    'arrowsize': 12,
}



G = nx.DiGraph()
for a in pivot.index:
    G.add_node(a) 
for i in pivot.index:
    for j in pivot.columns:
        if not((i, j) in list(G.edges)  or (j, i) in list(G.edges)) or i==j:
            G.add_edge(i,j,weight=pivot.loc[i,j])

avg_weight=pivot.mean().mean()

elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >1.2*avg_weight]
emed=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.8*avg_weight and d['weight']<1.2*avg_weight ]
esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <0.8*avg_weight]


pos=nx.spring_layout(G)

nx.draw_networkx_nodes(G,pos,node_size=1000)

# edges
nx.draw_networkx_edges(G,pos,edgelist=elarge,
                    width=6, arrows=True)
nx.draw_networkx_edges(G,pos,edgelist=esmall,
                    width=2,alpha=0.2, arrows=True)
nx.draw_networkx_edges(G,pos,edgelist=emed,
                    width=4,alpha=0.5, arrows=True)
# labels
nx.draw_networkx_labels(G,pos,**options,font_size=20,font_family='sans-serif')
nx.draw(G,with_labels=True, font_weight='bold')
