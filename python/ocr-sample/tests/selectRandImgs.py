#!/usr/bin/env python3

import os
import shutil
import random

random.seed(1776)
maxfiles = 100
images_dir = "../tdset/"
destination_dir = "../testimages/"

files = os.listdir(images_dir)
files_full = [images_dir + file for file in files]
random.shuffle(files_full)
files_to_copy = files_full[0:maxfiles]

os.makedirs(destination_dir, exist_ok=True)

for file in files_to_copy:
    try:
        shutil.copy(file, destination_dir)
        print(f'Copied {file} to {destination_dir}')
    except FileNotFoundError:
        print(f'File {file} not found.')
    except Exception as e:
        print(f'Error copying {file}: {e}')
