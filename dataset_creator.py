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
import sys 
import shutil


FLAGS = None 

parser = argparse.ArgumentParser()
################ FLAGS
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

def __MAIN__():
	makeDir(EXPORT_PATH)
	generate_dataset()


def generate_dataset():
	root_dir=IMPORT_PATH
	for subdir in os.listdir(root_dir):
		files_in_path = os.listdir("{}/{}/".format(IMPORT_PATH, subdir))
		export_subdirectory = "{}/{}_{}".format(EXPORT_PATH, subdir, SAMPLES)
		
		makeDir(export_subdirectory)
		
		logging.info("Processing subdirectory '{}'...".format(subdir))
		while len(os.listdir(export_subdirectory)) < SAMPLES:
			np.random.shuffle(files_in_path)
			exported_files = os.listdir(export_subdirectory)
			pick_if_one=random.randint(0,len(files_in_path)-1)
			if files[pick_if_one] not in exported_files:
				shutil.copy("{}/{}".format(IMPORT_PATH, files[pick_if_one]), 
					"{}/{}".format(export_subdirectory, files[pick_if_one]))
	
	logging.info("Files copied to {}".format(EXPORT_PATH))

def makeDir(newDir):
	if not os.path.exists(newDir): 
		logging.info("Created directory '{}'".format(newDir))
		os.makedirs(newDir)
	return newDir

__MAIN__()