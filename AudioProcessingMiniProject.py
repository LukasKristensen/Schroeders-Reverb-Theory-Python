import matplotlib.pyplot as plt
import tkinter as tk
import pyaudio
import wave
import threading
import numpy as np
from numpy import random
import scipy.io.wavfile
import audioFilters

defaultValues = [[0.3, 0.25, 0.25, 0.2], [1553, 1613, 1493, 1153], [223, 443], [-0.7, -0.7],[0.7]]

currentThreadsInputPlay = []
currentThreadsOutputPlay = []

mixingGUI = []
mixingLABEL = []

plainReverbGUI = []
plainReverbLABEL = []

plainReverbAmpGUI = []
plainReverbAmpLABEL = []

allPassDelayGUI = []
allPassDelayLABEL = []

allPassParamGUI = []
allPassParamLABEL = []

playing = False
soundfileInfo = []

matplotAwait = [True]
matplotData = []

def matplobLib():
    samplerate, data = scipy.io.wavfile.read("africa-toto.wav", mmap=False )

    print(len(data))
    listHalf = data[:len(data)//2]
    listHalfHalf = data[:len(listHalf)//2]

    emptyarray = []

    for i in listHalfHalf:
        emptyarray.append(i/2)

    emptyarray=np.array(emptyarray)

    while matplotAwait[0]:
        ""

    plt.figure("Input and output comparison")
    plt.title("Graph for .wav file")
    plt.plot(matplotData[1])
    plt.plot(matplotData[0])

    scipy.io.wavfile.write("testing-africa.wav",samplerate,emptyarray.astype(np.dtype('i2')))
    plt.show()

def standardPresetOne():
    for i, data in enumerate(defaultValues[0]):
        mixingGUI[i].set(data)
    for i, data in enumerate(defaultValues[1]):
        plainReverbGUI[i].set(data)
    for i, data in enumerate(defaultValues[2]):
        allPassDelayGUI[i].set(data)
    for i, data in enumerate(defaultValues[3]):
        allPassParamGUI[i].set(data)
    for i, data in enumerate(defaultValues[4]):
        plainReverbAmpGUI[i].set(data)

def getValues():
    storedVals = [[], [], [], [],[]]

    for i in mixingGUI:
        storedVals[0].append(i.get())
    for i in plainReverbAmpGUI:
        storedVals[1].append(i.get())
    for i in plainReverbGUI:
        storedVals[2].append(i.get())
    for i in allPassDelayGUI:
        storedVals[3].append(i.get())
    for i in plainReverbAmpGUI:
        storedVals[4].append(i.get())

    print("storedVals",storedVals)
    return storedVals


def processAudioPass():
    valueParameters = getValues()

    processedAudio = audioFilters.schroedersReverb(soundfileInfo[0], valueParameters, soundfileInfo[1])
    scipy.io.wavfile.write("africa-toto-output.wav", soundfileInfo[1], processedAudio.astype(np.dtype('i2')))

    matplotData.append(soundfileInfo[0])
    matplotData.append(processedAudio)
    matplotAwait[0] = False

    return processedAudio


def displayGUI():
    bgC = "Light gray"

    audioGUIWindow = tk.Tk()
    audioGUIWindow.title("Audio Processing Mini-project - Lukas Kristensen")

    audioGUIWindow.wm_minsize(1000, 500)
    audioGUIWindow.resizable(False,False)

    mixingLabel = tk.Label(text="Mixing parameters")
    plainReverbLabel = tk.Label(text="Plain reverb parameters")
    allPassLabel = tk.Label(text="Allpass parameters")

    playAudio = tk.Button(text="Play original .wav file", width="20", height="5", bg=bgC, fg="black", command=threadStartInput)
    stopAudio = tk.Button(text="Stop .wav original", width="20", height="5", bg=bgC, fg="black", command=threadStopInput)
    processAudio = tk.Button(text="Start Processing", width="20", height="5", bg=bgC, fg="black", command=processAudioPass)
    playNewAudio = tk.Button(text="Play new .wav file", width="20", height="5", bg=bgC, fg="black",command=threadStartOutput)
    stopNewAudioAudio = tk.Button(text="Stop new .wav original", width="20", height="5", bg=bgC, fg="black", command=threadStopOutput)

    standardPreset = tk.Button(text="Standard preset", width="20", height="5", bg=bgC, fg="black", command=standardPresetOne)
    getValue = tk.Button(text="GetValues", width="20", height="5", bg=bgC, fg="black", command=getValues)

    mixingParamLabel1 = tk.Label(text="mixing1")
    mixingParamLabel2 = tk.Label(text="mixing2")
    mixingParamLabel3 = tk.Label(text="mixing3")
    mixingParamLabel4 = tk.Label(text="mixing4")
    mixingLABEL.extend([mixingParamLabel1, mixingParamLabel2, mixingParamLabel3,mixingParamLabel4])

    mixingParamScale1 = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    mixingParamScale2 = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    mixingParamScale3 = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    mixingParamScale4 = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    mixingGUI.extend([mixingParamScale1, mixingParamScale2, mixingParamScale3,mixingParamScale4])

    reverbDelayLabel1 = tk.Label(text="reverbDelay1")
    reverbDelayLabel2 = tk.Label(text="reverbDelay2")
    reverbDelayLabel3 = tk.Label(text="reverbDelay3")
    reverbDelayLabel4 = tk.Label(text="reverbDelay4")
    plainReverbLABEL.extend([reverbDelayLabel1, reverbDelayLabel2, reverbDelayLabel3, reverbDelayLabel4])

    reverbDelayScale1 = tk.Scale(from_=0, to=2000, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    reverbDelayScale2 = tk.Scale(from_=0, to=2000, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    reverbDelayScale3 = tk.Scale(from_=0, to=2000, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    reverbDelayScale4 = tk.Scale(from_=0, to=2000, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    plainReverbGUI.extend([reverbDelayScale1, reverbDelayScale2, reverbDelayScale3, reverbDelayScale4])

    reverbTimeLabel1 = tk.Label(text="reverbTime")
    plainReverbAmpLABEL.extend([reverbTimeLabel1])

    reverbTimeScale1 = tk.Scale(from_=0, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    plainReverbAmpGUI.extend([reverbTimeScale1])

    a5label = tk.Label(text="ReverbDelay1")
    a6label = tk.Label(text="ReverbDelay2")
    allPassDelayLABEL.extend([a5label, a6label])

    d5label = tk.Label(text="AllpassParam1")
    d6label = tk.Label(text="AllpassParam2")
    allPassParamLABEL.extend([d5label, d6label])

    a5scale = tk.Scale(from_=0, to=2000, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    a6scale = tk.Scale(from_=0, to=2000, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    allPassDelayGUI.extend([a5scale, a6scale])

    d5scale = tk.Scale(from_=-0.99, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    d6scale = tk.Scale(from_=-0.99, to=0.99, digits=2, resolution=0.01, bg=bgC, fg="black", orient="horizontal")
    allPassParamGUI.extend([d5scale, d6scale])

    for i in range(len(mixingGUI)):
        # mixingGUI[i].bind("<Button-1>")
        mixingGUI[i].grid(row=(i*2)+1,column=0,pady=10, padx=20,sticky="N")
        mixingLABEL[i].grid(row=(i*2)+2,column=0,pady=0,sticky="N")
    mixingLabel.grid(row = 0, column=0, pady =5)

    for i in range(len(plainReverbGUI)):
        plainReverbGUI[i].grid(row=(i*2)+1,column=1,pady=10,sticky="N")
        plainReverbLABEL[i].grid(row=(i*2)+2,column=1,pady=0,sticky="N")
    plainReverbLabel.grid(row = 0, column=1, pady =5)

    plainReverbAmpGUI[0].grid(row=1,column=2,pady=10,sticky="N")
    plainReverbAmpLABEL[0].grid(row=2,column=2,pady=0,sticky="N")

    allPassLabel.grid(row = 0, column=3, pady =5)

    for i in range(len(allPassDelayGUI)):
        allPassDelayGUI[i].grid(row=(i*2)+1,column=3,pady=10,sticky="N")
        allPassDelayLABEL[i].grid(row=(i*2)+2,column=3,pady=0,sticky="N")

    for i in range(len(allPassParamGUI)):
        allPassParamGUI[i].grid(row=(i*2)+5,column=3,pady=10,sticky="N")
        allPassParamLABEL[i].grid(row=(i*2)+6,column=3,pady=0,sticky="N")

    standardPreset.grid(row=11,column=2, pady=40)
    getValue.grid(row=11,column=3,pady=40)

    playAudio.grid(row = 12, column=1, pady =40)
    stopAudio.grid(row = 12, column=2, pady =40)
    processAudio.grid(row = 12, column=3, pady =40)
    playNewAudio.grid(row = 12, column=4, pady =40)
    stopNewAudioAudio.grid(row = 12, column=5, pady =40)

    audioGUIWindow.mainloop()


def playOriginalWav():
    fileName = "africa-toto.wav"
    wavRead = wave.open(fileName, "rb")
    print("Status: Currently playing",fileName)

    pyA = pyaudio.PyAudio()

    frameRate = wavRead.getframerate()
    print("frameRate:",frameRate)

    audioStream = pyA.open(format=pyA.get_format_from_width(wavRead.getsampwidth()),
                           channels=wavRead.getnchannels(),
                           rate=frameRate,
                           output=True)
    data = wavRead.readframes(frameRate)
    while data and len(currentThreadsInputPlay) != 0:
        audioStream.write(data)
        data = wavRead.readframes(frameRate)


def playOutputWav():
    fileName = "africa-toto-output.wav"
    wavRead = wave.open(fileName, "rb")
    print("Status: Currently playing",fileName)

    pyA = pyaudio.PyAudio()

    frameRate = wavRead.getframerate()
    print("frameRate:",frameRate)

    audioStream = pyA.open(format=pyA.get_format_from_width(wavRead.getsampwidth()),
                           channels=wavRead.getnchannels(),
                           rate=frameRate,
                           output=True)
    data = wavRead.readframes(frameRate)
    while data and len(currentThreadsOutputPlay) != 0:
        audioStream.write(data)
        data = wavRead.readframes(frameRate)

def threadStartInput():
    holdThreadSize = len(currentThreadsInputPlay)
    currentThreadsInputPlay.append(threading.Thread(target=playOriginalWav))
    currentThreadsInputPlay[holdThreadSize].start()


def threadStopInput():
    if len(currentThreadsInputPlay) != 0:
        currentThreadsInputPlay.pop(len(currentThreadsInputPlay) - 1)
        print("Status: Stopped. Total threads -", len(currentThreadsInputPlay))


def threadStartOutput():
    holdThreadSize = len(currentThreadsOutputPlay)
    currentThreadsOutputPlay.append(threading.Thread(target=playOutputWav))
    currentThreadsOutputPlay[holdThreadSize].start()


def threadStopOutput():
    if len(currentThreadsOutputPlay) != 0:
        currentThreadsOutputPlay.pop(len(currentThreadsOutputPlay) - 1)
        print("Status: Stopped. Total threads -", len(currentThreadsOutputPlay))


samplerate, data = scipy.io.wavfile.read("day3_testing_sample.wav", mmap=False)

soundfileInfo.append(data)
soundfileInfo.append(samplerate)


tkinterGUIthread = threading.Thread(target=displayGUI)
tkinterGUIthread.start()

matplobLib()
