import clang_parse
from clang_parse import *
import os
import time
import abc
import re
import pandas as pd
from largecollections import cpp_7keywords,cpp_keywords
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter


class FeaturesInterface(metaclass=abc.ABCMeta):
    """Formal Interface"""
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'reads_text') and
                callable(subclass.reads_text) and

                hasattr(subclass, 'get_unigrams') and
                callable(subclass.get_unigrams_freq) and

                hasattr(subclass, 'get_length') and
                callable(subclass.get_length) and

                hasattr(subclass, 'get_char') and
                callable(subclass.get_char) and

                hasattr(subclass, 'get_comments') and
                callable(subclass.get_comments) and

                hasattr(subclass, 'average_line_len') and
                callable(subclass.average_line_len) and

                hasattr(subclass, 'standard_dev_lines') and
                callable(subclass.standard_dev_lines) and

                hasattr(subclass, 'get_empty_lines') and
                callable(subclass.get_empty_lines) and

                hasattr(subclass, 'white_space_ratio') and
                callable(subclass.white_space_ratio) and

                hasattr(subclass, 'indented_lines') and
                callable(subclass.indented_lines) and

                hasattr(subclass, 'get_keywords7_cpp') and
                callable(subclass.get_keywords7_cpp) and

                hasattr(subclass, 'get_keywords_cpp') and
                callable(subclass.get_keywords_cpp) and

                hasattr(subclass, 'get_avg_params_cpp') and
                callable(subclass.get_avg_params_cpp) and

                hasattr(subclass, 'get_functions_cpp') and
                callable(subclass.get_functions_cpp) and

                hasattr(subclass, 'get_tokens') and
                callable(subclass.get_tokens) and

                hasattr(subclass, 'get_braces') and
                callable(subclass.get_braces) and

                hasattr(subclass, 'calculate_tree_branching_factor') and
                callable(subclass.calculate_tree_branching_factor) and

                hasattr(subclass, 'calculate_maximum_depth') and
                callable(subclass.calculate_maximum_depth) and

                hasattr(subclass, 'calculate_ast_node_bigram_tf') and
                callable(subclass.calculate_ast_node_bigram_tf) and

                hasattr(subclass, 'get_term_frequency') and
                callable(subclass.get_term_frequency) and

                hasattr(subclass, 'data_chain') and
                callable(subclass.data_chain) or


                NotImplemented)


    @abc.abstractmethod
    def reads_text(self,file_name: str) -> str:
        """
        reads text files
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_unigrams_freq(self, files: str) -> str:
        """
        Unigram frequency
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_length(self,files: str) -> str:
        """
        counts the length of file
        in characters. Sets the
        self.length object
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_char(self, character: str, feature) ->str:
        """
        A More general approach to
        counting characters  like
        tabs, and spaces
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_comments(self:str) -> str:
        """
        Log of the number of comments divided by
        length)
        file length in characters
        """
        raise  NotImplemented


    @abc.abstractmethod
    def average_line_len(self, files: str) ->str:
        """
        The average length of each line
        """
        raise NotImplemented

    @abc.abstractmethod
    def standard_dev_lines(self):
        """
        The standard deviation of the character
        lengths of each line
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_empty_lines(self, files: str) -> str:
        """
        Log of the number of empty lines divided
        by file length in characters, excluding
        leading and trailing lines between lines of
        Text
        """
        raise NotImplemented

    @abc.abstractmethod
    def white_space_ratio(self, files: str) ->str:
        """
        The ratio between the number of whites-
        pace characters (spaces, tabs, and new-
        lines) and non-whitespace characters
        """
        raise NotImplemented

    @abc.abstractmethod
    def indented_lines(self, files: str) -> str:
        """
        A boolean representing whether the ma-
        jority of indented lines begin with spaces
        or tabs
        """
        raise NotImplemented



    @abc.abstractmethod
    def get_keywords7_cpp(self, files: str) ->str:

        """
        Log of the number of occurrences of key-length)
        word divided by file length in characters,
        where keyword is one of do, else-if, if, else,
        switch, for or while
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_keywords_cpp(self, files: str) ->str:
        """
        Term frequency of 84 C++ keywords
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_avg_params_cpp(self):
        """
        The standard deviation of the number of
        parameters among all functions
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_functions(self, files: str) -> str:
        """
        A regex partial match for
        all C++ functions in
        a document

        """
        raise NotImplemented

    @abc.abstractmethod
    def get_tokens(self, files: str) ->str:
        """
        Log of the number of word tokens divided
        by file length in characters
        """
        raise NotImplemented


    @abc.abstractmethod
    def get_braces(self, files: str) ->str:
        """
        A boolean representing whether the ma-
        jority of code-block braces are preceded
        by a newline character
        """
        raise NotImplemented


    @abc.abstractmethod
    def calculate_maximum_depth(self,ode_file:str, edge_file:str)->str:
        """

        Maximum depth of an AST node
        """
        return NotImplemented

    @abc.abstractmethod
    def calculate_tree_branching_factor(self,node_file:str, edge_file:str)->str:
        """
        Branching factor of the tree formed by con-
        verting code blocks of files into nodes
        """
        return NotImplemented


    @abc.abstractmethod
    def calculate_ast_node_bigram_tf(self,node_table_path:str, edge_table_path:str)->str:
        """
        Term frequency AST node bigrams
        """
        return NotImplemented

    @abc.abstractmethod
    def get_term_frequency(self,nodes_file:str, edges_file:str) ->str:
        """
        Term frequency of code unigrams in
        AST leaves
        """



    @abc.abstractmethod
    def data_chain(self):
        """
        A series of methods that collects features
        from code
        """
        raise NotImplemented


