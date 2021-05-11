import numpy as np
import scipy.io.wavfile

# Structure of code

# TODO: Lav pseudo kode her, som går over fundamentalt hvad funktionerne skal have
# TODO: Kører koden parralelt ift. kodeflow?

mixingParams = np.array([0.4, 0.3, 0.2, 0.1])
plainReverbDelay = np.array([1613, 1493, 1153, 853])
allPassReverbDelay = np.array([200, 400])
allPassParams = np.array([-0.8, 0.8])
plainReverbTime = 1.2

# Reverb time
def gainFromReverb(plainReverbInput, samplingFrequency):
    gainPlain = 10**(-3*plainReverbInput/(samplingFrequency*plainReverbTime))
    print(gainPlain)

    return gainPlain

def plainReverb(data, plainGainTotal):
    print("Data", data,"PlainGainTotal",plainGainTotal)
    soundDataSize = np.size(data)
    outputSound = np.zeroes(soundDataSize)

    for i in soundDataSize:
        if s < plainReverbDelay


    return data


def allPassReverb(data):
    print("Running allpass filter", data)
    return data


def schroedersReverb(soundFile, filterParameters, fileFrequency):
    plainGainTotal = []
    emptySoundFile = np.zeros(np.size(soundFile))

    for i in range (len(mixingParams)):
        plainGainTotal.append(gainFromReverb(int(plainReverbDelay[i]),fileFrequency))

    for i in range(len(plainReverbDelay)):
        emptySoundFile+=plainReverb(soundFile, plainReverbDelay[i], plainGainTotal[i])


    print("TotalGain",plainGainTotal)

    processedPlain = plainReverb(soundFile, plainGainTotal)
    processedAllPass = allPassReverb(processedPlain)
    return processedAllPass
