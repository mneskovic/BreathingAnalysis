import argparse
import sounddevice as sd
from scipy.io.wavfile import write
from pyAudioAnalysis import audioTrainTest as aT
import scipy

filteredDesired = False
splitDesired = False
fullDesired = False

parser = argparse.ArgumentParser()
parser.add_argument('--filter', dest='filteredDesired', action='store_true')
parser.add_argument('--full', dest='fullDesired', action='store_true')
parser.add_argument('--split', dest='splitDesired', action='store_true')

args = parser.parse_args() 
# Train SVM Classifier
if args.filteredDesired:
    dataPath = "data/filtered"
    if args.splitDesired:
        dataPath = "data/filtered/split"
        print("Split filtered")
elif args.splitDesired:
    dataPath = "data/split"
else:
    dataPath = "data/"

aT.extract_features_and_train([dataPath + "/exhale", dataPath + "/inhale"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svmSMtemp", False)

fs = 44100  # Sample rate
seconds = 0.5  # Duration of recording
prevBreath = -1

total = 0
numBreaths = -1
numInhale = 0
numExhale = 0

print("Starting...")
while total < 30:

    # Record chunk
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    if args.filteredDesired:
        b, a = scipy.signal.butter(3, [500, 5000], btype='bandpass', fs=fs)
        filteredRecording = scipy.signal.filtfilt(b, a, myrecording[:, 0])
        write('output.wav', fs, filteredRecording)
    else:
        write('output.wav', fs, myrecording)  # Save as WAV file

    # Classify the chunk
    currBreath, scores, classes = aT.file_classification("output.wav", "svmSMtemp","svm")
    currBreath = int(currBreath)

    print("Exhale: " + str(scores[0]) + " Inhale: " + str(scores[1]))

    if scores[currBreath] > 0.8:
        if currBreath != prevBreath:
            numBreaths += 1
            if currBreath == 0:
                print("Just Exhaled")
                numExhale +=1 
            else:
                print("Just Inhaled")
                numInhale +=1
            prevBreath = currBreath
        else:
            if prevBreath == 0:
                numExhale += 1
            else:
                numInhale += 1
            print("Same")
    else:
        print("Inconclusive")
    total += 0.5

print("")
print("Breaths per minute: " + str(numBreaths))
print("Num Inhales: " + str(numInhale) + " Num Exhale: " + str(numExhale))
