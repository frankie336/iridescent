import abc
import clang.cindex



file = 'corpus/JULY10/gennady.korotkevich/LCM/JULY10_gennady.korotkevich_LCM.cpp'
index = clang.cindex.Index.create()
tu = index.parse(file)




class ClangWorksInterface(metaclass=abc.ABCMeta):
    """Formal Interface"""
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'traverse') and
                callable(subclass.traverse) and

                hasattr(subclass, 'get_nodes_cpp') and
                callable(subclass.get_nodes_cpp) or



                NotImplemented)

    @abc.abstractmethod
    def traverse(self):
        """
        Branching factor of the tree formed by con-
        verting code blocks of files into nodes

        The average branching factor can be quickly
        calculated as the number of non-root nodes
        (the size of the tree, minus one; or the number
        of edges) divided by the number of non-leaf nodes
        (the number of nodes with children).
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_nodes_cpp(self,files: str) ->str:
        """

        Get all nodes in a cpp AST
        """
        raise NotImplemented




class ClangWorks(ClangWorksInterface):
    def __init__(self):

        self.function_calls_list = []
        self.function_declarations_list = []
        self.nodes_list = []


    def traverse(self,node):
        """
        Branching factor of the tree formed by con-
        verting code blocks of files into nodes

        The average branching factor can be quickly
        calculated as the number of non-root nodes
        (the size of the tree, minus one; or the number
        of edges) divided by the number of non-leaf nodes
        (the number of nodes with children).
        """
        for child in node.get_children():
            self.traverse(child)
            self.nodes_list.append(child.spelling)

        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            self.function_calls_list.append(node.spelling)

        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            self.function_declarations_list.append(node.spelling)

        print ('Found %s [line=%s, col=%s]' % (node.displayname, node.location.line, node.location.column))




    def get_nodes_cpp(self,files: str) ->str:
        """

        Get all nodes in a cpp AST
        """
        index = clang.cindex.Index.create()
        tu = index.parse(files)
        root = tu.cursor
        self.traverse(root)

        print(self.nodes_list)

        nodes_list = [x for x in self.nodes_list if x]
        print(nodes_list)










def test_module():
    run = ClangWorks()
    run.get_nodes_cpp(files=file)

test_module()

