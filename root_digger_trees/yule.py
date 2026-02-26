from ete3 import Tree
import random
import os

tips = 34 
trees = 100000

outdir = os.path.join("simulated_x_" + str(tips), "unrooted")
if not os.path.isdir(outdir):
    os.makedirs(outdir)

for i in range(trees):
    print(i)
    random.seed(i)
    t = Tree()
    t.add_child(name="0")
    current_tips = 1
    while current_tips < tips:
        selected_leaf = random.choice(list(t.iter_leaves()))
        selected_leaf.add_child(name=selected_leaf.name)
        selected_leaf.add_child(name=str(current_tips))
        current_tips += 1
    outpath = os.path.join(outdir, "sim_" + str(i) + ".tree")
    with open(outpath, "w+") as outfile:
        outfile.write(t.write())
