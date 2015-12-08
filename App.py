#!/usr/bin/env python

"""               Shree Krishnaya Namaha             """
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
from NewsReader import NewsReader
import mraa
import config
import os
import time
import signal

keepGoing = True

def signalHandler(signal, frame):
    global keepGoing
    keepGoing = False
    
def main():
    global keepGoing
    inpPin = mraa.Gpio(config.INP_PIN)
    # Set the selected pin as input 
    inpPin.dir(mraa.DIR_IN)
    if config.CONFIG_SERVER_SPAWN == True:
        os.system("python ConfigServer.py&")       # Start the config server 

    # Set the sound card 
    os.environ['ALSA_CARD'] = str(config.AUDIO_CARD_NUMBER)
    try:
        newsList = open(config.RSS_LINKS_FILE, "r")
    except IOError:
        print "Could not open the file %s " %config.RSS_LINKS_FILE
        os.exit(1)

    links = newsList.readlines()
    rss = []
    for link in links:
        temp = link.replace("\n", '')
        if (temp != ""):
            rss.append(temp)
       

    if (len(rss) == 0):
        print "No RSS links, can not continue"
        os.exit(2)

    print rss
    newsReader = NewsReader(rss)
    
    while (keepGoing == True):
        if (inpPin.read() == 0):
            print "Reading the news"
            time.sleep(0.1)
            if os.path.isfile(config.NEW_LIST_FILE):
                try:
                    newsList = open(config.RSS_LINKS_FILE, "r")
                except IOError:
                    print "Could not open the file %s " %config.RSS_LINKS_FILE
                    os.exit(1)

                links = newsList.readlines()
                rss = []
                for link in links:
                    temp = link.replace("\n", '')
                    if (temp != ""):
                        rss.append(temp)

                if (len(rss) == 0):
                    print "No RSS links, can not continue"
                    os.exit(2)
                print "New set of links received, setting the same"
                print rss
                newsReader.setRssLinks(rss)
                os.remove(config.NEW_LIST_FILE)
                
            newsReader.run()
            while (inpPin.read() == 0):
                pass
        else:
            time.sleep(0.1)

    os.system("killall python ConfigServer.py")

            
if __name__ == "__main__":
    # Register the exit handler        
    signal.signal(signal.SIGINT, signalHandler)
    main()
