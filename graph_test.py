
class pNode: # Shell structure to hold a pycparser node and its parent node
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
class cNode: # Shell structure to hold a datapoint and its children
    def __init__(self, node):
        self.node = node
        self.children = []


#stack children then parnets

# Make a tree
one = cNode(1)

two = cNode(2)
three = cNode(3)
four = cNode(4)

one.children = [two, three, four]

five = cNode(5)
six = cNode(6)

two.children = [five, six]

seven = cNode(7)

three.children.append(seven)

eight = cNode(8)

seven.children.append(eight)

nine = cNode(9)
ten = cNode(10)

eight.children = [nine, ten]

eleven = cNode(11)

ten.children.append(eleven)

onep = pNode(one, None)


nodestack = []
nodestack.append(onep)
firstChild = None
lastLeaf = None
vis = 0
while nodestack:
    current = nodestack.pop()
    children = current.node.children
    vis += 1 # track num nodes
    if children:
        for child in children:
            pChild = pNode(child, current)
            nodestack.append(pChild)
    elif firstChild is None:
        firstChild = current
        lastLeaf = current
    else:
        lastLeaf = current
print("Firstchild is " + str(firstChild.node.node))
print("Lastleaf is " + str(lastLeaf.node.node))

master_path = []
leaf_ivals = []
visited = set()
path_creation = []
path_creation.append(firstChild)
while False:
    current = path_creation.pop()
    children = current.node.children
    vis += 1
    master_path.append(current.node.node)
    if current.node.node not in visited:
        visited.add(current.node.node)
        if children:
            for child in children:
                pChild = pNode(child, current)
                path_creation.append(pChild)

        if current.parent:
            path_creation.append(current.parent)

master_path = []
leaf_ivals = []
curr_ival = -1
cVisited = set()
lvis = 0
current = firstChild
print("Vis is  " + str(vis))
master_path.append(current.node.node)
while len(cVisited) != vis - 2:
    next = None
    for child in current.node.children:
        if child not in cVisited:
            pChild = pNode(child, current)
            next = pChild
            cVisited.add(child)
            break

    if not next:
        next = current.parent
        if not next:
            print(master_path)
            print("Welp")
    current = next
    master_path.append(current.node.node)

print(master_path)



#for leaf in self.leaf_ivals: # add copy of all lists to master leaf-leaf path set
#    self.pathlist.append(self.master_path[leaf:])
#self.leaf_ivals.append(self.ival)
#no scenario where we have perviously visited a child and want to visit it again
