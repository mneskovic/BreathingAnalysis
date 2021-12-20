import sounddevice as sd
from scipy.io.wavfile import write
from pyAudioAnalysis import audioTrainTest as aT
import scipy

# Train SVM Classifier
aT.extract_features_and_train(["data/filtered/exhale","data/filtered/inhale"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svmSMtemp", False)

fs = 44100  # Sample rate
seconds = 0.5  # Duration of recording
prevBreath = -1

total = 0
numBreaths = -1

while total < 30:

    # Record chunk
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    #write('output.wav', fs, myrecording)  # Save as WAV file
    print(myrecording.shape)
    b, a = scipy.signal.butter(3, [500, 5000], btype='bandpass', fs=fs)
    filteredRecording = scipy.signal.filtfilt(b, a, myrecording[:, 0])
    write('output-filter.wav', fs, filteredRecording)

    # Classify the chunk
    currBreath, scores, classes = aT.file_classification("output-filter.wav", "svmSMtemp","svm")
    currBreath = int(currBreath)

    print("Exhale: " + str(scores[0]) + " Inhale: " + str(scores[1]))

    if scores[currBreath] > 0.8:
        if currBreath != prevBreath:
            numBreaths += 1
            if currBreath == 0.0:
                print("Just Exhaled")
            else:
                print("Just Inhaled")
            prevBreath = currBreath
        else:
            print("Same")
    else:
        print("Inconclusive")
    total += 0.5

print("Breaths per minute: " + str(numBreaths))
