#!/usr/bin/env python3

from dataclasses import dataclass
import typing as tp
import os
import sys

def main():
    cli = parse_cli()

    for fpath in cli.input_files:
        with open(fpath, "w") as f:
            pass
            #f.write()


@dataclass
class Cli():
    output_dir: str
    input_files: list[str]

def parse_cli() -> Cli:
    def printHelpExit(msg: str|None = None, exit_code: int = 1) -> tp.NoReturn:
        exe_name = "transform_km_list.py"
        if msg is not None:
            print(msg + "\n\n")
        print(f"Usage: {exe_name} OPTIONS <INPUT FILEs...> ")
        print(f"")
        print(f"OPTIONS:")
        print(f" -h, --help                 Print this help and exit")
        print(f" -o, --output-dir           output directory")
        sys.exit(exit_code)

    output_dir: str|None = None
    input_files: list[str] = []

    av = iter(sys.argv)
    next(av)
    carg = next(av)
    while carg is not None:
        if carg == "-h" or carg == "--help":
            printHelpExit(exit_code=0)
        elif carg == "-o" or carg == "--output-dir":
            carg = next(av)
            if (carg is None): printHelpExit("Expected directory name")


        carg = next(av)
        
    return Cli(
        input_files = input_files if len(input_files) != 0 else printHelpExit("At least one input file has to be given"),
        output_dir = output_dir if output_dir is not None else printHelpExit("Output directory has to be specified"),
    )


if __name__ == "__main__":
    main()
