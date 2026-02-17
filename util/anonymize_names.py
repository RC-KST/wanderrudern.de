#!/bin/env python
import typing
import base64
from enum import Enum
import struct
from dataclasses import dataclass
import os
import sys

def main():
    cli = parse_cli()

    
    print(f"Data file: {cli.input_file}")
    try:
        with open(cli.input_file, "rb") as f: fd = f.read()
    except Exception as e: 
        print(f"Could not read from file: {e}")
        fd = b''
    print(f"Data read {len(fd)}:", fd)
    ignore_data = deserialize_data(fd)


    if isinstance(cli.sub_cmd, AddCmd):
        for entry in cli.sub_cmd.names:
            idx = contains_person(ignore_data, entry[0])
            if idx is None:
                ignore_data.append(entry)
            else:
                print("[INFO]: person not in database, replacing...")
                ignore_data[idx] = entry
    elif isinstance(cli.sub_cmd, RemoveCmd):
        for entry, _ in cli.sub_cmd.names:
            idx = contains_person(ignore_data, entry)
            if idx is not None:
                del ignore_data[idx]
            else: print("[INFO]: person not in database, ignoring...")
    elif isinstance(cli.sub_cmd, ListCmd):
        print("Stored names:")
        for i, (entry, replacement) in enumerate(ignore_data): print(f"\t[{i}]: '{entry}' -> '{replacement}'")
        return
    elif isinstance(cli.sub_cmd, AnonymizeCmd):
        print("Anonymize files: ", cli.sub_cmd.files)
        for file in cli.sub_cmd.files:
            anonymize_file(file, ignore_data)

    else: assert(False)

    with open(cli.input_file, "wb") as f:
        print(f"writing data: {ignore_data}")
        d = serialize_data(ignore_data)
        print(f"Data write {len(d)}:", d)
        #if isinstance(cli.sub_cmd, ListCmd): assert(d == fd)
        f.write(d)

def anonymize_file(filepath: str, ignore_data: list[tuple[str, str]]):
    with open(filepath, "r") as f: text = f.read()

    for name, replacement in ignore_data:
        print(f"replacement: '{name}' -> '{replacement}'")
        text = text.replace(name, replacement)

    with open(filepath, "w") as f: f.write(text)


def serialize_data(l: list[tuple[str, str]]) -> bytes:
    for c in l:
        if ':' in c or '|' in c: helpExit(f"Invalid name '{c}', no ':' or '|' characters allowed")
    #print("[ser] serializing: ", l)
    d_concat = "|".join(map(lambda c: ":".join(c), l)).encode()
    #print(f"[ser] d concat: ", d_concat)
    d_enc = base64.b64encode(d_concat).decode()
    #print(f"[ser] b64 dec: {d_enc} -> rot13")
    #assert(d_enc == d_enc.translate(ROT13_TRANS).translate(ROT13_TRANS_RET))
    d_enc_transl = d_enc
    #d_enc_transl = d_enc.translate(ROT13_TRANS)
    #print(f"[ser] b64 enc: rot13 -> {d_enc_transl}")
    #d = base64.b64decode(d_enc_transl)
    d = d_enc_transl.encode()
    #print("[ser] serialized: ", d)
    return d

def contains_person(l: list[tuple[str, str]], name: str) -> None | int:
    for i, (cname, _) in enumerate(l):
        if cname == name: return i
    return None

def deserialize_data(d: bytes) -> list[tuple[str, str]]:
    #b = b64rot13(d, ret=True).decode()
    #print("[deser] deserializing: ", d)

    d_enc = d
    #d_enc = base64.b64encode(d)
    #print(f"[deser] b64 enc: {d_enc} -> rot13_ret")
    d_enc_transl = d_enc
    #d_enc_transl = d_enc.translate(ROT13_TRANS_RET)
    #print(f"[deser] b64 dec: rot13_ret -> {d_enc_transl}")
    b = base64.b64decode(d_enc_transl)
    #print(f"[deser] d_enc_transl rot13: ", base64.b64decode((base64.b64encode(b)).translate(ROT13_TRANS)))
    #print("[deser] concat: ", b)
    l = list(map(lambda c: (c[0], c[1]),
                 map(lambda c: c.split(':', 1),
                     filter(lambda c: len(c) != 0,
                            b.decode().split('|')))))
    #print("[deser] deserialized: ", l)
    return l

