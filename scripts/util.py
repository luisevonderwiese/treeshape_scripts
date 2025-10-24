import os
import matplotlib.pyplot as plt

def unrooted_tree_names(base_dir):
    return [tree_name.split(".")[0] for tree_name in os.listdir(os.path.join(base_dir, "trees/unrooted"))]


def add_fancy_legend():
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)

