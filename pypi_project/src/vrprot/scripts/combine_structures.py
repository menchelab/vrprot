# Author: Till Pascal Oblau
import glob
import shutil
import sys

from chimerax.core.commands import run


def main(directory: str, target: str):
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
            shutil.move(file, f"{directory}/{first_structure}/{filename}")


# directory = "/Users/till/Documents/UNI/Master_Bioinformatik-Universität_Wien/3.Semester/proteins/Multistru"
# target = "/Users/till/Documents/UNI/Master_Bioinformatik-Universität_Wien/3.Semester/proteins/Multistru/Combined"
# TODO: Remove in release
directory = sys.argv[1]
target = sys.argv[2]
main(directory, target)
