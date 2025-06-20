#!/usr/bin/python3
import os
import subprocess as sb

def calc_hashes(fnames: list[str]) -> dict[str, str]:
    """Returns a map from filenames to file hashes"""

    fnames_chunked = chunked(100, fnames)
    out_str = ""
    for chunk in fnames_chunked:
        cmd_res = sb.run(["sha256sum"] + chunk, capture_output=True)
        out_str += str(cmd_res.stdout, encoding="UTF-8")

    return filename_to_hash_map(out_str)

    
def filename_to_hash_map(hash_file_data: str) -> dict[str, str]:
    print(f"hashing files from state:\n{hash_file_data}")
    map: dict[str, str] = {}
    for line in hash_file_data.splitlines():
        hash, filepath = line.split()
        map[filepath] = hash
    return map

def map_to_txt(map: dict[str, str]) -> str:
    out_str = ""
    for fname in map:
        out_str += "  ".join([map[fname], fname]) + "\n"
    return out_str

def find_all_filenames(dir: str) -> list[str]:
    hash_filenames: list[str] = []
    for dir_path, dir_names, filenames in os.walk(dir):
        hash_filenames += list(map(lambda f: os.path.join(dir_path, f), filenames))
    return hash_filenames

def chunked(chunk_size: int, l: list) -> list[list]:
    return [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]

def write_to_file(filepath: str, txt: str):
    with open(filepath, "w") as f:
        f.write(txt)

def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File '{filepath}' not found, reading as empty string")
        return ""

    return data
