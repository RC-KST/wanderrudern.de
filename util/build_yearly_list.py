#!/usr/bin/env python3

import csv
import os
import sys
import dataclasses
from dataclasses import dataclass
from typing import NoReturn
import locale
#locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Header name, Position (starting at 0)
PLACE_HEADER = "Platz"
EQUATORS_HEADER = "Äquator"

# Length Equator
EQUATOR_LENGTH=40_077


@dataclass
class KmEntry:
    name: str
    km: int
    last_fulfilment_year: int
    gold_medals: int

def append_files_from_dir(dir: str, file_list: list[str]):
    for path, _, files in os.walk(dir):
        for file in files:
            cfpath = os.path.join(path, file)
            splitted = os.path.basename(cfpath).rsplit('.', 1)
            if (len(splitted) != 2): continue
            if (splitted[1] != "csv"): continue
            try:
                year = int(splitted[0])
                if year < 1000: continue
            except: continue
            file_list.append(cfpath)


#BASE_FILE="../wettbewerbe/ewige_liste/ewige_kilometerliste_base.csv"
def main():
    cli_args = parse_cli(sys.argv)
    if "append_dir" in cli_args and cli_args["append_dir"] is not None:
        append_files_from_dir(cli_args["append_dir"], cli_args["files"])
        

    header, entries = read_basefile(cli_args["base_file"])

    for file in cli_args["files"]:
        append_file(file, entries)

    entries_list = list(entries.values())
    entries_list.sort(key = lambda c: c.km)
    entries_list.reverse()

    write_file(cli_args["output_file"], header, entries_list)

def append_file(path: str, entries: dict[str, KmEntry]):
    year = int(os.path.basename(path).rsplit(".", 1)[0])
    print(f"Processing appendix file '{path}': year: {year}")
    with open(path, "r") as f:
        sniffer = csv.Sniffer()
        sniffer.sniff(f.read(2048))
        f.seek(0)
        r = csv.reader(f, delimiter=";")

        if (sniffer.has_header): next(r) # skip header if existing
        for row in r:
            if len(row) != 3:
                print("[ERROR] Yearly reports have to contain at most 3 columns: Name/Km/Gold won")
                sys.exit(1)

            name = row[0]
            jahres_km = parse_bignum(row[1])
            gold_gewonnen = parse_bool(row[2])

            if name not in entries:
                entries[name] = KmEntry(name, 0, year, 0)

            entries[name].km += jahres_km
            entries[name].gold_medals += 1 if gold_gewonnen else 0
            entries[name].last_fulfilment_year = max(year, entries[name].last_fulfilment_year)



def read_basefile(path: str) -> tuple[list[str], dict[str, KmEntry]]:
    entries: dict[str, KmEntry] = {}
    header: list[str] = []

    print(f"processing base file '{path}'")
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        header = list(next(reader))
        header = [
                PLACE_HEADER,
                header[0],
                header[1],
                header[2],
                header[3],
                EQUATORS_HEADER,
                "",
            ]

        for i, row in enumerate(reader):
            name = row[0]
            #km = locale.atoi(row[1])
            km = parse_bignum(row[1])
            last_fulfilment_year = locale.atoi(row[2])
            gold_medals = locale.atoi(row[3])
            #comment = row[5]
            if name in entries: print(f"[WARNING] name '{name}' is existing multiple times")
            entries[name] = KmEntry(name, km, last_fulfilment_year, gold_medals)
            #print(f"row {i}:", row[0])
    return (header, entries)

