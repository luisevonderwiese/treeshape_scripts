import os
import shutil
import pandas as pd
import util
from ete3 import Tree

base_dir = "../data/grove_modificated/"
treeshapy_dir = os.path.join(base_dir, "treeshapy")
clean_dir = os.path.join(base_dir, "treeshapy_clean")
if not os.path.isdir(clean_dir):
    os.makedirs(clean_dir)

copy = 0
clean = 0
error = 0
error1 = 0
error2 = 0

for tree_name in util.unrooted_tree_names(base_dir):
    #print(tree_name)
    file_names = [tree_name + ending for ending in ["_absolute.tsv", "_relative_max.tsv", "_relative_tips.tsv", "_relative_yule.tsv", "_times.tsv"]]
    try:
        t = Tree(os.path.join(base_dir, "trees/unrooted/", tree_name + ".newick"))
    except:
        error1 += 1
        continue
    if len(t.children) == 3:
        copy += 1
        print(tree_name)
        for fn in file_names:
            shutil.copy(os.path.join(treeshapy_dir, fn), os.path.join(clean_dir, fn))
        continue
    if not len(t.children) == 2:
        error += 1
        continue
    clean += 1
    print(tree_name)
    for fn in file_names:
        #if os.path.isfile(os.path.join(clean_dir, fn)):
        #    print(fn, "already clean")
        #    continue
        if not os.path.isfile(os.path.join(treeshapy_dir, fn)):
            continue
        df = pd.read_csv(os.path.join(treeshapy_dir, fn), sep = "\t")
        if len(df) == 0:
            print(fn, "empty")
            continue
        l = len(df)
        df = df[df["root"] != "0"]
        if l - len(df) != 1:
            print(fn, "not matching")
            error2 += 1
            continue
        df.to_csv(os.path.join(clean_dir, fn), sep = "\t")
        #print(fn, "cleaned")

print("copy:", str(copy), "clean:", str(clean), "error:", str(error), "error1:", str(error1), "error2:", str(error2))
