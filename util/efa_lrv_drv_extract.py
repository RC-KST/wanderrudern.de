#!/usr/bin/env python3

import typing
import functools as ft
from dataclasses import dataclass
import csv
import os
import sys

C_CLASS = 0
C_CLASS_TXT = 1
C_PREREQ = 2
C_NAME = 3
C_BIRTH_YEAR = 4
C_KM = 6

TRIP_FIELDS = 6
TRIP_BASE = 9
C_TRIP_ID = lambda trip: TRIP_BASE + (TRIP_FIELDS * trip) + 0
C_TRIP_BEGIN = lambda trip: TRIP_BASE + (TRIP_FIELDS * trip) + 1
C_TRIP_END = lambda trip: TRIP_BASE + (TRIP_FIELDS * trip) + 2
C_TRIP_NAME = lambda trip: TRIP_BASE + (TRIP_FIELDS * trip) + 3
C_TRIP_KM = lambda trip: TRIP_BASE + (TRIP_FIELDS * trip) + 4
def trip_count_from_row(trips_row: list[str]) -> int:
    trips_row_len = len(trips_row)
    i: int = 0
    while (C_TRIP_ID(i) < trips_row_len) and trips_row[C_TRIP_ID(i)] != "": i += 1
    return i

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

GROUPS_DRV_LIST = [
    "Jugend 3b", "Jugend 3c", "Jugend 3d", "Jugend 3e",
    "Männer 1a", "Frauen 2a",
    "Männer 1b", "Frauen 2b",
    "Männer 1c", "Frauen 2c",
]
GROUPS_DRV = {
    "Jugend 3a": { "min": 8, "max": 10, "min_km": 200, "min_trip_info": "eine dreitägige Wanderfahrt", "info": "Jugend" },
    "Jugend 3b": { "min": 11, "max": 12, "min_km": 300, "min_trip_info": "eine dreitägige Wanderfahrt", "info": "Jugend" },
    "Jugend 3c": { "min": 13, "max": 14, "min_km": 400, "min_trip_info": "eine dreitägige Wanderfahrt", "info": "Jugend" },
    "Jugend 3d": { "min": 15, "max": 16, "min_km": 700, "min_trip_info": "eine dreitägige Wanderfahrt", "info": "Jugend" },
    "Jugend 3e": { "min": 17, "max": 18, "min_km": 800, "min_trip_info": "eine dreitägige Wanderfahrt", "info": "Jugend" },

    "Männer 1a": { "min": 19, "max": 60, "min_km": 800, "min_trip_info": "davon 160 Wanderfahrtskilometer", "info": "Männlich" },
    "Männer 1b": { "min": 61, "max": 75, "min_km": 600, "min_trip_info": "davon 120 Wanderfahrtskilometer", "info": "Männlich" },
    "Männer 1c": { "min": 76, "min_km": 500, "min_trip_info": "davon 100 Wanderfahrtskilometer", "info": "Männlich" },

    "Frauen 2a": { "min": 19, "max": 60, "min_km": 800, "min_trip_info": "davon 160 Wanderfahrtskilometer", "info": "Weiblich" },
    "Frauen 2b": { "min": 61, "max": 75, "min_km": 600, "min_trip_info": "davon 120 Wanderfahrtskilometer", "info": "Weiblich" },
    "Frauen 2c": { "min": 76, "min_km": 500, "min_trip_info": "davon 100 Wanderfahrtskilometer", "info": "Weiblich" },
}

GROUPS_LRV_LIST = [ "M1", "W1", "M2", "W2", "M3", "W3", "M4", "W4", "M5", "W5", "M6", "W6", "M7", "W7" ]
GROUPS_LRV = {
    "M1": { "min": 0, "max": 14,  "min_km": 500, "info": "jugend männlich" },
    "W1": { "min": 0, "max": 14,  "min_km": 500, "info": "jugend weiblich" },
    "M2": { "min": 15, "max": 18, "min_km": 800, "info": "jugend männlich" },
    "W2": { "min": 15, "max": 18, "min_km": 800, "info": "jugend weiblich" },
    "M3": { "min": 19, "max": 31, "min_km": 800, "info": "Männlich" },
    "W3": { "min": 19, "max": 31, "min_km": 800, "info": "Weiblich" },
    "M4": { "min": 32, "max": 39, "min_km": 700, "info": "Männlich" },
    "W4": { "min": 32, "max": 39, "min_km": 700, "info": "Weiblich" },
    "M5": { "min": 40, "max": 49, "min_km": 700, "info": "Männlich" },
    "W5": { "min": 40, "max": 49, "min_km": 700, "info": "Weiblich" },
    "M6": { "min": 50, "max": 59, "min_km": 600, "info": "Männlich" },
    "W6": { "min": 50, "max": 59, "min_km": 600, "info": "Weiblich" },
    "M7": { "min": 60, "min_km": 500, "info": "Männlich" },
    "W7": { "min": 60, "min_km": 500, "info": "Weiblich" },
}


