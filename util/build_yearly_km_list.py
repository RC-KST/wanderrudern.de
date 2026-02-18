#!/usr/bin/env python3

import typing
import functools as ft
import os
import sys
import csv
from dataclasses import dataclass
import arbitration

def main():

    cli = parseCli()

    try: os.mkdir(cli.output_directory)
    except: pass

    c_name = cli.name_column

    for filepath in cli.input_files:
        with open(filepath) as f:
            print(f"file: {filepath}")
            csvr = csv.reader(f, delimiter="|")
            header = next(csvr)
            rows = list(csvr)
            print("rows", rows)

        is_with_comma = ',' in rows[0][c_name]
        print(f"is with comma: {is_with_comma}")
        def map_fn(c: list[str]) -> list[str]:
            if is_with_comma:
                c[c_name] = "Giese, Astrid" if c[c_name] == "A.G." else c[c_name]
            else:
                c[c_name] = "Astrid Giese" if c[c_name] == "A.G." else c[c_name]

            return c
        rows = list(map(map_fn, rows))
        
        # Splitting
        if is_with_comma:
            names_splitted = list(map(lambda row: row[c_name].split(',', 1), rows))
            for i in range(len(names_splitted)):
                if len(names_splitted[i]) != 2:
                    print("[comma]======>>>", names_splitted[i])
                if len(names_splitted[i]) < 2: names_splitted[i] = [names_splitted[i][0], ""]
            names_splitted = list(map(lambda c: (c[1].strip(), c[0].strip()), names_splitted))
            print("comma names", names_splitted)
        else:
            names_splitted = list(map(lambda row: row[c_name].split(' ', 1), rows))
            print("first split", list(names_splitted))
            for i in range(len(names_splitted)):
                if len(names_splitted[i]) != 2:
                    print("[space]======>>>", names_splitted[i])
                if len(names_splitted[i]) < 2: names_splitted[i] = [names_splitted[i][0], ""]
            names_splitted = list(map(lambda c: (c[0].strip(), c[1].strip()), names_splitted))
            print("space names", names_splitted)

        #names_splitted = list(map(lambda c: (c[1].strip(), c[0].strip()), names_splitted))
        

        arb = arbitration.ArbitrationState(iter(names_splitted))
        arb.compute_shorthands()
        for i, _ in enumerate(rows):
            name_short = arb.lookup(names_splitted[i])
            rows[i][c_name] = name_short
        

        try: os.mkdir(cli.output_directory)
        except: pass

        output_path = os.path.join(cli.output_directory, os.path.basename(filepath))
        with open(output_path, "w") as f:
            csvw = csv.writer(f, delimiter="|")
            csvw.writerow(header)
            csvw.writerows(rows)



@dataclass
class Cli:
    input_files: list[str]
    output_directory: str
    name_column: int


def helpExit(msg: str|None = None, exit_code: int = 1) -> typing.NoReturn:
    exe_name = "build_yearly_km_list.py"
    if msg is not None: print(msg + "\n\n")
    print(f"USAGE: {exe_name} OPTIONS <INPUT_FILE ...>")
    print(f"")
    print(f"OPTIONS:")
    print(f" -h, --help                 print this and exit")
    print(f" -n, --name-column          specify on which column the name is positioned start at index 0, default is 1")
    #print(f" -r, --name-order           specify ")
    print(f" -o, --output-dir           specify output folder")
    sys.exit(exit_code)

def parseCli() -> Cli:
    input_files: list[str] = []
    output_dir: str | None = None
    name_column: int | None = None


    va = iter(sys.argv)
    next(va, None)
    carg = next(va, None)
    while (carg != None):
        print(f"carg: '{carg}'")
        if carg == "-h" or carg == "--help": helpExit(exit_code=0)
        elif carg == "-o" or carg == "--output-dir":
            if output_dir is not None: helpExit("Only one output directory may be specified")
            carg = next(va, None)
            if (carg is None): helpExit("Expected output directory path")
            output_dir = carg
        elif carg == "-n" or carg == "--name-column":
            if name_column is not None:  helpExit("--name-column may only be specified once")
            col = next(va, None)
            if col is None: helpExit("--name-column expects an integer that represents the name column index, starting at 0")
            name_column = int(col)
        else: 
            if (carg.startswith("-")): helpExit(f"Unknown option {carg}")
            print("Positional: ", carg)
            input_file = carg
            input_files.append(input_file)
        carg = next(va, None)

    if len(input_files) == 0:
        helpExit("At least one input file has to be given")
    if name_column is None: name_column = 1

    return Cli(
        input_files=input_files,
        output_directory=(output_dir if output_dir is not None else helpExit("output directory has to be specified")),
        name_column=name_column
    )


if __name__ == "__main__":
    main()

