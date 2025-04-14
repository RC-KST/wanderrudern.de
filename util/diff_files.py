#!/usr/bin/python3

import os
import util

REMOTE_WDIR = ""

WDIR = os.path.dirname(os.path.realpath(__file__))
PUBLIC_PATH = os.path.realpath(os.path.join(WDIR, "..", "public"))
UTIL_HASHING_PATH = os.path.join(os.path.realpath(os.path.join(WDIR, "..")), "util_hashing")
SFTP_BATCH_FILE = os.path.join(UTIL_HASHING_PATH, "update.sftp")
HASHES_FILE = os.path.join(UTIL_HASHING_PATH, "hashes.chk")


def main():
    os.makedirs(UTIL_HASHING_PATH, exist_ok=True)
    print(f"Working dir: {WDIR}")

    data = util.read_file(HASHES_FILE)

    old_fname_to_hash: dict[str, str] = util.filename_to_hash_map(data)
    new_fname_to_hash: dict[str, str] = util.calc_hashes(util.find_all_filenames(PUBLIC_PATH))

    changed: list[str] = []
    removed: list[str] = []
    added: list[str] = []

    for old_fpath in old_fname_to_hash:
        if old_fpath in new_fname_to_hash:
            if old_fname_to_hash[old_fpath] != new_fname_to_hash[old_fpath]:
                changed.append(old_fpath)
            del new_fname_to_hash[old_fpath]
        else:
            removed.append(old_fpath)

    for new_fpath in new_fname_to_hash:
        added.append(new_fpath)


    print("Changed:")
    for c in changed:
        print(f"\t{c}")

    print("\nRemoved:")
    for c in removed:
        print(f"\t{c}")

    print("\nAdded:")

    for c in added:
        print(f"\t{c}")

    put_files = changed + added
    rm_files = removed

    out_str = ""
    dirs_created: dict[str, None] = { "/": None }
    for file in put_files:
        file_remote = f"{REMOTE_WDIR}/{os.path.relpath(file, PUBLIC_PATH)}"
        remote_dirname = os.path.dirname(file_remote)

        if remote_dirname not in dirs_created:
            out_str += f"mkdir -p -f \"{remote_dirname}\";\n"
            dirs_created[remote_dirname] = None

        out_str += f"put \"{file}\" -o \"{file_remote}\";\n"
    out_str += "\n"

    for file in rm_files:
        file_remote = f"{REMOTE_WDIR}/{os.path.relpath(file, PUBLIC_PATH)}"
        out_str += f"rm -r -f \"{file_remote}\";\n"
    out_str += "\nbye;\n"

    util.write_to_file(SFTP_BATCH_FILE, out_str)


if __name__ == "__main__":
    main()
