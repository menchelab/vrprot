# Author: Till Pascal Oblau
# To Run this script, use the following command:
# chimerax --script '"combine_structures.py" "<directory where the pdbs files are located>" "<directory where the combined structures should be saved>"'

import ast
import glob
import os
import shutil
import sys

from chimerax.core.commands import run


def main(directory: str, target: str, subprocess: bool):
    """Script used to combine multiple structure fractions into one single structure. Processing is not applied as this will lead to a memory overflow.

    Args:
        directory (str): Directory that contains all PDB files from the bulk download.
        target (str): Directory where the combined structures should be saved.
    """
    all_files = glob.glob(f"{directory}/*.pdb")
    while len(all_files) > 1:
        first_structure = all_files[0].split("/")[-1]
        first_structure = first_structure.split("-")[1]
        structures = []
        for file in all_files:
            tmp = file.split("/")[-1]
            tmp = tmp.split("-")[1]
            if tmp == first_structure:
                structures.append(file)
        if len(structures) == 1:
            all_files.remove(structures[0])
            continue
        for file in structures:
            run(session, f"open {file}")
            run(session, f"echo HELLO")
        run(session, f"save {target}/AF-{first_structure}-F1.glb")
        run(session, "close")
        for file in structures:
            all_files.remove(file)
            filename = file.split("/")[-1]
            os.makedirs(f"{directory}/{first_structure}", exist_ok=True)
            shutil.move(file, f"{directory}/{first_structure}/{filename}")
    if subprocess:
        run(session, "exit")


# directory = "/Users/till/Documents/UNI/Master_Bioinformatik-Universität_Wien/3.Semester/proteins/Multistru"
# target = "/Users/till/Documents/UNI/Master_Bioinformatik-Universität_Wien/3.Semester/proteins/Multistru/Combined"
# TODO: Remove in release
subprocess = False
directory = sys.argv[1]
target = sys.argv[2]
if len(sys.argv) >= 4:
    subprocess = ast.literal_eval(sys.argv[3])
run(session, f"echo {subprocess}")
main(directory, target, subprocess)
