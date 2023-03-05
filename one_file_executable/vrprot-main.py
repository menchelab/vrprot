#! python3
import os
import sys

sys.path = [
    os.path.join(os.path.dirname(__file__), "..", "pypi_project", "src")
] + sys.path
import vrprot.util
from vrprot.alphafold_db_parser import AlphafoldDBParser
from vrprot.argument_parser import argument_parser
from vrprot.util import Logger

log = Logger("main")


def main():
    """Main function will take the arguments passed by the user and execute the program accordingly."""
    args = argument_parser().parse_args()
    parser = AlphafoldDBParser()
    if args.mode == "clear":
        parser.clear_default_dirs()
        exit()
    parser.set_batch_size(args)
    parser.set_dirs(args)
    parser.set_alphafold_version(args)
    parser.set_coloring_mode(args)
    parser.set_chimerax(args)
    parser.set_thumbnails(args)
    parser.set_gui(args)
    parser.set_only_images(args)
    log.info(f"AlphaFold Version DB: {parser.alphafold_ver}")
    if args.mode == "fetch":
        parser.execute_fetch(args.proteins[0])
    if args.mode == "local":
        parser.execute_local(args.source[0])
    if args.mode == "list":
        with open(args.file[0]) as f:
            proteins = f.read().splitlines()
        parser.execute_from_object(proteins)
    if args.mode == "bulk":
        parser.execute_from_bulk(args.source[0])


if __name__ == "__main__":
    main()