def main():
    cli = parseCli()

    assert(cli.competition == "lrv" or cli.competition == "drv")
    GROUPS = GROUPS_LRV if cli.competition == "lrv" else GROUPS_DRV
    GROUPS_LIST = GROUPS_LRV_LIST if cli.competition == "lrv" else GROUPS_DRV_LIST

    for filepath, year in zip(cli.input_files, cli.input_files_years):
        with open(filepath) as f:
            print(f"[{year}] file: {filepath}")
            csvr = csv.reader(f, delimiter="|")
            persons = parse_csv(csvr)

            classes: dict[str, list[Person]] = {}
            for group in GROUPS_LIST: classes[group] = []
            for person in persons: classes[person.rclass].append(person)

            for person in persons:
                print(f"item: {person.name} ({person.km}km, class_info: {person.rclass_info})")
                for trip in person.trips:
                    print(f"\t{trip}")

            md_txt = write_md(GROUPS_LIST, GROUPS, classes, year, cli.competition)

            output_file_path = gen_out_path(filepath, cli.output_directory, "md")
            try: os.mkdir(cli.output_directory)
            except: pass
            with open(output_file_path, "w") as f: f.write(md_txt)

            if cli.export_ewige:
                output_file_path = gen_out_path(filepath, cli.output_directory, "csv")
                rows = write_csv(GROUPS_LIST, GROUPS, classes, year, cli.competition)
                with open(output_file_path, "w") as f:
                    csvw = csv.writer(f, delimiter=";")
                    csvw.writerows(rows)

def write_csv(
    GROUPS_LIST: list[str],
    GROUPS: dict[str, dict[str, int]],
    class_persons: dict[str, list[Person]],
    year: int,
    competition: str) -> list[list[str]]:

    rows = []
    rows.append(["Name", "Jahres-Kilometer", "Gold gewonnen (Ja/Nein/True/False)"])
    
    persons: list[Person] = list(ft.reduce(lambda acc, c: acc + class_persons[c], class_persons.keys(), []))
    persons.sort(key=lambda c: c.km)
    persons.reverse()

    for person in persons:
        name = " ".join(reversed(list(map(lambda c: c.strip(), person.name.split(',', 1)))))
        #print(f"name: '{name}'")
        rows.append([name, person.km, "false"])

    return rows

def gen_out_path(input_file_path: str, output_dir: str, new_ext: str) -> str:
    output_file_path = os.path.basename(input_file_path)
    if len(output_file_path.rsplit('.', 1)) != 0:
        output_file_path = output_file_path.rsplit('.', 1)[0]
    output_file_path = os.path.join(output_dir, output_file_path + "." + new_ext)
    return output_file_path

def write_md(
    GROUPS_LIST: list[str],
    GROUPS: dict[str, dict[str, int]],
    class_persons: dict[str, list[Person]],
    year: int,
    competition: str) -> str:
    assert(competition == 'lrv' or competition == 'drv')

    md = ""
    md_title = f"Sommerwettbewerb LRV Brandenburg {year}" if competition == 'lrv' \
            else f"DRV Jahreswettbewerb {year}"
    md += f"""---
title: {md_title}
weight: 0
date: {year}
---

"""
    for cclass in GROUPS_LIST:
        assert(cclass in GROUPS)

        name_heading = "Name"
        name_space = ft.reduce(
                lambda acc, c: max(acc, len(c)),
                map(lambda c: c.name, class_persons[cclass]),
                len(name_heading))
        km_heading = "Kilometer"
        km_space = ft.reduce(
                lambda acc, c: max(acc, len(c)),
                map(lambda c: c.km_str, class_persons[cclass]),
                len(km_heading))
        trip_km_heading = "davon Wanderfahrtskilometer"
        trip_km_space = ft.reduce(
                lambda acc, c: max(acc, len(c)),
                map(lambda c: c.trips_km_str, class_persons[cclass]),
                len(trip_km_heading))

        md += "{{% v 2 %}}\n"

        min_max_age = f"{GROUPS[cclass]['min']} - {GROUPS[cclass]['max']} Jahre" \
                if "max" in GROUPS[cclass] else f"ab {GROUPS[cclass]['min']} Jahre"
        md += f"\n## {GROUPS[cclass]['info']}: {min_max_age}\n"
        min_trip_info = f", {GROUPS[cclass]['min_trip_info']}" if "min_trip_info" in GROUPS[cclass] else ""
        md += f"Erfüllung mit mindestens {GROUPS[cclass]['min_km']}km{min_trip_info}.\n"

        # Table
        print(f"class {cclass}: {GROUPS[cclass]}")
        name_fmt = format_space(name_heading, name_space)
        km_fmt = format_space(km_heading, km_space)
        trip_km_fmt = format_space(trip_km_heading, trip_km_space)
        md += f"| {name_fmt} | {km_fmt} | {trip_km_fmt} |\n"
        md += f"|{'-' * (name_space + 2)}|{'-' * (km_space + 2)}|{'-' * (trip_km_space + 2)}|\n"
        for person in class_persons[cclass]:
            name_fmt = format_space(person.name, name_space)
            km_fmt = format_space(person.km_str, km_space)
            trip_km_fmt = format_space(person.trips_km_str , trip_km_space)
            md += f"| {name_fmt} | {km_fmt} | {trip_km_fmt} |\n"
        if len(class_persons[cclass]) == 0:
            name_fmt = format_space("-", name_space)
            km_fmt = format_space("-", km_space)
            trip_km_fmt = format_space("-" , trip_km_space)
            md += f"| {name_fmt} | {km_fmt} | {trip_km_fmt} |\n"
        md += "\n"
        #print(f"\t-> {person.name} ({person.km}km, wanderfahrt: {trips_km})")
    return md