def write_file(path: str, header: list[str], entries: list[KmEntry]):

    print(f"Writing output to file: '{path}'")
    with open(path, "w") as f:
        w = csv.writer(f, delimiter=";")
        # Header: Platz, Name, Gesamt-Kilometer, letzte Erfüllung, Gold, Äquator, Comment
        w.writerow(header)
        for i, entry in enumerate(entries):
            eq_done = entry.km // EQUATOR_LENGTH
            eq_km_left = EQUATOR_LENGTH - (entry.km % EQUATOR_LENGTH)
            eq_perc = ((entry.km % EQUATOR_LENGTH) / EQUATOR_LENGTH) * 100

            eq_done_str = f"{eq_done}"
            if eq_done == 0:
                #eq_done_str = ""
                #if eq_perc >= 50.0:
                eq_done_str = f"{eq_perc:.1f}%"

            #print(f"{entry.name} eq perc: {eq_perc}", eq_perc >= 50.0)
            comment = ""
            if eq_perc >= 50.0 or eq_done > 0:
                comment = "fehlen " + format_bignum(eq_km_left) + " km"

            row = [
                    i+1,
                    entry.name,
                    #f"{entry.km:n}",
                    format_bignum(entry.km),
                    entry.last_fulfilment_year,
                    entry.gold_medals,
                    eq_done_str,
                    comment,
                ]
            assert(len(row) == len(header))
            w.writerow(row)

def parse_bool(s: str) -> bool:
    sprep = s.strip().lower()
    if sprep == "ja" or sprep == 'true' or sprep == "yes":
        return True
    elif sprep == "nein" or sprep == 'false' or sprep == "no":
        return False
    else:
        raise Exception("Boolean value may only be one of ja/yes/true/nein/no/false")

# Workaround for internationalized strings
def parse_bignum(s: str) -> int:
    return int(s.replace('.', ''))

# Workaround for internationalized strings
def format_bignum(n: int) -> str:
    return locale.format_string("%d", n, grouping=True).replace(",", ".")

def parse_cli(args: list[str]) -> dict:
    def print_help_and_exit(msg: str | None = None, exit_code: int = 1) -> NoReturn:
        msg_ext = msg + "\n" if msg is not None else ""
        print(msg_ext +
"""Usage: build_ewige_list.py [OPTIONS] <appending files...>

OPTIONS:
 -h, --help                         Print this help and exit
 -o, --output-file                  Specify the csv file, the accumulated data should be written into
 -b, --base-file                    Specify the base csv file, Separator: ';', Columns: 'Name', 'Kilometer', 'last fulfilment', 'gold medal count', 
 -d, --append-dir                   Specify directory where appending files lie, all have to be of the form '<year>.csv'
 -f, --force                        Ignore warnings
""")
        sys.exit(exit_code);

    force: bool = False
    base_file: str | None = None
    out_file: str | None = None
    append_dir: str | None = None
    files: list[str] = []
    i: int = 1
    while (i < len(args)):
        if args[i] == "-h" or args[i] == "--help":
            print_help_and_exit(None, exit_code=0)
        elif args[i] == "-f" or args[i] == "--force":
            force = True
        elif args[i] == "-o" or args[i] == "--output-file":
            i += 1
            if i >= len(args): print_help_and_exit("Expected output file!")
            out_file = args[i]
        elif args[i] == "-b" or args[i] == "--base-file":
            i += 1
            if i >= len(args): print_help_and_exit("Expected base file!")
            base_file = args[i]
            if not os.path.exists(base_file):
                print_help_and_exit(f"The given basefile '{base_file}' does not exist!")
        elif args[i] == "-d" or args[i] == "--append-dir":
            i += 1
            if i >= len(args): print_help_and_exit("Expected directory!")
            append_dir = args[i]
            if (not os.path.exists(append_dir)) or (not os.path.isdir(append_dir)):
                print_help_and_exit(f"The given appending directory '{append_dir}' does not exist or is not a directory!")
        else:
            # Positionals
            files.append(args[i])
        i += 1


    if out_file is None: out_file = "out.csv"
    if not force and os.path.exists(out_file):
        print("[WARNING] This file exists already!")
        overwrite = parse_bool(input("Overwrite output file (ja/nein/yes/now)? "))
        if not overwrite:
            print("Exiting..")
            sys.exit(1)

    if base_file is None: print_help_and_exit("A base file has to be given")

    return {
        "base_file": base_file,
        "output_file": out_file,
        "files": files,
        "append_dir": append_dir,
    }


if __name__ == "__main__":
    main()
