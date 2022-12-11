import pandas as pd
import time


table = "/home/prime/joern/parsed/home/prime/PycharmProjects/iridescent/corpus/JULY10/gennady.korotkevich/ARRANGE2/JULY10_gennady.korotkevich_ARRANGE2.cpp/nodes.csv"


def calculate_term_bigram_frequency(table):

    df = pd.read_csv(table,sep='\t')
    # Create a list of all the tokens in the 'Code' column
    df['code'] = df['code'].fillna("")
    tokens = df['code'].tolist()


   
    #Calculate the frequency of each bigram in the list of tokens
    bigrams = pd.Series(tokens).map(lambda x: [x[i:i+2] for i in range(len(x)-1)])
    bigram_freq = bigrams.explode().value_counts()

    # Return the calculated bigram frequencies
    print(bigram_freq)
    return bigram_freq














def calculate_branching_factor(node_file, edge_file):
    # Load the node and edge data into Pandas dataframes
    nodes = pd.read_csv(node_file)
    edges = pd.read_csv(edge_file)

    # Correlate the nodes and edges by matching the "key" and "start" or "end" columns
    nodes = nodes.merge(edges, left_on="key", right_on="start", how="outer")

    # Count the total number of nodes and children in the tree
    num_nodes = len(nodes)
    num_children = len(edges)

    # Calculate the branching factor by dividing the total number of children by the total number of nodes
    branching_factor = num_children / num_nodes

    return branching_factor








import pandas as pd

def calculate_maximum_depth(node_file, edge_file):
    # Load the node and edge data into Pandas dataframes
    nodes = pd.read_csv(node_file)
    edges = pd.read_csv(edge_file)

    # Correlate the nodes and edges by matching the "key" and "start" or "end" columns
    nodes = nodes.merge(edges, left_on="key", right_on="start", how="outer")

    # Set the maximum depth to 0
    max_depth = 0

    # Traverse the tree in a depth-first manner, starting from the root node
    for index, row in nodes.iterrows():
        # If the node is a leaf node, update the maximum depth to the distance from the root to the leaf node
        if row["childNum"] == 0:
            depth = row["depth"]
            max_depth = max(max_depth, depth)

    return max_depth







def calculate_ast_node_bigram_tf(node_table_path, edge_table_path):
    # Load the node and edge tables into memory using Pandas
    nodes = pd.read_csv(node_table_path)
    edges = pd.read_csv(edge_table_path)

    # Create an empty AST node bigram table
    bigrams = pd.DataFrame(columns=["Pair", "Frequency"])

    # Iterate through the rows of the node table
    for _, node in nodes.iterrows():
        # Check if the current node has a parent
        parent_node = edges[edges.end == node.key].first()
        if parent_node:
            # If the current node has a parent, add an entry to the AST node bigram table
            # with the node type pair (parent type, child type) and the frequency 1
            bigram = (parent_node.type, node.type)
            if bigram in bigrams.index:
                bigrams.loc[bigram, "Frequency"] += 1
            else:
                bigrams.loc[bigram] = 1

    # Calculate the term frequency of each bigram by dividing its frequency by the total
    # number of node type pairs in the table
    total_pairs = len(bigrams)
    bigrams["TF"] = bigrams["Frequency"] / total_pairs

    return bigrams












programmer_list, contest_list, round_list, numTernary_list, numKeywords_list = [], [], [], [], []
numComments_list, avgLineLength_list, stdDevLineLength_list, numTabs_list = [], [], [], []
numSpaces_list, numEmptyLines_list, whiteSpaceRatio_list, tabsLeadLines_list = [], [], [], []
WordUnigramTF_list, numFunctions_list, numTokens_list, newLineBeforeOpenBrace_list = [], [], [], []
branchingFactor_list, avgParams_list, cppKeywords_list, MaxDepthASTNode_list = [], [], [], []






fruits = ["apple", "orange","orange","orange"]


print(fruits.index('orange'))










