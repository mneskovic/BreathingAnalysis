import sounddevice as sd
from scipy.io.wavfile import write
from pyAudioAnalysis import audioTrainTest as aT

# Train SVM Classifier
aT.extract_features_and_train(["data/exhale","data/inhale"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svmSMtemp", False)

fs = 44100  # Sample rate
seconds = 0.5  # Duration of recording
prevBreath = -1

while True:

    # Record chunk
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file

    # Classify the chunk
    (currBreath, scores) = aT.file_classification("New Recording 4.wav", "svmSMtemp","svm")
    if scores[currBreath] > 0.8:
        if currBreath != prevBreath:
            if currBreath == 0.0:
                print("Just Exhaled")
            else:
                print("Just Inhaled")
            prevBreath = currBreath

