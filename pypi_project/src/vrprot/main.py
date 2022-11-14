#! python3

from .alphafold_db_parser import AlphafoldDBParser
from .argument_parser import argument_parser
from .util import Logger

log = Logger("main")


def main():
    """Main function will take the arguments passed by the user and execute the program accordingly."""
    args = argument_parser().parse_args()
    parser = AlphafoldDBParser()
    log.info(f"Alphafold_Version:   {parser.alphafold_ver}")
    if args.mode == "clear":
        parser.clear_default_dirs()
        exit()
    parser.set_batch_size(args)
    parser.set_dirs(args)
    parser.set_alphafold_version(args)
    parser.set_coloring_mode(args)
    parser.set_chimerax(args)
    if args.mode == "fetch":
        parser.execute_fetch(args.proteins[0])
    if args.mode == "local":
        parser.execute_local(args.source[0])
    if args.mode == "list":
        with open(args.file[0]) as f:
            proteins = f.read().splitlines()
        parser.execute_from_object(proteins)


if __name__ == "__main__":
    main()
