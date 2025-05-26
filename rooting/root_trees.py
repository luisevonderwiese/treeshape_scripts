import os
import shutil


def run_root_digger(msa_path, tree_path, prefix):
    command = "./../bin/rd"
    command += " --msa " + msa_path
    command += " --tree " + tree_path
    command += " --prefix " + prefix
    command += " --threads auto"
    print(command)
    os.system(command)


def root_trees(base_dir):
    msa_dir = os.path.join(base_dir, "msa")
    results_dir = os.path.join(base_dir, "results")
    unrooted_trees_dir = os.path.join(base_dir, "trees/unrooted")
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")
    rd_dir = os.path.join(results_dir, "rd")
    for d in [rooted_trees_dir, rd_dir]:
        if not os.path.isdir(d):
            os.makedirs(d)

    for tree_name in os.listdir(unrooted_trees_dir):
        tree_name_x = ".".join(tree_name.split(".")[:-1])
        rooted_tree_path = os.path.join(rooted_trees_dir, tree_name_x + ".rooted.tree")
        if os.path.isfile(rooted_tree_path):
            continue
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        msa_path = os.path.join(msa_dir, tree_name_x + ".fasta") 
        prefix = os.path.join(rd_dir, tree_name_x)
        run_root_digger(msa_path, unrooted_tree_path, prefix)
        try:
            shutil.copyfile(prefix + ".rooted.tree", rooted_tree_path)
        except:
            print(msa_path)


root_trees("../data/evonaps_dna")
