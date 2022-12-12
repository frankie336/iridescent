import time

import pandas as pd


edges_file = "/home/prime/joern/parsed/home/prime/PycharmProjects/iridescent/corpus/LTIME110A/gennady.korotkevich/LARGEFAM/LTIME110A_gennady.korotkevich_LARGEFAM.cpp/edges.csv"

nodes_file = "/home/prime/joern/parsed/home/prime/PycharmProjects/iridescent/corpus/LTIME110A/gennady.korotkevich/LARGEFAM/LTIME110A_gennady.korotkevich_LARGEFAM.cpp/nodes.csv"


import pandas as pd


import pandas as pd

import pandas as pd

def get_term_frequency(nodes_file, edges_file):
    # Load the nodes and edges tables from the CSV files
    nodes = pd.read_csv(nodes_file,sep='\t')
    edges = pd.read_csv(edges_file,sep='\t')

    # Check if the command, key, and childNum columns are present in the nodes table
    # and the start and end columns are present in the edges table
    if "command" not in nodes.columns:
        raise KeyError("The nodes table does not contain the 'command' column")
    if "key" not in nodes.columns:
        raise KeyError("The nodes table does not contain the 'key' column")
    if "childNum" not in nodes.columns:
        raise KeyError("The nodes table does not contain the 'childNum' column")
    if "start" not in edges.columns:
        raise KeyError("The edges table does not contain the 'start' column")
    if "end" not in edges.columns:
        raise KeyError("The edges table does not contain the 'end' column")

    # Filter the nodes table to only include leaf nodes (nodes without children)
    leaves = nodes[nodes["childNum"] == 0]

    # Group the leaf nodes by their code and count the number of occurrences of each code
    term_frequency = leaves.groupby("code")["code"].count()

    # Return the term frequency as a dictionary
    return term_frequency.to_dict()




print(get_term_frequency(nodes_file,edges_file))
