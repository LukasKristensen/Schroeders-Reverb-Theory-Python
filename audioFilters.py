import numpy as np
import scipy.io.wavfile

# Structure of code

# TODO: Lav pseudo kode her, som går over fundamentalt hvad funktionerne skal have
# TODO: Kører koden parralelt ift. kodeflow?

mixingParams = np.array([0.3, 0.25, 0.25, 0.2])
plainReverbDelay = np.array([853, 1613, 1493, 1153])
allPassReverbDelay = np.array([223, 443])
allPassParams = np.array([-0.7, 0.7])
plainReverbTime = 2


def gainFromReverb(inputSound, plainReverbDelay1, samplingFrequency):
    inputSoundSize = np.size(plainReverbDelay)
    outputGain = np.zeros(inputSoundSize)

    for i in np.arange(inputSoundSize):
        outputGain[i] = 10**(-3*plainReverbDelay[i]/(plainReverbTime*samplingFrequency))

    return outputGain


def plainReverb(data, delay, plainGainTotal):
    soundDataSize = np.size(data)
    outputSound = np.zeros(soundDataSize)

    for i in np.arange(soundDataSize):
        if i < delay:
            outputSound[i] = data[i]
        else:
            print("Iteration",i)
            print("Data",data,"plainGainTotal",plainGainTotal)
            outputSound[i] = data[i]+plainGainTotal*outputSound[i-delay]

    return outputSound


def allPassReverb(data, allPassReverbDelayInput, allPassParamsInput):
    soundDataSize = np.size(data)
    outputSound = np.zeros(soundDataSize)

    for i in np.arange(soundDataSize):
        if i < int(allPassReverbDelayInput):
            outputSound[i] = data[i]
        else:
            outputSound[i] = allPassParamsInput*data[i]+data[i-allPassReverbDelayInput]-allPassParamsInput*outputSound[i-allPassReverbDelayInput]

    return data


def schroedersReverb(soundFile, valueParameters, fileFrequency):
    print("Soundfile:",soundFile)

    plainGainTotal = []
    soundFileHolder = np.zeros(np.size(soundFile))

    for i in range (len(mixingParams)):
        plainGainTotal.append(gainFromReverb(soundFile, int(plainReverbDelay[i]),fileFrequency))

    for i in range(len(plainReverbDelay)):
        soundFileHolder = soundFileHolder+plainReverb(soundFile, plainReverbDelay[i], plainGainTotal[i])

    for i in range(len(allPassReverbDelay)):
        soundFileHolder = allPassReverb(soundFile, allPassReverbDelay[i], allPassParams[i])

    print("SoundfileEnd:",soundFileHolder)
    print("Returning schroeders reverb")
    return soundFileHolder
