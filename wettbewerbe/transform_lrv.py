#!/usr/bin/env python3
import typing
from dataclasses import dataclass
from typing import Iterable
import functools as ft
import csv
import os
import sys
import arbitration

#files = [
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2004.csv", 2004),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2005.csv", 2005),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2006.csv", 2006),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2007.csv", 2007),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2008.csv", 2008),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2009.csv", 2009),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2010.csv", 2010),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2011.csv", 2011),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2012.csv", 2012),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2013.csv", 2013),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2014.csv", 2014),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2015.csv", 2015),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2016.csv", 2016),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2017.csv", 2017),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2018.csv", 2018),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2019.csv", 2019),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2020.csv", 2020),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2021.csv", 2021),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2022.csv", 2022),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2023.csv", 2023),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2024.csv", 2024),
#    ("./lrv_brandenburg_exp/Brandenburg_Kilometer_2025.csv", 2025),
#]
#LRV_DIR =  "lrv_gen"

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

GROUPS_LIST = [ "M1", "W1", "M2", "W2", "M3", "W3", "M4", "W4", "M5", "W5", "M6", "W6", "M7", "W7" ]
GROUPS = {
    "M1": { "min": 0, "max": 14,  "min_km": 500 },            
    "W1": { "min": 0, "max": 14,  "min_km": 500 },
    "M2": { "min": 15, "max": 18, "min_km": 800 },             
    "W2": { "min": 15, "max": 18, "min_km": 800 },
    "M3": { "min": 19, "max": 31, "min_km": 800 },         
    "W3": { "min": 19, "max": 31, "min_km": 800 },
    "M4": { "min": 32, "max": 39, "min_km": 700 },             
    "W4": { "min": 32, "max": 39, "min_km": 700 },
    "M5": { "min": 40, "max": 49, "min_km": 700 },             
    "W5": { "min": 40, "max": 49, "min_km": 700 },
    "M6": { "min": 50, "max": 59, "min_km": 600 },             
    "W6": { "min": 50, "max": 59, "min_km": 600 },
    "M7": { "min": 60, "min_km": 500 },             
    "W7": { "min": 60, "min_km": 500 },
}


ID_PLATZ = 0
ID_NAME = 1
ID_KM = 2
ID_GROUP = 3


def main():
    cli = parseCli()

    for (file, year) in zip(cli.input_files, cli.input_files_years):
        print(f"file {file}")
        with open(os.path.join(SCRIPT_DIR, file), "r") as f:
            csvr = csv.reader(f, delimiter="|")
            header = next(csvr)
            print("header: ", header)
            out_data = transform_data(header, list(csvr))

            md_out = write_data(year, header, out_data)

            output_dir = os.path.join(SCRIPT_DIR, cli.output_directory)
            try: os.mkdir(output_dir)
            except: pass

            print("====== md_out ======")
            print(md_out)
            with open(os.path.join( output_dir, 
                f"lrv_brandenburg_{year}.md"), "w") as f:
                f.write(md_out)
            


        
def transform_data(header: list[str], input_rows: list[list[str]]) -> dict[str, list[list[str]]]:
    assert(header[ID_PLATZ].lower() == "platz")
    assert(header[ID_NAME].lower() == "name")
    assert(header[ID_KM].lower() == "kilometer")
    assert(header[ID_GROUP].lower() == "gruppe")

    input_rows = list(filter(lambda c: c[0] != '', input_rows))


    # Name anonymization
    names: list[tuple[str, str]] = []
    for row in input_rows:
        splitted = row[ID_NAME].split(' ', 1)
        print("splitted:", splitted)
        names.append((splitted[0], splitted[1]))
    arb_state = arbitration.ArbitrationState(iter(names))
    arb_state.compute_shorthands()
    for i, name_row in enumerate(iter(names)):
        input_rows[i][ID_NAME] = arb_state.lookup(name_row)

    # Build groups by classification
    data: dict[str, list[list[str]]] = {}
    for key in GROUPS.keys(): data[key] = []

    header = header[0:4]
    print(f"\theader: {header}")
    for row in input_rows:
        #if row[0] == '': break
        row = row[0:4]

        #print(f"Group {row[ID_GROUP]}")
        assert(row[ID_GROUP] in GROUPS)
        data[row[ID_GROUP]].append(row)
        #print("\t", row)

    for key in data.keys():
        data[key].sort(key=lambda c: int(c[ID_PLATZ]))
        print("\t", key, data[key])

    return data

