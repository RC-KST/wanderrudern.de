#!/usr/bin/python3
import os
import subprocess as sb
import util

CHUNK = 100

WDIR = os.path.dirname(os.path.realpath(__file__))
PUBLIC_PATH = os.path.realpath(os.path.join(WDIR, "..", "public"))
UTIL_HASHING_PATH = os.path.join(os.path.realpath(os.path.join(WDIR, "..")), "util_hashing")
HASHES_FILE = os.path.join(UTIL_HASHING_PATH, "hashes.chk")

def main():
    os.makedirs(UTIL_HASHING_PATH, exist_ok=True)

    print(f"Working dir: {WDIR}")
    hash_filenames = util.find_all_filenames(PUBLIC_PATH)

    # Stich together output string from `sha256sum` calls
    hashes_map: dict[str, str] = util.calc_hashes(hash_filenames)

    print(f"hashes: ==={hashes_map}===")

    out_str = util.map_to_txt(hashes_map)

    util.write_to_file(HASHES_FILE, out_str)



if __name__ == "__main__":
    main()
