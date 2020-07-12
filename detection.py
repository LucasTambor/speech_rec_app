#!/usr/bin/python3
import speech_recognition as sr
from logger import Logger
import snowboydecoder

class speechDetection(object):
    # Speech recognizer
    r = sr.Recognizer()
    mic = sr.Microphone()

    command_list = ["blue", "green" ,"red", "stop"]

    def __init__(self, ipc):
        self.Log = Logger("speechDetection")
        self.Log.log("INIT")
        self.ipc = ipc

    def hotword_callback(self):
        self.Log.log("Hotword detect")
        # send status 0 to sound feedback
        self.ipc.send_sound_off()
        # Play recognize sound - ding.wav
        snowboydecoder.play_audio_file()
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)

        # sound to text
        try:
            text = self.r.recognize_google(audio)
            # pass the string as a list to handler
            self.handle_command(text.split(" "))
        except Exception as e:
            self.Log.log("Failed")
            snowboydecoder.play_audio_file('./lib/resources/dong.wav')
            print(e)


    def handle_command(self, words):
        self.Log.log("Words detected: {}".format(words))
        for word in words:
            for command in self.command_list:
                # Get first command in text input
                if word == command:
                    self.Log.log("Command found: {}".format(command))
                    self.send_command(command)
                    break
            else:
                continue
            break
        else:
            self.Log.log("No command detected")

    def send_command(self, command):
        self.ipc.send_camera(command)

if __name__ == '__main__':
    pass