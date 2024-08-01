"""Script to run cProfile on the pypinball.main.main() function.

The script requires an output file to write the profiling data to so that it can be 
visualized using snakeviz.
"""

import argparse
import cProfile

import pypinball

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Script to run cProfile on the pypinball program"
    )
    parser.add_argument(
        "output", type=str, help="Output file to write the profile data to"
    )
    parser.add_argument(
        "main_args", nargs=argparse.REMAINDER, help="Arguments for pypinball.main"
    )
    args = parser.parse_args()

    profiler = cProfile.Profile()
    profiler.enable()
    pypinball.main.main(args.main_args)
    profiler.disable()

    profiler.dump_stats(args.output)
