# Author: Till Pascal Oblau
# To Run this script, use the following command:
# chimerax --script '"combine_structures.py" "<directory where the pdbs files are located>" "<directory where the combined structures should be saved>"'

import ast
import glob
import os
import shutil
import sys
import argparse
import re

SCRIPTS = os.path.dirname(os.path.realpath(__file__))
sys.path.append(SCRIPTS)
import chimerax_bundle

from chimerax.core.commands import run


def main(
    directory: str,
    target: str,
    subprocess: bool,
    processing: str,
    color: list,
    overwrite: bool,
    proteins: list,
    image=False,
):
    """Script used to combine multiple structure fractions into one single structure. Processing is not applied as this will lead to a memory overflow.

    Args:
        directory (str): Directory that contains all PDB files from the bulk download.
        target (str): Directory where the combined structures should be saved.
        subprocess (bool): If the script is called inside the chimerax command line, this will be set to False. This will prevent the script from exiting the ChimeraX session.
    """
    os.makedirs(target, exist_ok=True)
    pattern = re.compile("|".join(proteins))
    all_files = [
        file for file in glob.glob(f"{directory}/*.pdb") if pattern.search(file)
    ]
    bundle = chimerax_bundle.Bundle(session, directory, target)
    bundle.apply_processing(processing, color)
    prefix = "mf"
    while len(all_files) > 1:
        file = all_files.pop()
        first_structure = os.path.basename(file)
        ver = re.findall(r"_v(\d+)\.pdb", first_structure)[0]
        protein = re.findall(r"AF-(\w+)-", first_structure)[0]
        pattern = re.compile(protein)
        fractions = [f for f in all_files if pattern.search(f)]

        # Single fraction
        if len(fractions) == 1:
            continue

        output = f"{target}/{prefix}_AF-{protein}-F1-model_v{ver}.glb"
        # Output already exists and overwrite is False. Remove all files from the processing list
        if os.path.exists(output) and not overwrite:
            for file in fractions:
                all_files.remove(file)
            continue

        # Run bundle command on all files
        files = [os.path.basename(file) for file in fractions]
        tmp_names = ["tmp_" + file for file in files]
        bundle.run(files, tmp_names)

        # Open and save file for first structure
        for file in tmp_names:
            run(session, f'open {target}/{file.replace("pdb","glb")}')
        run(session, f"save {output}")

        # Remove all other files for this structure
        for file in tmp_names:
            os.remove(f"{target}/{file.replace('pdb','glb')}")

        # Close session and remove processed files from all_files
        run(session, "close")
        for file in fractions:
            all_files.remove(file)
            # os.makedirs(f"{directory}/{first_structure}", exist_ok=True)
            # shutil.move(file, f"{directory}/{first_structure}/{filename}")
    if subprocess:
        run(session, "exit")


if __name__ == "ChimeraX_sandbox_1":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        help="Directory that contains all PDB files from the bulk download.",
    )
    parser.add_argument(
        "target", help="Directory where the combined structures should be saved."
    )
    parser.add_argument(
        "--subprocess",
        "-sp",
        help="If this is set ChimeraX will close after all structures are done.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--processing_mode",
        "-mode",
        help="The processing mode that should be applied to the structures.",
        default="cartoons_ss_coloring",
    )
    parser.add_argument(
        "--overwrite",
        "-ow",
        help="If this is set, the script will overwrite existing files.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--proteins",
        "-p",
        help="The proteins that should be processed.",
        type=str,
    )
    # parser.add_argument("--colors","-c", help="The coloring that should be applied to the structures.", default=['red','green','blue'],nargs=3,type=str)
    args = parser.parse_args()
    directory = args.directory
    target = args.target
    subprocess = args.subprocess
    processing = args.processing_mode
    overwrite = args.overwrite
    proteins = args.proteins.split(",")
    # color = ast.literal_eval(args.colors)
    color = ["red", "green", "blue"]
    run(session, f"echo {subprocess}")
    main(directory, target, subprocess, processing, color, overwrite, proteins)
