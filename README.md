# audio-dataset-builder
Originally designed to create customised datasets for the Simple Audio Recognition tutorial on the TensorFlow website. Includes scrips for segementation and dataset creation.

https://www.tensorflow.org/tutorials/audio_recognition

# Program descriptions:

***Sound Extractor -*** Essentially a segementation tool for audio that extrats two classes (sounds and noise). Identifies sounds based on "loudness" on a recording and saves them as a new audio clip of a defined length to specified directory. 

@TODO The noise extraction function needs some more work. 

***Dataset Creator -*** A tool that imports all files from a directory and its subdirectories and randomly picks and copies a defined number of files into a new directory. The new folder will have the same structure as the original directory that was imported.

***Noise Builder -*** Appends audio clips and creates a new audio clip of approx. 1 min 45 sec. 
