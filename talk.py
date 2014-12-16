SP_FAST = 155
SP_SLOW = 115

import pyttsx
import time

from hyphenate import hyphenate_word
from natospell import nato_spell

import speechsettings

class EliteTalker:
    def __init__(self, nato_spelling=False, hyphen_spelling=False, nato_max_len=7):
        self.speech = self.s = pyttsx.init()
        self.speaking = False
        self.set_normal()
        self.nato = nato_spelling
        self.nato_max_length = nato_max_len
        self.hyphen = hyphen_spelling

        print "Available voices:"
        voices = self.s.getProperty("voices")
        for v in voices:
            print "Name: %-15s - ID: %60s " % (v.name, v.id)

        try:
            if speechsettings.voice_id != None:
                self.s.setProperty("voice",speechsettings.voice_id)
                print "Setting voice to ", speechsettings.voice_id
            if speechsettings.voice_number != None:
                self.set_voice_number(speechsettings.voice_number)
        except:
            print "Error setting the voice!"

    def set_voice_number(self, voice_number):
        voices = self.s.getProperty("voices")
        self.s.setProperty("voice",voices[voice_number].id)
        print "Setting voice to ", voices[voice_number].id


    def say(self, text):
        """Just a shorthand for speak()"""
        return self.speak_now(text)

    def speak_now(self, text):
        self.speak(text, not_now=False)
        return self.flush()

    def speak(self, text, not_now=False):
        self.s.say(text)
        if not_now:
            return
        return self.flush()

    def flush(self):
        if self.speaking:
            print "Already speaking..",

            # this isn't running in a thread! It will never succeed so disabling it

            #counter = 5
            # while counter and self.speaking:
            #     print ".",
            #     counter -= 1
            #     time.sleep(0.1)
            #     #self.s.stop()
            if self.speaking:
                print "stopping."
                #self.s.stop()
                return False
            #print "waited enough."

        self.speaking = True
        try:
            self.s.runAndWait()
        except RuntimeError:
            print "Runtime Error while uttering speech"

        self.speaking = False
        return True

    def set_slow(self):
        self.speech.setProperty("rate", SP_SLOW)

    def set_normal(self):
        self.speech.setProperty("rate", SP_FAST)

    def speak_system(self, system):

        #print "## DEBUG Speak system, nato, hyphen", system, self.nato, self.hyphen
        sys = system

        if self.hyphen==True:
            #print "##DEBUG Hyphen speaking"
            sys = self._system_speakify(system)
            sys = " ".join(hyphenate_word(sys))

        if self.nato==True:
            #print "##DEBUG Nato speaking"
            sys = system
            sys_nato = ""
            for w in sys.split(" "):
                if len(w) < self.nato_max_length:
                    sys_nato += " "+nato_spell(w)
                else:
                    sys_nato += " "+w
            sys = sys_nato
        #print "## DEBUG sys", sys

        if self.nato:
            self.set_normal()
        else:
            self.set_slow()

        self.speak_now(sys)
        self.set_normal()

    @staticmethod
    def _system_speakify(txt):
        new_txt = ""
        counter = 0
        for c in txt:
            counter += 1
            new_txt += c
            if c in "0123456789" and counter % 2:
                new_txt += " "
            if c == "-":
                new_txt += "dash"

        return new_txt

    def announce_system(self, system):
        self.s.setProperty("rate", SP_FAST)
        self.say("Entering system ")
        self.speak(system + "!!")

if __name__ == "__main__":
    e = EliteTalker()
    e.say("This is a test!")
    e.flush()
