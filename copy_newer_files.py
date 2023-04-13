#!/usr/local/bin/python3

import os
import shutil
import subprocess
import time
import sys

def copy_missing_and_newer_files(src_dir, dst_dir):
    # Strip the last / character from the src_dir and dst_dir
    if src_dir.endswith("/"):
        l=len(src_dir)
        src_dir = src_dir[:l-1]
    if dst_dir.endswith("/"):
        l=len(dst_dir)
        dst_dir = dst_dir[:l-1]

    # Check if source and destination directories exist
    if not os.path.exists(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        sys.exit()
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Get list of files and subdirectories in source directory
    src_list = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_list.append(os.path.join(root, file))

    # Get list of files and subdirectories in destination directory
    dst_list = []
    for root, dirs, files in os.walk(dst_dir):
        for file in files:
            dst_list.append(os.path.join(root, file))

    # Create a list of relative paths to the source files. It will be used in the comparison for newer files in the source directory
    src_rel_list = []
    for file in src_list:
        src_rel_file = os.path.relpath(file, src_dir)
        src_rel_list.append(src_rel_file)
        # print(f"src_rel_list: '{file}'                       '{src_rel_file}'")

    # Create a list of relative paths to the destination files. It will be used in the comparison for newer files in the source directory
    dst_rel_list = []
    for file in dst_list:
        dst_rel_file = os.path.relpath(file, dst_dir)
        dst_rel_list.append(dst_rel_file)
        # print(f"dst_rel_list: '{file}'                        '{dst_rel_file}'")

    # Copy missing and newer files from source to destination
    new_files = []
    for file in src_rel_list:
        # print(f"file: '{file}'")
        if file not in dst_rel_list:
            src_file = os.path.join(src_dir, file)
            # print(f"src_file: '{src_file}'")
            if os.path.isfile(src_file):
                new_files.append(src_file)
                print(f"Will copy '{src_file}'")
        else:
            src_file = os.path.join(src_dir, file)
            dst_file = os.path.join(dst_dir, file)
            src_mtime = os.path.getmtime(src_file)
            dst_mtime = os.path.getmtime(dst_file)
            # print(f"src_file: '{src_file}'        dst_file: '{dst_file}'        file: '{file}'")
            if src_mtime > dst_mtime:
                if os.path.isfile(src_file):
                    print(f"Will copy '{src_file}' src_mtime-dst_mtime={src_mtime-dst_mtime}")
                    new_files.append(src_file)

    print(f"Copying {len(new_files)} files...")

    # Copy files using the "cp" command and monitor performance in real time
    total_size = sum(os.path.getsize(file) for file in new_files)
    copied_size = 0
    start_time = time.time()
    for file in new_files:
        src_path, src_file = os.path.split(file)
        # print(f"Copying file: '{src_file}' from '{src_path}'  to dst_dir: '{dst_dir}'")
        src_rel_path = os.path.relpath(src_path, src_dir)
        # print(f"src_rel_path: '{src_rel_path}'")
        dst_path = os.path.abspath(os.path.join(dst_dir, src_rel_path))
        # print(f"Making path '{dst_path}'")
        os.makedirs(dst_path, exist_ok=True)
        subprocess.run(["cp", "-p", file, dst_path])
        src_mtime = os.path.getmtime(file)
        dst_mtime = os.path.getmtime(dst_path)
        copied_size += os.path.getsize(file)
        percent_done = int((copied_size / total_size) * 100)
        elapsed_time = int(time.time() - start_time)
        if elapsed_time > 0:
           print(f"{percent_done}% done ({elapsed_time} seconds elapsed) ({copied_size / 1024 / 1024:.2f} MB) ({copied_size / elapsed_time / 1024 / 1024:.2f} MB/s) '{file}'\033[K", end="\r")
        else:
           print(f"{percent_done}% done ({elapsed_time} seconds elapsed) ({copied_size / 1024 / 1024:.2f} MB) '{file}'\033[K", end="\r")

    # Print overall performance summary
    elapsed_time = int(time.time() - start_time)
    if elapsed_time > 0:
        print(f"Copied {len(new_files)} files ({total_size / 1024 / 1024:.2f} MB) in {elapsed_time} seconds ({total_size / elapsed_time / 1024 / 1024:.2f} MB/s)\033[K")
    else:
        print(f"Copied {len(new_files)} files ({total_size / 1024 / 1024:.2f} MB) in {elapsed_time} seconds\033[K")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python copy_missing_and_newer_files.py SRC_DIR DST_DIR")
        sys.exit()
    copy_missing_and_newer_files(sys.argv[1], sys.argv[2])

