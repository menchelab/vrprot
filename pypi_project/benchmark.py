#! python3
from main import main
from src.vrprot.argument_parser import argument_parser
import sys
from timeit import timeit


def benchmark_local():
    pcc = False
    if "-pcc" in sys.argv:
        pcc = True
    sys.argv = [
        "main.py",
        "-ow",
        "-ll",
        "INFO",
        "local",
        "./processing_files/pdbs",
    ]
    if pcc:
        sys.argv = ["-pcc"] + sys.argv
    args = argument_parser().parse_args()
    main(args)


if __name__ == "__main__":
    if sys.argv[1] == "local":
        n = 5
        runtime = timeit(benchmark_local, number=n)
        print(f"{n} repetitions took", runtime, "seconds")
        print("Average time per repetition:", runtime / n)

    # sequential 50 runs:
