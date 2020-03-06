"""
energy ("loudness") based segmentation

This program export audio segments from a audio clip based on interesting events.
An interesting event is registered if the energy levels breaks a defined threshold within a defined time frame.

# TODO rewrite as a class
"""
import librosa
import librosa.display
import numpy as np
import argparse
import os, sys
import soundfile as sf
import matplotlib.pyplot as plt
import random
import logging

parser = argparse.ArgumentParser()
parser.add_argument(
	'--import_path',
	type=str,
	default='test_folder/',
	help='Location of import directory')

parser.add_argument(
	'--export_path',
	type=str,
	default='export_folder/',
	help='Location of export directory')

parser.add_argument(
	'--sample_rate',
	type=int,
	default=22050,
	help='Sample rate of exported audio')

parser.add_argument(
	'--CLIP_DURATION',
	type=int,
	default=3,
	help='Duration of segmeted audio')

parser.add_argument(
	'--export_filename',
	type=str,
	default='export_file',
	help='New file name')

parser.add_argument(
	'--plot',
	type=bool,
	default=False,
	help='Plots Spectrograms')

parser.add_argument(
	'--sound_type',
	type=str,
	default='call',
	help='Sound type on audio file')

FLAGS, unparsed = parser.parse_known_args()

IMPORT_PATH = FLAGS.import_path
EXPORT_PATH = FLAGS.export_path
IMPORTED_FILES = None

try:
	IMPORTED_FILES = os.listdir(IMPORT_PATH)
except IOError as e:
	logging.error("Could not import file names from path '{}'.\n Exit program with error: {}".format(IMPORT_PATH, e))
	exit()

TOT_FILES_IMPORTED = len(IMPORTED_FILES)
PLOT_SPECTROGRAMS = FLAGS.plot
SAMPLE_RATE = FLAGS.sample_rate
CLIP_DURATION = FLAGS.CLIP_DURATION*FLAGS.sample_rate
TOTAL_DURATION = 0
OFFSET = 0.2
THRESHOLD_MEAN = 0.85 # song=0.95 call=0.85

# Spectrograms config
N_FFT=2048
HOP_LENGTH = 512
UPPER_HZ_LIMIT=10000
LOWER_HZ_LIMIT=1000
WINDOW_LENGTH=N_FFT
N_MELS=128
CURRENT_POS = 0.5*SAMPLE_RATE
TOT_CLIPS = 0
IGNORED_CLIPS = 0
SAVED_NOISE = 0
IGNORED_FILES = 0


def __main__():

	imported_files()
	make_dir(EXPORT_PATH)
	pre_processing_audio(CURRENT_POS,TOT_CLIPS,IGNORED_CLIPS,SAVED_NOISE,TOTAL_DURATION,IGNORED_FILES)


def imported_files():
	"""
	import files from given directory
	"""
	# IMPORTED_FILES = os.listdir(IMPORT_PATH) # dir is your directory path
	TOT_FILES_IMPORTED = len(IMPORTED_FILES)
	logging.info("Import path: {}".format(IMPORT_PATH))
	logging.info("Total number of files names retrieved: {}".format(TOT_FILES_IMPORTED))


def make_dir(new_dir):
	"""
	creates new directory if not exists
	"""
	if not os.path.exists(new_dir):
		os.makedirs(new_dir)
		logging.info("Created directory '{}'".format(new_dir))
	return new_dir


def get_spectrograms(y):
	# TODO add function desc and what is y?
	unfiltered_signal = np.abs(librosa.stft(y,n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=N_FFT))
	raw_energy = librosa.feature.rmse(S=unfiltered_signal, frame_length=N_FFT, hop_length=HOP_LENGTH)
	# Filter out freq above 10k and below 1k Hz
	filtered_signal = librosa.feature.melspectrogram(
		S=unfiltered_signal,
		n_fft=N_FFT,
		hop_length=HOP_LENGTH,
		fmax=UPPER_HZ_LIMIT,
		fmin=LOWER_HZ_LIMIT,
		n_mels=N_MELS
	)
	tot_energy = librosa.feature.rmse(
		S=filtered_signal,
		frame_length=N_FFT,
		hop_length=HOP_LENGTH,
		center=True,
		pad_mode='reflect')
	return unfiltered_signal, raw_energy, filtered_signal, tot_energy


