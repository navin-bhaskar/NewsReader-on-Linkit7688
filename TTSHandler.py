#!/usr/bin/python

#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  


import os 
import subprocess
import time

""" Object to handle text to speech conversion using the available TTS
program """		

class TTSHandler:
    """ Uses eSpeak to synthesize the speech from text data.
    This constructor also takes in the path to the espeak program.
    """
    def __init__(self, synth_path=r"espeak"):
        self.synth_path = synth_path
        self.speed = 110    # speed of speech
        self.speak_pro=None
        
    def __status__(self):
        """ Returns the status of the synthesis. Returns true if 
        espeak is running returns false otherwise """
        if (self.speak_pro != None):
            # is the child still executing?
            if (self.speak_pro.poll() == None):
                # Has not exited yet 
                return True
            else:
                return False
        return False
        
    def setSpeed(self, speed):
        self.speed = speed
        
    def speak(self, spk_str):
        """ Speaks out a given string """
        if (type(spk_str) != type("")):
            raise TypeError, "speak(): expected string but received %s "\
            %type(spk_str)
        
        speed = '-s '+ str(self.speed)
        
        try:
            #self.speak_pro = subprocess.call([self.synth_path, speed, spk_str]) 
            speak = subprocess.Popen((self.synth_path, '--stdout', speed, spk_str), stdout=subprocess.PIPE)
            output = subprocess.check_output(('aplay'), stdin=speak.stdout)
            speak.wait()
        except OSError, WindowsError:
            print "Could not execute %s " %self.synth_path      
    
    def Set_TTS_Path(self, path):
        if (type(path) != type("")):
            raise TypeError, "TTS_Path(): expected string "
        if path != "":
            self.synth_path = path  
            
    def Set_TTS_Speed(self, speed):
        """ Sets the speed for TTS """
        if (type(speed) != type(1)):
            return 
        self.speed = speed      
        
        

if __name__ == "__main__":
    import os
    os.environ['ALSA_CARD']=str(2)
    synth = TTSHandler('espeak')
    synth.speak("Hello world")
    
    
            
        
        
        
