from pydub import AudioSegment
import os

dirs = ["data/filtered/split/inhale/", "data/filtered/split/exhale/", "data/filtered/doublesplit/exhale/", "data/filtered/doublesplit/inhale/"]

for i in range(2):
    ct = 1
    indir = dirs[i]
    outdir = dirs[len(dirs) - 1 - i]
    for filename in os.listdir(indir):
        sound = AudioSegment.from_wav(indir + filename)
        duration = sound.duration_seconds
        firstHalf = sound[0:duration/2*1000]
        secondHalf = sound[duration/2*1000:duration*1000]
        firstHalf.export(outdir+"train"+str(ct)+".wav", format="wav")
        ct += 1
        firstHalf.export(outdir+"train"+str(ct)+".wav", format="wav")
        ct += 1