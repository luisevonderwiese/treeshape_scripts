from treeshapy import TreeShape
from ete3 import Tree

t  = Tree("receptor/rd.lwr.tree")
ts = TreeShape(t, mode = "BINARY", rooted = False)

print(ts.absolute("diameter"))
