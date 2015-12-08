#!/usr/env python

"""                                Shree Krishnaya Namaha        """
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

from TTSHandler import TTSHandler
import feedparser as fp
from random import randint

class NewsReader(object):
    """ Object that represnets the news reader. 
    Uses feedparser to fetch the news and then uses eSpeak to speak out 
    the news """

    def __init__(self, rssList=[]):
        """ The ctor for this object. This takes in list of RSS feeds """
        self.rss = rssList
        self.rssLen = len(rssList)
        self.speaker = TTSHandler('espeak')

    def setRssLinks(self, rssList):
        """ Sets the current RSS list to the given list """
        self.rss = rssList;
        self.rssLen = len(self.rss)
        
    def run(self):
        """ When called, picks one of the RSS links randomly and then reads out the
        news """
        print self.rssLen
        link = self.rss[randint(0, self.rssLen-1)]
        print "Selected link is %s" %link
        msgToSpeak = ""
        try:
            feed = fp.parse(link)
        except:
            msgToSpeak = "Could not fetch the RSS feed, please try again"

        try:
            msgToSpeak = feed['entries'][0]['title_detail']['value'] # Speak top headline
        except:
            msgToSpeak = "Could not get the right value"

        print "The message that I got"
        print msgToSpeak

        self.speaker.speak(msgToSpeak.encode('ASCII'))
        

if __name__ == "__main__":
    list = [
        "http://www.moneycontrol.com/rss/MCtopnews.xml",
        "http://feeds.reuters.com/reuters/INworldNews",
        "http://timesofindia.feedsportal.com/c/33039/f/533916/index.rss",
        "http://feeds.bbci.co.uk/news/health/rss.xml"
    ]
    newsReader = NewsReader(list)
    newsReader.run()
    
