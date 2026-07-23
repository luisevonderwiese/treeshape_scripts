import os
import pandas as pd
from ete3 import Tree


def run_rd(msa_path, tree_path, prefix):
    command = "./rd --exhaustive "
    command += " --msa " + msa_path
    command += " --tree " + tree_path
    command += " --prefix " + prefix
    command += " --threads 8"
    command += " > " + prefix + ".rdlog"
    os.system(command)

def evaluate_lwrs(lwr_tree_path):
    t = Tree(lwr_tree_path)
    lwrs = {node.LWR : node for node in t.iter_descendants()}
    lwrs = dict(sorted(lwrs.items(), reverse = True))
    if len(lwrs) < 2:
        return float("nan"), float("nan"), float("nan")
    lwr_max = list(lwrs.items())[0]
    lwr_max_2 = list(lwrs.items())[1]
    n1 = lwr_max[1]
    n2 = lwr_max_2[1]
    d = n1.get_distance(n2, topology_only=True)
    return lwr_max[0], lwr_max_2[0], d



base_dir = "../../../hoehledi/example_workflow/run_sparta/out/tb_mirror"

res_dir = "rd_evaluations"
if not os.path.isdir(res_dir):
    os.makedirs(res_dir)

res_table = []
for dir_name in os.listdir(base_dir):
    msa_path = os.path.join(base_dir, dir_name, "msa.fasta")
    if not os.path.isfile(msa_path):
        continue
    with open(msa_path, "r") as infile:
        s = infile.read()
    n = s.count(">")
    if n > 35 or n < 4:
        continue
    name = dir_name.split(".")[0]
    print("Running rd for", name, "size", str(n))
    cur_res_dir = os.path.join(res_dir, name)
    if not os.path.isdir(cur_res_dir):
        os.makedirs(cur_res_dir)
    prefix = os.path.join(cur_res_dir, "rd")
    lwr_tree_path = prefix + ".lwr.tree"
    if not os.path.isfile(lwr_tree_path):
        tree_path = os.path.join(base_dir, dir_name, "gtr_g_i.raxml.bestTree")
        #run_rd(msa_path, tree_path, prefix)
    if not os.path.isfile(lwr_tree_path):
        print("no lwr tree")
        continue
    lwr_max, lwr_max_2, d  = evaluate_lwrs(lwr_tree_path)
    res_table.append([name, lwr_max, lwr_max_2, d])

df = pd.DataFrame(res_table, columns = ["dataset", "lwr_max", "lwr_max_2", "d"])
df.to_csv("results.csv")
