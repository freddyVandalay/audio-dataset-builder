
import librosa
import librosa.display
import numpy as np
import argparse
import os, sys
import soundfile as sf

IMPORTED_FILES = os.listdir('exported_noise_22/')
data = np.array(0)

saved=1
added=0
print(len(IMPORTED_FILES))
for file in range(0,len(IMPORTED_FILES)):
	added=added+1
	filename = IMPORTED_FILES[file]
	y, sr = librosa.load(str('exported_noise_22/' + filename), mono=True, offset=0, sr=16000)
	data = np.append(data,y)
	if 2*added>=70 :
		sf.write('noise_clips/' + 'noise_' + str(saved) + '_.wav', data, sr)
		saved = saved + 1
		added= 0
		data = np.array(0)
sf.write('noise_clips/' + 'noise_' + '.wav', data, sr)
