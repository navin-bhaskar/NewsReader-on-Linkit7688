#!/usr/bin/env python

"""         Shree Krishnaya Namaha        """
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

import cherrypy as http
import uuid 
import config

class rest:
    def __init__(self, stationFile):
        self.stations = []
        self.maxStations = 5
        self.stationFile = stationFile
        self.__fill_stations__()
        
        self. preHtmlStr="""
        <html><body>
        <h1> Random news reader on the Linkit 7688  </h1>
        <h2> Input the RSS links here: </h2>
        """
        self.formHtmlStartStr = """
        <form method='get' action='/posted'>
        """

        self.formHtmlEndStr = """<input type='submit' value='Submit' />"""
        
        self. postHtmlStr = """
        </form></body>
        </html>"""
        
    def __make_station_page__(self):
        preHtmlStr = self.preHtmlStr + self.formHtmlStartStr
         
        for i in range(0, self.maxStations):
           preHtmlStr = preHtmlStr + """station %d:  <input value="%s" name="station%d" size='50'/> <br>""" \
           %(i+1, self.stations[i], i+1)
           
        
        return preHtmlStr + self.formHtmlEndStr + self.postHtmlStr
        
    def __fill_stations__(self):
        try:
            stations = open(self.stationFile, 'r')
            lines = stations.readlines()
            stations.close()
        except:
            print "Could not open the file "
            lines = ""
        
        print "Stations line "
        print lines
        self.stations = []
        for line in lines:
            self.stations.append(line)

        while len(self.stations) < self.maxStations:
            self.stations.append('')
        
    @http.expose
    def index(self):
       return self.__make_station_page__()

    @http.expose
    def posted(self, station1, station2, station3, station4, station5):
        
        stations = open(self.stationFile, 'w')
        
        stations.write(station1 + '\n')
        stations.write(station2 + '\n')
        stations.write(station3 + '\n')
        stations.write(station4 + '\n')
        stations.write(station5 + '\n')

        stations.close()
        
        self.__fill_stations__()
        
        try:
            f = open(config.NEW_LIST_FILE, "w")
            f.write("Done writing")
            f.close()
        except:
            pass
        
        return self.__make_station_page__()
        
if __name__ == "__main__":
    http.config.update( {'server.socket_host':"0.0.0.0", 'server.socket_port':8181 } )
    http.quickstart(rest(config.RSS_LINKS_FILE))