def format_space(v: str, length: int) -> str:
    if (len(v) > length): return v
    return v + (" " * (length - len(v)))

def parse_csv(r) -> list[Person]:
    name_line: list[str] | None = next(r, None)
    entries: list[Person] = []
    while name_line is not None:
        if name_line[0] == "": panic("Malformed efa format, expected class information in first column")

        rclass = name_line[C_CLASS]
        rclass_info = name_line[C_CLASS]
        prereq = name_line[C_PREREQ]
        name = name_line[C_NAME]
        birth = name_line[C_BIRTH_YEAR]
        _ = birth
        km = int(name_line[C_KM])

        trips_list: list[Trip] = []

        # Find last row of this persons trip information section
        last_trips_row = None
        current_trips_row = next(r, None)
        while current_trips_row is not None and current_trips_row[0] == "":
            last_trips_row = current_trips_row
            current_trips_row = next(r, None)
        name_line = current_trips_row

        if last_trips_row is not None:
            for i in range(trip_count_from_row(last_trips_row)):
                trip_name = last_trips_row[C_TRIP_NAME(i)]
                trip_km = last_trips_row[C_TRIP_KM(i)]
                trip_begin = last_trips_row[C_TRIP_BEGIN(i)]
                trip_end = last_trips_row[C_TRIP_END(i)]
                trips_list.append(Trip(
                    name = trip_name,
                    km = int(trip_km),
                    begin = trip_begin,
                    end = trip_end,
                    ))

        trips_km = ft.reduce(lambda acc, c: acc + c, map(lambda c: c.km, trips_list))
        entries.append(Person(
            name = name,
            km = km,
            km_str = f"{km}km",
            rclass_info = rclass_info,
            rclass = rclass.replace(')', ''),
            prereq = prereq,
            trips = trips_list,
            trips_km_str = f"{trips_km}km",
        ))

    return entries

@dataclass
class Person:
    name: str
    km: int
    km_str: str
    rclass_info: str
    rclass: str
    prereq: str
    trips: list[Trip]
    trips_km_str: str

@dataclass
class Trip:
    name: str
    km: int
    begin: str
    end: str



def panic(msg: str) -> typing.NoReturn:
    print("[PANIC]: " + msg, file=sys.stderr)
    sys.exit(-100)


#def parse_efa_exp(reader)


@dataclass
class Cli:
    input_files: list[str]
    input_files_years: list[int]
    output_directory: str
    competition: str
    export_ewige: bool


def helpExit(msg: str|None = None, exit_code: int = 1) -> typing.NoReturn:
    exe_name = "efa_lrv_drv_extract.py"
    if msg is not None: print(msg + "\n\n")
    print(f"USAGE: {exe_name} OPTIONS <INPUT_FILE INPUT_FILE_YEAR ...>")
    print(f"")
    print(f"OPTIONS:")
    print(f" -h, --help                 print this and exit")
    print(f" --drv,--lrv                Specify which competition will be extracted")
    print(f" --export-ewige             Export for the list that holds all rowed kilometers")
    #print(f" -i, --input-file           specify an input file")
    #print(f" -y, --input-file-year      specify a year for the given input file, count must be identical to input files specified, order matters")
    print(f" -o, --output-dir           specify output folder")
    sys.exit(exit_code)

def parseCli() -> Cli:
    input_files: list[str] = []
    input_files_years: list[int] = []
    output_dir: str | None = None
    competition: str | None = None
    export_ewige: bool = False


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
        elif carg == "--drv" or carg == "--lrv":
            if competition is not None: helpExit(" Only one instance of --lrv/--drv may be specified")
            if carg == "--drv": competition = "drv"
            else: competition = "lrv"
        elif carg == "--export-ewige":
            export_ewige = True
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
        competition=competition if competition is not None else helpExit("one of --drv/--lrv have to be speicified"),
        export_ewige=export_ewige,
    )


if __name__ == "__main__":
    main()