def segmentation(
		y,
		i,
		filename,
		mean_energy_of_file,
		CURRENT_POS,
		CLIP_DURATION,
		SAMPLE_RATE,
		file_duration,
		saved_bird_sounds,
		saved_noise,
		ignored_clips,
		ignored_files
):
	"""
	Energy based segmentation
	"""
	while CURRENT_POS + CLIP_DURATION < SAMPLE_RATE*file_duration:

		# Window
		data = y[int(CURRENT_POS):int(CURRENT_POS + CLIP_DURATION)]

		unfiltered_signal, unfiltered_energy, filtered_signal, filtered_energy = get_spectrograms(data)
		# Local average energy
		mean_energy_of_window = np.mean(filtered_energy)
		logging.info("mean_energy_of_window/mean_energy_of_file = {}".format(mean_energy_of_window/mean_energy_of_file))
		# extract loudest parts
		if mean_energy_of_window / mean_energy_of_file >= THRESHOLD_MEAN:  # and localMax/mean_energy_of_file>THRESHOLD_MAX_OVER_MEAN):
			# save if begging and end of snippet has low energy.
			# print(np.mean(filtered_energy[0][0:5])<mean_energy_of_file*.8)
			# print(np.mean(filtered_energy[0][len(filtered_energy[0])-6:len(filtered_energy[0])-1])<mean_energy_of_file*0.8)
			energy_start_of_window = np.mean(filtered_energy[0][0:4])
			energy_end_of_window = np.mean(filtered_energy[0][len(filtered_energy[0])-5:len(filtered_energy[0])-1])

			if energy_start_of_window<mean_energy_of_file and energy_end_of_window<mean_energy_of_file:
				sf.write(FLAGS.export_path + FLAGS.export_filename + '_' + filename + '_' + str(i) + '_' + str(CURRENT_POS / SAMPLE_RATE) + '.wav', data, SAMPLE_RATE)
				saved_bird_sounds += 1
				CURRENT_POS = CURRENT_POS+CLIP_DURATION*random.uniform(0.25, 0.65)
				# print('CURRENT_POS:' + str(CURRENT_POS/SAMPLE_RATE))
				if FLAGS.plot:
					plot_spectrograms(unfiltered_energy, unfiltered_signal, filtered_energy, filtered_signal)

			else:
				CURRENT_POS = CURRENT_POS + CLIP_DURATION * random.uniform(0.5, 0.20)
		elif mean_energy_of_window / mean_energy_of_file < THRESHOLD_MEAN*0.03:  # sets ratio to 0.075
			sf.write('exported_noise/' + FLAGS.export_filename + '_' + str(i) + '_nohash_noise_' + str(CURRENT_POS/FLAGS.sample_rate) + '.wav', data, SAMPLE_RATE)
			saved_noise += 1
			CURRENT_POS = CURRENT_POS+CLIP_DURATION
		else:
			# print('****Clip ignored:')
			ignored_clips += 1
			CURRENT_POS = CURRENT_POS + CLIP_DURATION*random.uniform(0.2, 0.4)
	if saved_bird_sounds == 0:
		ignored_files += 1
	return saved_bird_sounds, saved_noise, ignored_clips, ignored_files


def plot_spectrograms(unfiltered_energy, unfiltered_signal, filtered_energy, filtered_signal):
	plt.figure(figsize=(16, 6))
	# Unfiltered energy graph
	plt.subplot(4, 2, 1)
	plt.semilogy(unfiltered_energy.T, label='RMS Energy: unfiltered')
	plt.xticks([])
	plt.xlim([0, unfiltered_energy.shape[-1]])
	plt.legend(loc='best')
	# Unfiltered spectrogram
	plt.subplot(4, 2, 2)
	librosa.display.specshow(librosa.power_to_db(unfiltered_signal,ref=np.max),y_axis='mel', x_axis='time')
	plt.colorbar(format='%+2.0f dB')
	plt.title('Unfiltered spectrogram')
	plt.tight_layout()
	# Filtered energy
	plt.subplot(4, 2, 3)
	plt.semilogy(filtered_energy.T, label='RMS Energy: filtered')
	plt.xticks([])
	plt.xlim([0, filtered_energy.shape[-1]])
	plt.legend(loc='best')
	# Filtered spectrogram
	plt.subplot(4, 2, 4)
	librosa.display.specshow(librosa.power_to_db(filtered_signal, ref=np.max),y_axis='mel', x_axis='time')
	plt.title('Filtered spectrogram')
	plt.colorbar(format='%+2.0f dB')

	plt.show()
	plt.close()


def pre_processing_audio(CURRENT_POS,TOT_CLIPS, IGNORED_CLIPS,SAVED_NOISE,TOTAL_DURATION, IGNORED_FILES):
	for i in range(TOT_FILES_IMPORTED):
		logging.info("FLAGS.plot: {}".format(FLAGS.plot))
		filename = IMPORTED_FILES[i]
		logging.info("Preprocessing file: {} / {}".format(str(i + 1), str(len(IMPORTED_FILES))))
		logging.info("filename: {}".format(filename))
		logging.info("CLIP_DURATION/SAMPLE_RATE = {}".format(str(CLIP_DURATION/SAMPLE_RATE)))

		# load audio file ad create a data array represenation
		y, sr = librosa.load(str(IMPORT_PATH + filename), mono=True, offset=OFFSET, sr=SAMPLE_RATE)

		# duration in sec
		file_duration = librosa.get_duration(y=y, sr=sr)
		TOTAL_DURATION = TOTAL_DURATION + file_duration
		energy_file = get_spectrograms(y)[3]
		mean_energy_of_file = np.mean(energy_file)

		saved_bird_sounds = 0
		saved_noise = 0
		ignored_clips = 0
		ignored_files = 0
		saved_bird_sounds, saved_noise, ignored_clips, ignored_files = segmentation(
			y,
			i,
			filename,
			mean_energy_of_file,
			CURRENT_POS,
			CLIP_DURATION,
			SAMPLE_RATE,
			file_duration,
			saved_bird_sounds,
			saved_noise,
			ignored_clips,
			ignored_files
		)

		CURRENT_POS = 0
		TOT_CLIPS = TOT_CLIPS + saved_bird_sounds
		IGNORED_CLIPS = IGNORED_CLIPS + ignored_clips
		SAVED_NOISE = SAVED_NOISE + saved_noise
		IGNORED_FILES = IGNORED_FILES + ignored_files

		logging.info('Tot number of birds clips saved: {}'.format(saved_bird_sounds))
		logging.info('Tot number of noise clips saved: {}'.format(saved_noise))
		logging.info('Tot number of clips ignored: {}'.format(ignored_clips))

		logging.info('SAVED_NOISE: {}'.format(SAVED_NOISE))
		logging.info('TOT_CLIPS: {}'.format(TOT_CLIPS))
		logging.info('IGNORED_CLIPS: {}'.format(IGNORED_CLIPS))
		logging.info('Ignored files: {}'.format(IGNORED_FILES))

	logging.info('Total time: {}'.format(TOTAL_DURATION/60))


__main__()
