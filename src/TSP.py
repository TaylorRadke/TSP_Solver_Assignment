import sys
import os.path as path
from reader import reader
from solver import greedy2opt
import matplotlib.pyplot as plt
from output import output


def main(file_name,allowed_time):
    tsp_node_dict = reader(path.join(path.curdir,'tsp_files',file_name))
    greedy2opt(tsp_node_dict, allowed_time)
    output(tsp_node_dict)


if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