def write_data(
        year: int,
        header: list[str],
        data: dict[str, list[list[str]]]) -> str:
    md = ""
    md += f"""---
title: Sommerwettbewerb LRV Brandenburg {year}
weight: 0
date: {year}
---
"""
    for group in GROUPS_LIST:
        assert(group in GROUPS)
        rows = data[group]
        place_space = ft.reduce(
                lambda acc, c: max(acc, len(c)),
                map(lambda c: c[ID_PLATZ], rows),
                len(header[ID_PLATZ]))
        name_space = ft.reduce(
                lambda acc, c: max(acc, len(c)),
                map(lambda c: c[ID_NAME], rows),
                len(header[ID_NAME]))
        km_space = ft.reduce(
                lambda acc, c: max(acc, len(c)),
                map(lambda c: c[ID_KM], rows),
                len(header[ID_KM]))


        # Group heading
        #group = cd[ID_GROUP]
        gender: str|None = None 
        if group.startswith("M"): gender = "Männlich"
        if group.startswith("W"): gender = "Weiblich"
        if "max" in GROUPS[group]:
            min_max = f"{GROUPS[group]['min']} - {GROUPS[group]['max']}"
        else:
            min_max = f"ab {GROUPS[group]['min']}"

        md += "{{% v 2 %}}\n"
        md += f"\n## {gender} Alter {min_max} (Erfüllung: mindestens {GROUPS[group]['min_km']} km)\n\n"


        if len(data[group]) == 0:
            md += "In diesem Jahr gab es keine Erfüller dieser Kategorie\n\n"
            continue

        # Table
        place_fmt = format_space(header[ID_PLATZ], place_space)
        name_fmt = format_space(header[ID_NAME], name_space)
        km_fmt = format_space(header[ID_KM], km_space)
        md += f"| {place_fmt} | {name_fmt} | {km_fmt} |\n"
        md += f"|{'-' * (place_space + 2)}|{'-' * (name_space + 2)}|{'-' * (km_space + 2)}|\n"
        for row in rows:
            place_fmt = format_space(row[ID_PLATZ], place_space)
            name_fmt = format_space(row[ID_NAME], name_space)
            km_fmt = format_space(row[ID_KM], km_space)
            md += f"| {place_fmt} | {name_fmt} | {km_fmt} |\n"
        md += "\n"


    return md

def format_space(v: str, length: int) -> str:
    if (len(v) > length): return v
    return v + (" " * (length - len(v)))


@dataclass
class Cli:
    input_files: list[str]
    input_files_years: list[int]
    output_directory: str

def parseCli() -> Cli:
    def helpExit(msg: str|None = None, exit_code: int = 1) -> typing.NoReturn:
        exe_name = "transform_lrv.py"
        if msg is not None: print(msg + "\n\n")
        print(f"USAGE: {exe_name} OPTIONS <INPUT_FILE INPUT_FILE_YEAR ...>")
        print(f"")
        print(f"OPTIONS:")
        print(f" -h, --help                 print this and exit")
        #print(f" -i, --input-file           specify an input file")
        #print(f" -y, --input-file-year      specify a year for the given input file, count must be identical to input files specified, order matters")
        print(f" -o, --output-dir           specify output folder")
        sys.exit(exit_code)

    input_files: list[str] = []
    input_files_years: list[int] = []
    output_dir: str | None = None


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
        #elif carg == "-i" or carg == "--input-file":
        #    carg = next(va, None)
        #    if (carg is None): helpExit("Expected input file path")
        #    input_files.append(carg);
        #elif carg == "-y" or carg == "--input-file-year":
        #    carg = next(va, None)
        #    if (carg is None): helpExit("Expected corresponding year of input file")
        #    input_files_years.append(int(carg));
        else: #helpExit("Extraneous arguments given")
            if (carg.startswith("-")): helpExit(f"Unknown option {carg}")
            print("Positional: ", carg)
            input_file = carg
            input_file_year = next(va, None)
            if input_file_year is None: helpExit("Expected year following the input filepath")
            try: input_file_year = int(input_file_year)
            except: helpExit(f"Expected year as a number, but got \"{input_file_year}\"")
            input_files.append(input_file)
            input_files_years.append(input_file_year)
        carg = next(va, None)

    if len(input_files) == 0:
        helpExit("At least one input file has to be given")
    if len(input_files) != len(input_files_years):
        helpExit("a year has to be specified for each input file")

    return Cli(
        input_files=input_files,
        input_files_years=input_files_years,
        output_directory=(output_dir if output_dir is not None else helpExit("output directory has to be specified")),
    )



if __name__ == "__main__":
    main()
