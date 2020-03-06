from librosa import librosa.display
import numpy as np
import os
import soundfile as sf

dir_name = 'exported_noise_22/'
IMPORTED_FILES = os.listdir(dir_name)
data = np.array(0)

saved = 1
added = 0
print(len(IMPORTED_FILES))
for file in range(0,len(IMPORTED_FILES)):
	added = added+1
	filename = IMPORTED_FILES[file]
	y, sr = librosa.load(str(dir_name + filename), mono = True, offset = 0, sr = 16000)
	data = np.append(data, y)
	if 2 * added >= 70:
		sf.write('noise_clips/noise_{}_.wav'.format(str(saved)), data, sr)
		saved = saved + 1
		added = 0
		data = np.array(0)

	sf.write('noise_clips/noise_.wav', data, sr)