class FeatureExtractor(FeaturesInterface):

    cpp_comments_regx = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    def __init__(self):

        self.length = None
        self.lines_lengths = []
        self.tabsLeadLines = False
        self.ave_param = 0
        self.total_param = 0
        self.total_funcs = 0



    def reads_text(self,file_name: str) -> str:
        """
        reads text files
        """
        with open(file_name) as f:
            the_file = f.readlines()

        return  the_file


    def get_unigrams_freq(self, files: str) -> str:
        """
        Unigram Freequency

        """
        file_string = "".join(self.reads_text(file_name=files))

        unigrams_list  = file_string.split()

        collect = []

        counter = Counter(unigrams_list)
        for element, count in counter.items():
            collect.append(count)

            print(f"{element}: {count}")

        summed = sum(collect)

        return summed







    def get_length(self, files: str) -> str:
        """
		counts the length of file
		in characters
		"""
        file_string = "".join(self.reads_text(file_name=files))

        length = int(len(file_string))

        return length



    def get_char(self, character: str, feature: str, files: str)->str:
        """
        A More general approach to
        counting characters  like
        tabs, and spaces
        """
        read_file = self.reads_text(file_name=files)

        file_string = "".join(read_file)

        find = [character]

        filter_chars = re.findall(r"(?=(" + '|'.join(find) + r"))", file_string)

        total_chars = len(filter_chars)

        feature_chars = total_chars / self.length



        #print('Total length in characters: ' + str(self.length), '\n',
                  #'Total occurrences of '+feature+': ' + (str(total_chars)), '\n',
                  #'The Feature metric of '+feature+': ' + str(feature_chars)

                  #)

        return feature_chars



    def get_comments(self, files: str) -> str:

        """
        Log of the number of comments divided by
        length)
        file length in characters
        """
        read_file = self.reads_text(file_name=files)
        file_string = "".join(read_file)

        cpp_comment = FeatureExtractor.cpp_comments_regx
        ptrn = re.compile(cpp_comment, re.MULTILINE)
        comments_found = ptrn.findall(file_string)

        #print(comments_found)

        comments_num = len(comments_found)

        feature_comments = comments_num/self.length

        #print('Comments found: '+str(comments_num),'\n',
              #'The feature metric of comments: '
              #)

        return feature_comments



    def average_line_len(self, files: str) ->str:
        """
        The average length of each line
        """
        read_file = self.reads_text(file_name=files)
        total_lines = len(read_file)

        all_lengths = []

        for l in read_file:
            length = len(l)
            #print(length)
            all_lengths.append(length)

        #print(all_lengths)
        average_len = np.average(all_lengths)
        #print ('The average length of characters on each line: '+str(average_len))

        self.lines_lengths = all_lengths#Set this up for later use in annother method

        return  average_len



    def standard_dev_lines(self):
        """
        The standard deviation of the character
        lengths of each line
        """
        line_len_sdev = np.std(self.lines_lengths)
        #print('The standard dev of the character lengths of each line: '+str(line_len_sdev))

        return line_len_sdev



    def get_empty_lines(self, files: str) -> str:
        """
        Log of the number of empty lines divided
        by file length in characters, excluding
        leading and trailing lines between lines of
        Text
        """
        read_file = self.reads_text(file_name=files)
        #print(read_file)

        filter_empty_lines = [x for x in read_file if x == "\n"]
        total_empty = len(filter_empty_lines)

        #print(filter_empty_lines)

        feature_empty = total_empty /self.length

        #print('Total Empty lines: '+str(total_empty),'\n',
              #'The feature metric of empty lines: '+ str(feature_empty)
              #)

        return  feature_empty




    def white_space_ratio(self, files: str) ->str:
        """
        The ratio between the number of whites-
        pace characters (spaces, tabs, and new-
        lines) and non-whitespace characters
        ::x:1
        """
        read_file = self.reads_text(file_name=files)
        file_string = "".join(read_file)
        find_white = ['\n','\t',' ']

        all_white_spaces = re.findall(r"(?=(" + '|'.join(find_white) + r"))", file_string)
        #print(all_white_spaces)

        find_all = ['.']
        all_chars = re.findall(r"(?=(" + '|'.join(find_all) + r"))", file_string)
        #print(all_chars)

        filter_these = ['\n','\t',' ']
        non_white = [x for x in all_chars if x not in filter_these]
        #print(non_white)

        white_num = len(all_white_spaces)
        #print(white_num)

        non_white_num = len(non_white)
        #print(non_white_num)

        ratio = round(non_white_num/white_num)

        return ratio


    def indented_lines(self, files: str) -> str:
        """
        A boolean representing whether the ma-
        jority of indented lines begin with spaces
        or tabs
        """
        read_file = self.reads_text(file_name=files)
        file_string = "".join(read_file)

        find_indents = re.findall(r'(^\s*.)', file_string, flags=re.MULTILINE)

        starts_with_tab = [x for x in find_indents if '\t' in x]
        starts_with_space = [x for x in find_indents if ' ' in x]


        if len(starts_with_tab) > len(starts_with_space):

            self.tabsLeadLines = True



    def get_keywords7_cpp(self, files: str) ->str:
        """
        Log of the number of occurrences of key-length)
        word divided by file length in characters,
        where keyword is one of do, else-if, if, else,
        switch, for or while
        """
        key_words = cpp_7keywords
        #print(key_words)

        read_file = self.reads_text(file_name=files)
        file_string = "".join(read_file)

        #Gets all key words
        key_words_found = re.findall(r"(?=(" + '|'.join(key_words) + r"))", file_string)
        unique_keywords = list(set(key_words_found))

        len_keywords = int(len(key_words_found))
        len_unique_keywords  = len(unique_keywords)

        feature_all_key_word = len_keywords/self.length
        feature_unique_key_word = len_unique_keywords / self.length


        #print('Total length in characters: '+str(self.length),'\n',
              #'Total unique occurrences of keywords: '+str(len(unique_keywords)),'\n',
              #'From a subset of '+str(len(key_words))+' keyords','\n'
               #'The Feature metric of unique keywords found: ' + str(feature_key_word),'\n',
              #'The Feature metric of all keywords found: ' + str(feature_unique_key_word), '\n'
              #)

        return feature_all_key_word, feature_unique_key_word


    def get_keywords_cpp(self, files: str) ->str:
        """
        Term frequency of 84 C++ keywords
        """
        read_file = self.reads_text(file_name=files)
        file_string = "".join(read_file)

        # Gets all key words
        key_words_found = re.findall(r"(?=(" + '|'.join(cpp_keywords) + r"))", file_string)

        feature_all_key_word = len(key_words_found)

        return feature_all_key_word




    def get_avg_params_cpp(self):
        """
        The standard deviation of the number of
        parameters among all functions
        """
        subtract_mean = self.total_param - self.ave_param

        if subtract_mean ==0:
            return 0

        square = subtract_mean *2

        divide = square/self.total_funcs

        root = (math.sqrt(divide))


        return root


    def get_functions(self, files: str) -> str:
        """
        A regex partial match for
        all C++ functions in
        a document

        """
        reg_pat = '(.*)(\(\))(.*)'
        file_string = ''.join(self.reads_text(file_name=files))
        funcs = re.compile(reg_pat)
        found_funcs = funcs.findall(file_string)

        total_functions = (int(len(found_funcs)))

        feature_functions = total_functions/self.length

        return feature_functions


    def get_tokens(self, files: str) ->str:
        """
        Log of the number of word tokens divided
        by file length in characters
        """
        file_string = ''.join(self.reads_text(file_name=files))
        tokens = file_string.split()

        total_tokens  = int(len(tokens))

        feature_tokens = total_tokens/self.length

        return feature_tokens



    def get_braces(self, files: str) ->str:
        """
        A boolean representing whether the ma-
        jority of code-block braces are preceded
        by a newline character
        """
        file_string = ''.join(self.reads_text(file_name=files))

        filter_newline_precedes = ['\\n{', '\\n}']
        filter_all_braces = ['{','}']

        precedes = re.findall(r"(?=(" + '|'.join(filter_newline_precedes) + r"))",file_string)

        all_braces = re.findall(r"(?=(" + '|'.join(filter_all_braces) + r"))", file_string)

        len_precedes = len(precedes)
        len_all = len(all_braces)

        if len_precedes > len_all/2:
            return True
        else:
            return False



    def calculate_tree_branching_factor(self, node_file: str, edge_file: str) -> str:
        """
        Branching factor of the tree formed by con-
        verting code blocks of files into nodes
        """
        nodes = pd.read_csv(node_file,sep='\t')
        edges = pd.read_csv(edge_file,sep='\t')

        #Correlate the nodes and edges by matching the "key" and "start" or "end" columns
        nodes = nodes.merge(edges, left_on="key", right_on="start", how="outer")

        #Count the total number of nodes and children in the tree
        num_nodes = len(nodes)
        num_children = len(edges)

        # Calculate the branching factor by dividing the total number of children by the total number of nodes
        branching_factor = num_children / num_nodes

        return branching_factor





    def calculate_maximum_depth(self, node_file: str, edge_file: str) -> str:
        """

        Maximum depth of an AST node
        """
        # Load the node and edge data into Pandas dataframes
        nodes = pd.read_csv(node_file,sep='\t')
        edges = pd.read_csv(edge_file,sep='\t')


        # Correlate the nodes and edges by matching the "key" and "start" or "end" columns
        nodes = nodes.merge(edges, left_on="key", right_on="start", how="outer")





        # Set the maximum depth to 0
        max_depth = 0

        #Use the min key value to calculte difference
        root = nodes["key"].min()

        # Traverse the tree in a depth-first manner, starting from the root node
        for index, row in nodes.iterrows():

            # If the node is a leaf node, update the maximum depth to the distance from the root to the leaf node
            if row["childNum"] == 0:

                cur_depth = row["key"] - root
                if cur_depth > max_depth:
                    max_depth +=cur_depth
                    print(max_depth)



        return max_depth


    def calculate_ast_node_bigram_tf(self,node_table_path:str, edge_table_path:str)->str:
        """

        Term frequency AST node bigrams

        """
        # Load the node and edge tables into memory using Pandas
        nodes = pd.read_csv(node_table_path, sep='\t')
        edges = pd.read_csv(edge_table_path, sep='\t')


        bigrams_list = []

        for _, node in nodes.iterrows():
            # Check if the current node has a parent
            parent_node = edges[edges.end == node.key]

            if len(parent_node) >0:
                parent_node = parent_node
                # If the current node has a parent, add an entry to the AST node bigram table
                # with the node type pair (parent type, child type) and the frequency 1

                bigram = parent_node["type"].values[0]+'/'+node["type"]
                bigrams_list.append(bigram)


        bigrams = pd.DataFrame(bigrams_list, columns=["pair"])
        bigrams["frequency"] = 1

        agg_functions = {'pair': 'first', 'frequency': 'sum'}
        combined = bigrams.groupby(bigrams['pair']).aggregate(agg_functions)
        summed = combined["frequency"].sum()


        return summed



    def get_term_frequency(self, nodes_file: str, edges_file: str) -> str:
        """
        Term frequency of code unigrams in
        AST leaves
        """
        # Load the nodes and edges tables from the CSV files
        nodes = pd.read_csv(nodes_file, sep='\t')
        edges = pd.read_csv(edges_file, sep='\t')

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

        unigram_list = leaves["code"].tolist()

        counter = Counter(unigram_list)

        collect = []

        for element, count in counter.items():
            collect.append(count)
            print(f"{element}: {count}")

        summed = sum(collect)


        return summed





    def data_chain(self):
        """
        A series of methods that collects features
        from code
        """
        programmer, contest_list, round_list, numTernary_list, numKeywords_list = [], [], [], [], []
        numComments_list, avgLineLength_list, stdDevLineLength_list, numTabs_list = [], [], [], []
        numSpaces_list, numEmptyLines_list, whiteSpaceRatio_list, tabsLeadLines_list = [], [], [], []
        WordUnigramTF_list, numFunctions_list, numTokens_list, newLineBeforeOpenBrace_list = [], [], [], []
        branchingFactor_list, avgParams_list, cppKeywords_list, MaxDepthASTNode_list = [], [], [], []
        ASTNodeBigramsTF_list,CodeInASTLeavesTF_list = [],[]

        master_feature_dict = {'programmer': programmer,'contest':contest_list,'round':round_list,
                               'WordUnigramTF':WordUnigramTF_list,
                               'numTokens':numTokens_list,'numTernary':numTernary_list,
                               'numKeywords':numKeywords_list,
                               'avgParams':avgParams_list,'numFunctions':numFunctions_list,
                               #'nestingDepth':nestingDepth_list,
                               'numComments':numComments_list,'avgLineLength':avgLineLength_list,
                               'stdDevLineLength':stdDevLineLength_list,'numTabs':numTabs_list,
                               'numSpaces':numSpaces_list,'numEmptyLines':numEmptyLines_list,
                               'whiteSpaceRatio':whiteSpaceRatio_list,
                               'newLineBeforeOpenBrace':newLineBeforeOpenBrace_list,
                               'tabsLeadLines':tabsLeadLines_list,
                               'cppKeywords':cppKeywords_list,'MaxDepthASTNode':MaxDepthASTNode_list,
                               'branchingFactor':branchingFactor_list,'ASTNodeBigramsTF':ASTNodeBigramsTF_list,
                               'CodeInASTLeavesTF':CodeInASTLeavesTF_list

                               }



        index_file = 'corpus/INDEX.txt'
        index_file = self.reads_text(file_name=index_file)
        files = [s.strip('\n') for s in index_file]



        for x in files:
            """
            x is the location of files
            meta gets the string 
            value for later use
            """
            meta = x.split('/')
            programmer.append(meta[2])
            contest_list.append(meta[1])
            round_list.append(meta[3])



            """
            Calculating the branching factor
            By using Joren generated .csv
            parse of each file.
            https://joern.readthedocs.io/en/dev/import.html
            
            The average branching factor can be quickly calculated
            as the number of non-root nodes (the size of the tree, 
            minus one; or the number of edges) divided by the number 
            of non-leaf nodes (the number of nodes with children). 
            """
            current_dir = os.getcwd()
            home_dir = os.path.expanduser("~")
            nodescsv = home_dir+'/joern/parsed/'+current_dir+'/corpus/'+meta[1]+'/'+meta[2]+\
                  '/'+meta[3]+'/'+meta[1]+'_'+meta[2]+'_'+meta[3]+'.cpp/nodes.csv'




            edgescsv  = home_dir+'/joern/parsed/'+current_dir+'/corpus/'+meta[1]+'/'+meta[2]+\
                  '/'+meta[3]+'/'+meta[1]+'_'+meta[2]+'_'+meta[3]+'.cpp/edges.csv'

            #nodesdf = pd.read_csv(nodescsv,sep='\t')
            #nodesdf['childNum'] = nodesdf['childNum'].fillna(0)
            #print(nodesdf['childNum'])
            #child_list = nodesdf["childNum"].values.tolist()
            #non_leafs_list = [x for x in child_list if x !=0.0]
            #print(child_list)
            #print(non_leafs_list)
            #nestingDepth = len(child_list)/len(non_leafs_list)
            #nestingDepth_list.append(nestingDepth)
            #print(nodescsv,'<-----')


            self.length = self.get_length(files=x)#len

            MaxDepthASTNode = self.calculate_maximum_depth(node_file=nodescsv,edge_file=edgescsv)
            MaxDepthASTNode_list.append(MaxDepthASTNode)

            branchingFactor = self.calculate_tree_branching_factor(node_file=nodescsv,edge_file=edgescsv)
            branchingFactor_list.append(branchingFactor)

            ASTNodeBigramsTF = self.calculate_ast_node_bigram_tf(node_table_path=nodescsv,edge_table_path=edgescsv)
            ASTNodeBigramsTF_list.append(ASTNodeBigramsTF)


            CodeInASTLeavesTF = self.get_term_frequency(nodes_file=nodescsv,edges_file=edgescsv)
            CodeInASTLeavesTF_list.append(CodeInASTLeavesTF)#


            WordUnigramTF = self.get_unigrams_freq(files=x)
            #uni = ', '.join(WordUnigramTF)
            WordUnigramTF_list.append(WordUnigramTF)

            key_words = self.get_keywords7_cpp(files=x)
            numTernary = key_words[0]#
            numKeywords = key_words[1]
            numTernary_list.append(numTernary)
            numKeywords_list.append(numKeywords)

            #branchingFactor = clang_parse.get_funcs(files=x)
            #self.ave_param = branchingFactor[0]
            #branchingFactor_list.append(self.ave_param)
            #self.total_param = branchingFactor[1]
            #self.total_funcs = branchingFactor[2]

            avgParams = self.get_avg_params_cpp()
            avgParams_list.append(avgParams)

            numTokens = self.get_tokens(files=x)
            numTokens_list.append(numTokens)

            numFunctions = self.get_functions(files=x)
            numFunctions_list.append(numFunctions)

            numComments = self.get_comments(files=x)
            numComments_list.append(numComments)

            avgLineLength = self.average_line_len(files=x)
            avgLineLength_list.append(avgLineLength)

            stdDevLineLength = self.standard_dev_lines()
            stdDevLineLength_list.append(stdDevLineLength)

            numTabs = self.get_char(character='\t', feature='tabs', files=x)
            numTabs_list.append(numTabs)

            numSpaces = self.get_char(character=' ', feature='spaces', files=x)
            numSpaces_list.append(numSpaces)

            numEmptyLines = self.get_empty_lines(files=x)
            numEmptyLines_list.append(numEmptyLines)

            whiteSpaceRatio = self.white_space_ratio(files=x)
            whiteSpaceRatio_list.append(whiteSpaceRatio)

            newLineBeforeOpenBrace = self.get_braces(files=x)
            newLineBeforeOpenBrace_list.append(newLineBeforeOpenBrace)

            self.indented_lines(files=x)
            tabsLeadLines = self.tabsLeadLines
            tabsLeadLines_list.append(tabsLeadLines)

            cppKeywords = self.get_keywords_cpp(files=x)
            cppKeywords_list.append(cppKeywords)

        master_df = pd.DataFrame(master_feature_dict)

        print((master_df))


        master_df.to_csv('output/feature_extraction.csv')





def test_module():

    run = FeatureExtractor()
    run.data_chain()

test_module()



































