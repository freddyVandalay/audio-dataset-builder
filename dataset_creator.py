import os
import sys 
import shutil
import argparse
import random 
import numpy as np

FLAGS = None 

parser = argparse.ArgumentParser()
################ FLAGS
parser.add_argument(
	'--import_path',
    type=str,
    default='import_folder/',
    help='Location of import directory')

parser.add_argument(
	'--export_path',
    type=str,
    default='export_folder/',
    help='Location of export directory')
parser.add_argument(
	'--samples',
    type=int,
    default='200',
    help='Location of export directory')
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
		current_folder = EXPORT_PATH + '/'+ subdir + '_' + str(SAMPLES) + '/'
		
		makeDir(EXPORT_PATH + '/'+ subdir + '_' + str(SAMPLES) + '/')
		
		print('Processing: ')
		print(subdir)
		while len(os.listdir(current_folder))<SAMPLES:
			files = os.listdir(str(IMPORT_PATH + '/' + subdir + '/'))
			np.random.shuffle(files)
			exported_files = os.listdir(current_folder)
			pick_if_one=random.randint(0,len(files)-1)
			if files[pick_if_one] not in exported_files:
				shutil.copy(IMPORT_PATH + '/' + subdir + '/' + files[pick_if_one], current_folder + files[pick_if_one])
	print(' files copied to ' + EXPORT_PATH)

def makeDir(newDir):
	if not os.path.exists(newDir): os.makedirs(newDir)
	return newDir

__MAIN__()