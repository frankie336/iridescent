"""
Experimental parsing with PyClang
Needs some clean up, but ok for now
https://www.programcreek.com/python/example/111613/clang.cindex.CursorKind.VAR_DECL
https://stackoverflow.com/questions/37194718/find-all-references-of-specific-function-declaration-in-libclang-python


The average number of parameters among
all functions
"""
from clang.cindex import *


def is_function_call(funcdecl, c):
    """ Determine where a call-expression cursor refers to a particular function declaration
    """
    defn = c.get_definition()
    return (defn is not None) and (defn == funcdecl)

def fully_qualified(c):
    """ Retrieve a fully qualified function name (with namespaces)
    """
    res = c.spelling
    c = c.semantic_parent
    while c.kind != CursorKind.TRANSLATION_UNIT:
        res = c.spelling + '::' + res
        c = c.semantic_parent
    return res








def find_funcs_and_calls(tu):
    """ Retrieve lists of function declarations and call expressions in a translation unit
    """
    filename = tu.cursor.spelling
    calls = []
    funcs = []
    paras = []

    for c in tu.cursor.walk_preorder():
        if c.location.file is None:
            pass
        elif c.location.file.name != filename:
            pass
        elif c.kind == CursorKind.CALL_EXPR:
            calls.append(c)
        elif c.kind == CursorKind.FUNCTION_DECL:
            funcs.append(c)

        elif c.kind == CursorKind.PARM_DECL:
            paras.append(c)


    return funcs, calls,paras



def get_funcs(files: str) ->str:

    all_funcs, all_paras = [],[]


    idx = Index.create()
    args =  '-x c++ --std=c++11'.split()
    tu = idx.parse(files, args=args)
    funcs, calls,paras = find_funcs_and_calls(tu)
    for f in funcs:
        print(fully_qualified(f), f.location)
        all_funcs.append(f)
        for c in calls:
            if is_function_call(f, c):
                print('-', c)

        for p in paras:
            #all_paras.append(p)
            print(fully_qualified(p))
            all_paras.append(p)

    funcs_len = len(all_funcs)

    paras_len = len(all_paras)

    print(funcs_len,paras_len)

    if funcs_len ==0:
        feature_paras = 0
        paras_len = 0
        funcs_len = 0

        return feature_paras, paras_len,funcs_len
    feature_paras = paras_len/funcs_len


    return feature_paras,paras_len,funcs_len


#get_funcs(files='corpus/LTIME110A/noimi/TREERET/LTIME110A_noimi_TREERET.cpp')




