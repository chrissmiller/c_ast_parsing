from __future__ import print_function
import argparse
import sys
import regex
import re
from os import system
from pycparser import c_parser, c_ast, parse_file

def buildString(path): # so  maybe we  should just keep names for  the acutal paht
    short_name = {"ArrayDecl":"AD", "ArrayRef":"AR", "Assignment":"A", "BinaryOp": "BO", "Break":"B", \
    "Case": "C", "Cast": "Ca", "Compound":"Co", "CompoundLiteral":"CL", "Constant":"Cn", \
    "Continue":"Ct", "Decl":"D", "DeclList":"DL", "Default":"De", "DoWhile": "DW", \
    "EllipsisParam":"EP", "EmptyStatement":"ES", "Enum":"E", "Enumerator":"En", \
    "ExprList":"EL", "FileAST":"FA", "For":"F", "FuncCall": "FC", "FuncDecl":"FL", \
    "FuncDef":"FD", "Goto": "G", "ID":"ID", "IdentifierType":"IT", "If":"I", \
    "InitList":"IL", "Label":"L", "NamedInitializer":"N", "ParamList":"PL", "PtrDecl":"PD", \
    "Return":"R", "Struct":"S", "StructRef":"SR", "Switch":"Sw", "TernaryOp":"TO", \
    "TypeDecl":"TD", "Typedef":"T", "Typename":"Tn", "UnaryOp":"UO", "Union":"U", \
    "While":"W", "Pragma":"P"}

    pathString = ""
    head = path[0]
    tail = path[-1]
    mpath = path[1:-1]

    pathString += leafToString(head)

    pathString += ","
    for i in range(len(mpath)):
        node = mpath[i]
        pathString += short_name[node.__class__.__name__]
        if i != len(mpath) - 1:
            pathString += "|"
    pathString += ","

    pathString += leafToString(tail)
    return pathString


# Returns a leaf node's most detailed name possible
def leafToString(node):
    short_name = {"ArrayDecl":"AD", "ArrayRef":"AR", "Assignment":"A", "BinaryOp": "BO", "Break":"B", \
    "Case": "C", "Cast": "Ca", "Compound":"Co", "CompoundLiteral":"CL", "Constant":"Cn", \
    "Continue":"Ct", "Decl":"D", "DeclList":"DL", "Default":"De", "DoWhile": "DW", \
    "EllipsisParam":"EP", "EmptyStatement":"ES", "Enum":"E", "Enumerator":"En", \
    "ExprList":"EL", "FileAST":"FA", "For":"F", "FuncCall": "FC", "FuncDecl":"FL", \
    "FuncDef":"FD", "Goto": "G", "ID":"ID", "IdentifierType":"IT", "If":"I", \
    "InitList":"IL", "Label":"L", "NamedInitializer":"N", "ParamList":"PL", "PtrDecl":"PD", \
    "Return":"R", "Struct":"S", "StructRef":"SR", "Switch":"Sw", "TernaryOp":"TO", \
    "TypeDecl":"TD", "Typedef":"T", "Typename":"Tn", "UnaryOp":"UO", "Union":"U", \
    "While":"W", "Pragma":"P"}

    nname = node.__class__.__name__
    if nname == "Constant":
        return (short_name[nname] + "|" + node.type + "|" + splitString(node.value))
    elif nname == "Goto":
        return (short_name[nname] + "|" + splitString(node.name))

    elif nname == "ID":
        return(short_name[nname] + "|" + splitString(node.name))
    elif nname == "IdentifierType":
        tname = short_name[nname]
        for val in node.names:
            tname += "|" + val
        return tname
    elif nname == "Pragma":
        return (short_name[nname] + "|" + splitString(node.string))
    else:
        return nname

def splitString(value):
    try:
        float(value)
        return value
    except:
        value = value.strip()
        cstring = ""
        splitval = regex.split("(?<=[a-z])(?=[A-Z])|_|[0-9]|(?<=[A-Z])(?=[A-Z][a-z])|\\s+", value, flags=regex.VERSION1)
        length = len(splitval)
        for i in range(length - 1):
            cstring += splitval[i] + "|"
        cstring += splitval[length-1]
        return cstring


class pNode: # Shell structure to hold a pycparser node and its parent node
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent

class Parser:
    def __init__(self):
        self.master_path = []

        self.final_paths = []
        self.pathlist = []

        self.ival = -1
        self.leaf_ivals = []


    #
    def leaf_leaf_pathfinder(self, start_node):
        nodestack = []
        start_node_p = pNode(start_node, None)
        nodestack.append(start_node_p)
        self.master_path = []
        self.vis = 0
        self.leaf_ivals = []
        firstLeaf = None

        # Traverse once, add parents to all nodes and ID first leaf
        while nodestack:
            current = nodestack.pop()
            self.vis += 1
            children = current.node.children()

            if children:
                for child in children:
                    pChild = pNode(child[1], current)
                    nodestack.append(pChild)
            elif firstLeaf is None:
                firstLeaf = current

        cVisited = [] # change back to set? hashability issue
        current = firstLeaf
        self.master_path.append(firstLeaf.node)
        cVisited.append(firstLeaf.node)
        self.ival = -1
        while len(cVisited) != self.vis - 2:
            next = None
            self.ival += 1
            children = current.node.children()
            if children:
                for child in children:
                    if child[1] not in cVisited:
                        pChild = pNode(child[1], current)
                        next = pChild
                        cVisited.append(child[1])
                        break
            else:
                for leaf in self.leaf_ivals:
                    self.pathlist.append(self.master_path[leaf:])
                self.leaf_ivals.append(self.ival)

            if not next:
                next = current.parent
                if not next:
                    print("Error tracking:")
                    print(" len(cVisited) = " + str(len(cVisited)))
                    print(" vis = " + str(self.vis))
                    print(" reached head node with no available children.")
                    with open("parser.log", "w") as logfile:
                        logfile.write("Master Path:\n")
                        for item in self.master_path:
                            logfile.write(str(item.__class__.__name__) + "\n")

            current = next
            self.master_path.append(current.node)



        for path in self.pathlist:
            new_path = []
            for i in range(1, len(path)-1): # ignore start/end leaves
                if path[i] not in new_path and path[i].children(): # not duplicate or leaf
                    new_path.append(path[i])
            if new_path:
                new_path.insert(0, path[0])
                new_path.append(path[-1])
                self.final_paths.append(new_path)



    def outputPathFile(self):
        with open("main_out.txt", "a") as output:
            for path in self.final_paths:
                output.write(buildString(path) + " ")
            output.write("\n")


if __name__ == "__main__":

    argparser = argparse.ArgumentParser('Dump AST')
    argparser.add_argument('dirname', help='name of directory to parse')
    argparser.add_argument('--coord', help='show coordinates in the dump',
                           action='store_true')
    args = argparser.parse_args()
    dir = args.dirname
    filename_file = "ast_finames.txt"
    cmd = "cd " + dir
    system(cmd)
    cmd = "ls > " + filename_file
    system(cmd)
    with open(filename_file, "r") as finames_file:
        finames = finames_file.readlines()

    for filename in finames:
        filename = filename.rstrip()
        if not re.fullmatch(".*\.i", filename):
            continue
        ast = parse_file(filename, use_cpp=False)

        parsing = Parser()
        for child in ast.children(): # only want to parse functions
            if child[1].__class__.__name__ == "FuncDef":
                parsing.leaf_leaf_pathfinder(child[1])
        parsing.outputPathFile()
