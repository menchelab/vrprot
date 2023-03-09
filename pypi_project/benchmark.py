#! python3
from timeit import timeit
from main import main
from src.vrprot.argument_parser import argument_parser
import sys


def benchmark_local():
    arguments = []
    arguments = [
        "main.py",
        "-ow",
        "-ll",
        "INFO",
        "local",
        "./processing_files/pdbs",
    ]
    if "-pcc" in sys.argv:
        arguments = arguments[:1] + ["-pcc"] + arguments[1:]
    if "-parallel" in sys.argv or "-p" in sys.argv:
        arguments = arguments[:1] + ["-p"] + arguments[1:]
    sys.argv = arguments
    args = argument_parser().parse_args()
    main(args)


def benchmark_from_bulk():
    arguments = []
    arguments = [
        "main.py",
        "-ow",
        "-ll",
        "INFO",
        "bulk",
        "../../static/UP000000805_243232_METJA_v4_Kopie.tar",
    ]
    if "-pcc" in sys.argv:
        arguments = arguments[:1] + ["-pcc"] + arguments[1:]
    if "-parallel" in sys.argv or "-p" in sys.argv:
        arguments = arguments[:1] + ["-p"] + arguments[1:]
    sys.argv = arguments
    args = argument_parser().parse_args()
    main(args)


if __name__ == "__main__":
    func = {
        "local": benchmark_local,
        "bulk": benchmark_from_bulk,
    }
    if len(sys.argv) > 1:
        if sys.argv[1] in func:
            func = func[sys.argv[1]]
            n = 10
            runtime = timeit(func, number=n)
            print(f"{n} repetitions took", runtime, "seconds")
            print("Average time per repetition:", runtime / 10)