ROT13_TRANS = bytes.maketrans(
        b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        b"NOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLM=")
ROT13_TRANS_RET = bytes.maketrans(
        b"NOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLM=",
        b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")

@dataclass
class Cli:
    input_file: str
    sub_cmd: AddCmd | RemoveCmd | ListCmd | AnonymizeCmd

def parse_cli() -> Cli:
    filepath: str | None = None
    sub_cmd: AddCmd | RemoveCmd | ListCmd | AnonymizeCmd | None = None

    it = iter(sys.argv)
    _ = next(it)
    carg = next(it, None)
    cpos = 0
    while (carg is not None):

        if carg == "-h" or carg == "--help": helpExit(exit_code=0)
        else:
            if carg.startswith("-"): helpExit(f"Unkown option '{carg}'")
            if cpos == 0:
                filepath = carg
            elif cpos == 1:
                if carg == "add":
                    sub_cmd = parse_add_cmd(it)
                    for name in sub_cmd.names:
                        if '|' in name:
                            print(f"Invalid name: '{name}'")
                            sys.exit(1)
                elif carg == "remove":
                    sub_cmd = parse_remove_cmd(it)
                elif carg == "list":
                    sub_cmd = parse_list_cmd(it)
                elif carg == "anonymize":
                    sub_cmd = parse_anonymize_cmd(it)
                else: helpExit(f"Unknown comamnd '{carg}'")

            cpos += 1
        carg = next(it, None)

    if filepath is None: helpExit("A filepath has to be given")
    if sub_cmd is None: helpExit("A subcommand has to be specified")

    return Cli(input_file=filepath, sub_cmd=sub_cmd)

@dataclass
class AnonymizeCmd:
    files: list[str]
def parse_anonymize_cmd(it: typing.Iterator[str]) -> AnonymizeCmd:
    files: list[str] = []
    carg = next(it, None)
    while carg is not None:
        if carg.startswith('-'): helpExit("Unknown option for subcommand 'anonymize'")
        files.append(carg)
        carg = next(it, None)
    return AnonymizeCmd(files=files)


@dataclass
class ListCmd: pass
def parse_list_cmd(it: typing.Iterator[str]) -> ListCmd:
    if next(it, None) is not None: helpExit("Expected no further args for list command")
    return ListCmd()

@dataclass
class AddCmd:
    names: list[tuple[str, str]]
def parse_add_cmd(it: typing.Iterator[str]) -> AddCmd:
    names: list[tuple[str, str]] = []
    carg = next(it, None)
    while carg is not None:
        if carg.startswith('-'): helpExit("Unknown option for subcommand 'add'")
        replacement = next(it, None)
        if replacement is None: helpExit(f"Expected name replacement after '{carg}'")
        names.append((carg, replacement))
        carg = next(it, None)
    return AddCmd(names=names)

@dataclass
class RemoveCmd:
    names: list[str]
def parse_remove_cmd(it: typing.Iterator[str]) -> RemoveCmd:
    names: list[str] = []
    carg = next(it, None)
    while carg is not None:
        names.append(carg)
        carg = next(it, None)
    return RemoveCmd(names=names)

def helpExit(msg: str | None = None, exit_code: int = 1) -> typing.NoReturn:
    exe_name = "anonymize_names.py"
    if msg is not None: print(msg + "\n")
    print(f"""USAGE: {exe_name} OPTIONS <Filepath> SUBCMD <subcommand arguments>

OPTIONS:
 -h, --help             Print this and exit

SUBCMDs:
 add <NAMES...>         Add a person to the file
 remove <NAMES...>      Remove a persons from the file
 anonymize <FILES...>   Anonymize files using the specified files
""")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
