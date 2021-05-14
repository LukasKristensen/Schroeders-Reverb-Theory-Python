import numpy as np

# Structure of code for implementing schroeder's reverb is inspired from lecture 9 in the Audio Processing course by Mads Græsbøll Christensen

# TODO: Kører koden parralelt ift. kodeflow?


# TODO: Alle arrays kan konverteres over til en
#Default values from lecture
mixingParams = np.array([0.3, 0.25, 0.25, 0.2])
plainReverbDelay = np.array([1553, 1613, 1493, 1153])
allPassReverbDelay = np.array([223, 443])
allPassParams = np.array([-0.7, -0.7])
plainReverbTimeP = [0]

# TODO kan optimeres uden funktion
def gainFromReverb(samplingFrequency):
    inputSoundSize = np.size(plainReverbDelay)
    outputGain = np.zeros(inputSoundSize)

    for i in np.arange(inputSoundSize):
        outputGain[i] = 10**(-3*plainReverbDelay[i]/(plainReverbTimeP[0]*samplingFrequency))

    return outputGain


def plainReverb(data, delay, plainGainTotal):
    soundDataSize = np.size(data)
    outputSound = np.zeros(soundDataSize)

    for i in np.arange(soundDataSize):
        if i < delay:
            outputSound[i] = data[i]
        else:
            outputSound[i] = data[i]+plainGainTotal*outputSound[i-delay]
    return outputSound


def allPassReverb(data, allPassReverbDelayInput, allPassParamsInput):
    soundDataSize = np.size(data)
    outputSound = np.zeros(soundDataSize)

    for i in np.arange(soundDataSize):
        if i < allPassReverbDelayInput:
            outputSound[i] = data[i]
        else:
            outputSound[i] = allPassParamsInput*data[i]+data[i-allPassReverbDelayInput]-allPassParamsInput*outputSound[i-allPassReverbDelayInput]

    return outputSound


def schroedersReverb(soundFile, valueParameters, fileFrequency):
    print("Soundfile:",soundFile)
    print("ParametersInput",valueParameters)

    print("ValuesBefore:\n","mixingParams",mixingParams,"plainReverbDelay",plainReverbDelay,"allPassReverbDelay",allPassReverbDelay,"allPassParams",allPassParams,"plainReverbTime",plainReverbTimeP)
    for i, data in enumerate(valueParameters[0]):
        mixingParams[i] = data
    for i, data in enumerate(valueParameters[1]):
        plainReverbDelay[i] = data
    for i, data in enumerate(valueParameters[2]):
        allPassParams[i] = data
    for i, data in enumerate(valueParameters[3]):
        allPassReverbDelay[i] = data
    for i, data in enumerate(valueParameters[4]):
        plainReverbTimeP[0] = data

    print("ValuesAfter:\n","mixingParams",mixingParams,"plainReverbDelay",plainReverbDelay,"allPassReverbDelay",allPassReverbDelay,"allPassParams",allPassParams,"plainReverbTime",plainReverbTimeP)

    soundFileHolder = np.zeros(np.size(soundFile))

    plainGainTotal = gainFromReverb(fileFrequency)

    for i in range(np.size(plainReverbDelay)):
        soundFileHolder = soundFileHolder+mixingParams[i]*plainReverb(soundFile, plainReverbDelay[i], plainGainTotal[i])

    for i in range(np.size(allPassReverbDelay)):
        soundFileHolder = allPassReverb(soundFileHolder, allPassReverbDelay[i], allPassParams[i])

    print("SoundfileEnd:",soundFileHolder)
    print("Returning schroeders reverb")
    return soundFileHolder
