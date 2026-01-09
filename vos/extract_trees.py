import os
from ete3 import Tree

indir = "../data/vos"
superoutdir = "../data/vos/trees"
primate_tree_path = "../data/vos/supertree1.dnd"

def parse_subgroups(path):
    with open(path, "r") as infile:
        lines = infile.readlines()
    start_index = -1
    for i, line in enumerate(lines):
        if line.startswith("Primate"):
            start_index = i
            break
    subgroups = lines[start_index][:-1].split("\t")[1:]
    matrix = {subgroup : [] for subgroup in subgroups}
    for j in range(start_index+1, len(lines) - 1):
        line = lines[j]
        parts = line.split(",\t")
        primate = parts[0]
        bits = parts[1][:-1].split("\t")
        if len(bits) != len(subgroups):
            print(bits)
            print(subgroups)
            print("error")
            assert(False)
        for k, subgroup in enumerate(subgroups):
            if bits[k] == "1":
                matrix[subgroup].append(primate)
            else:
                assert(bits[k] == "0")
    return matrix


def subtrees(continent):
    inpath = os.path.join(indir, "42040" + continent.lower(), "42040" + continent + ".txt")
    outdir = os.path.join(superoutdir, continent.lower())
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    subgroups = parse_subgroups(inpath)
    tips = [leaf.name for leaf in Tree(primate_tree_path).iter_leaves()]
    missing_taxa = set()
    for name, subgroup in subgroups.items():
        tree = Tree(primate_tree_path)
        missing_taxa.update([el for el in subgroup if el not in tips])
        subgroup = [el for el in subgroup if el in tips]
        tree.prune(subgroup)
        outpath = os.path.join(outdir, name + ".tree")
        tree.write(format=1, outfile=outpath)
    print(missing_taxa)


subtrees("Africa")
subtrees("SouthAmerica")
