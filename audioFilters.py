import numpy as np
import scipy.io.wavfile


# TO-DO: Lav pseudo kode her, som går over fundamentalt hvad funktionerne skal have


# Plain reverberators designed to gain the desired reverb
def plainReverb(data):
    print("Running", data)
    return data


def allPassReverb(data):
    print("Running allpass filter", data)
    return data


def schroedersReverb(soundFile, filterParameters):
    processedPlain = plainReverb(soundFile)
    processedAllPass = allPassReverb(processedPlain)
    return processedAllPass

