import os
from ete3 import Tree



def is_bifurcating(tree):
    try: #check if already precomputed
        return tree.bifurcating
    except AttributeError:
        tree.add_feature("bifurcating", bifurcating_recursive(tree))
        return tree.bifurcating

def bifurcating_recursive(tree):
    c = tree.children
    if len(c) == 2:
        return bifurcating_recursive(c[0]) and bifurcating_recursive(c[1])
    if len(c) == 0:
        return True
    return False


in_dir = "data/grove/trees/unrooted"
out_dir = "data/grove_modificated/trees/unrooted"

if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

for name in os.listdir(in_dir):
    src = os.path.join(in_dir, name)
    try:
        t = Tree(src)
    except Exception as e:
        print(e)
        continue
    if not is_bifurcating(t):
        t.resolve_polytomy()
        t.write(outfile = os.path.join(out_dir, name), format = 5)
