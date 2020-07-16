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
    # Check model in args
    if len(sys.argv) == 1:
        print("Error: need to specify model name")
        print("Usage: python3 main.py your.model")
        sys.exit(-1)

    model = sys.argv[1]

    # Signals handler
    signal.signal(signal.SIGINT, signal_handler)

    # Mqtt Inter Proccess Comunication Handler
    Mqtt = MqttIPC()

    # Speech detection Handler
    detectionHandler = speechDetection(Mqtt)

    # Use model as hotword
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.6)

    # main loop
    detector.start(detected_callback=detectionHandler.hotword_callback,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

    detector.terminate()
