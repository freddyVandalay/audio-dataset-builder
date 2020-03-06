"""
This script copy files from a specified folders subdirectories into a new specified path.
The user can specify the number fo files to be copied to the new paths subdirectories.
The files are picked randomly.

The export path is created if it does not exist

__root export path
	|
	|__subdir 1
	|__subdir 2
	|__subdir 3
	|__...


***Orinally created to create datasets for model training with TensorFlow

"""
import argparse
import logging
import numpy as np
import os
import random
import shutil

parser = argparse.ArgumentParser()
parser.add_argument(
	'--import_path',
	type=str,
	default='import_folder',
	help='Location of import directory')
parser.add_argument(
	'--export_path',
	type=str,
	default='export_folder',
	help='Location of export directory')
parser.add_argument(
	'--samples',
	type=int,
	default='200',
	help='Specifies the number of samples to be saved in the directory')

FLAGS, unparsed = parser.parse_known_args()

IMPORT_PATH = FLAGS.import_path
EXPORT_PATH = FLAGS.export_path
SAMPLES = FLAGS.samples


def __main__():
	create_dir(EXPORT_PATH)
	generate_dataset()


def generate_dataset():
	root_dir = IMPORT_PATH
	for subdir in os.listdir(root_dir):
		files_in_path = os.listdir("{}/{}/".format(IMPORT_PATH, subdir))
		export_subdirectory = "{}/{}_{}".format(EXPORT_PATH, subdir, SAMPLES)

		create_dir(export_subdirectory)

		logging.info("Processing subdirectory '{}'...".format(subdir))
		while len(os.listdir(export_subdirectory)) < SAMPLES:
			np.random.shuffle(files_in_path)
			exported_files = os.listdir(export_subdirectory)
			pick_if_one = random.randint(0, len(files_in_path)-1)

			if files[pick_if_one] not in exported_files:
				copy_source = "{}/{}".format(IMPORT_PATH, files[pick_if_one])
				copy_destination = "{}/{}".format(export_subdirectory, files[pick_if_one])
				shutil.copy(copy_source, copy_destination)

	logging.info("Files copied to {}".format(EXPORT_PATH))


def create_dir(dir_name):
	if not os.path.exists(dir_name):
		logging.info("Created directory '{}'".format(dir_name))
		os.makedirs(dir_name)


__main__()
