#!/usr/bin/python3

import sys
sys.path.append('./lib/')

import snowboydecoder
import signal
import speech_recognition as sr
from mqttIPCHandler import MqttIPC
from detection import speechDetection

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted


if __name__ == '__main__':
    # Confere se modelo foi passado como argumento
    if len(sys.argv) == 1:
        print("Error: need to specify model name")
        print("Usage: python3 main.py your.model")
        sys.exit(-1)

    model = sys.argv[1]

    # Tratativa dos signals
    signal.signal(signal.SIGINT, signal_handler)

    # Mqtt Inter Proccess Comunication Handler
    Mqtt = MqttIPC()

    # Utiliza modelo como hotword
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

    detectionHandler = speechDetection(detector, Mqtt)

    # main loop
    detector.start(detected_callback=detectionHandler.hotword_callback,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

    detector.terminate()
