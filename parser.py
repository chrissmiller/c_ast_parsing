from __future__ import print_function
import argparse
import sys
from pycparser import c_parser, c_ast, parse_file

def buildString(path): # so  maybe we  should just keep names for  the acutal paht
    pathString = ""
    head = path[0]
    tail = path[-1]
    mpath = path[1:-1]

    pathString += leafToString(head)

    pathString += ","
    for i in range(len(mpath)):
        node = mpath[i]
        pathString += node.__class__.__name__
        if i != len(mpath) - 1:
            pathString += "|"
    pathString += ","

    pathString += leafToString(tail)
    return pathString

# Returns a leaf node's most detailed name possible
def leafToString(node):
    nname = node.__class__.__name__
    if nname == "Constant":
        return (nname + "|" + node.type)
    elif nname == "Goto":
        return (nname + "|" + node.name)
    elif nname == "ID":
        return(nname + "|" + node.name)
    elif nname == "IdentifierType":
        tname = nname
        for val in node.names:
            tname += "|" + val
        return tname
    elif nname == "Pragma":
        return (nname + "|" + node.string)
    else:
        return nname

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
        with open("test_out.txt", "w") as output:
            for path in self.final_paths:
                output.write(buildString(path) + " ")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser('Dump AST')
    argparser.add_argument('filename', help='name of file to parse')
    argparser.add_argument('--coord', help='show coordinates in the dump',
                           action='store_true')
    args = argparser.parse_args()
    ast = parse_file(args.filename, use_cpp=True)
    #ast.show(showcoord=args.coord)
    parsing = Parser()
    for child in ast.children(): # only want to parse functions
        if child[1].__class__.__name__ == "FuncDef":
            parsing.leaf_leaf_pathfinder(child[1])
    print("N paths is " + str(len(parsing.final_paths)))
    parsing.outputPathFile()
    # for path in parsing.final_paths:
    #     print("==============================================================")
    #     for i in range(len(path)):
    #         if (i == 0):
    #             print("=============================START=============================")
    #             print(path[i])
    #             print("=PATHSTART=")
    #         elif (i == len(path) - 1):
    #             print("=PATHEND=")
    #             print(path[i])
    #             print("==============================END==============================")
    #         else:
    #             print(path[i].__class__.__name__)
    #     print("==============================================================")
