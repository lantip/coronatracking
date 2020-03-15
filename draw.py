#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
__version__     =   "0.0.1"
__author__      =   "@lantip"
__date__        =   "2020/03/15"
__description__ =   "Corona Tracking Indonesia"
""" 

import networkx as nx
import matplotlib
import pandas as pd
try:
    import matplotlib.pyplot as plt
except:
    # di osx perlu begini
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
from itertools import count
import sys
import argparse

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1], color=edge[2])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G, scale=2)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    elif graph_layout == 'planar':
        graph_pos=nx.planar_layout(G)
    elif graph_layout == 'kawai':
        graph_pos=nx.kamada_kawai_layout(G)
    elif graph_layout == 'circular':
        graph_pos=nx.circular_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=colors)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    #edge_labels = dict(zip(graph, labels))
    #nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
    #                            label_pos=edge_text_pos, bbox=dict(alpha=0), alpha=0)

    # show graph
    plt.tight_layout()
    plt.show()


google_sheet_url = 'https://docs.google.com/spreadsheets/d/1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw/export?format=csv&gid=0'
df  = pd.read_csv(google_sheet_url, skiprows=[0,1], usecols=range(20), header=None)

graph = []
for index, row in df.iterrows():
    if str(row[8]) == 'nan':
        if str(row[6]) == 'Lokal':
            if str(index+1) == '20':
                graph.append((str(index+1),'1', 'r', {'group': '1'}))
            else:    
                graph.append((str(index+1),str(index+1), 'b',  {'group': 'self'}))
        elif 'diamond' in str(row[7]).lower():
            graph.append((str(index+1),'Kapal', 'b',  {'group': 'kapal'}))
        else:
            graph.append((str(index+1),'Luar', 'g',  {'group': 'luar'}))
    else:
        graph.append((str(index+1),str(row[8]), 'r',  {'group': str(row[8])}))



def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument('-l', '--layout', type=str, default='spring', help="Masukkan jenis layoutnya: spring, kawai, spectral, random", required=True)
    args = parser.parse_args()

    layout = args.layout

    draw_graph(graph, graph_layout=layout, node_size=360, node_text_size=10, node_alpha=0.3)


if __name__ == '__main__':
    main()


