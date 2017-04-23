import telnetlib
import time
import socket


class lightpack():

    def __init__(self, _host = '127.0.0.1', _port = 3636, _ledMap = [1,2,3,4,5,6,7,8,9,10], _apiKey = None):
        self.host = _host
        self.port = _port
        self.ledMap = _ledMap
        self.apiKey = _apiKey

    def __readResult(self):  # Return last-command API answer  (call in every local method)
        total_data = []
        data = self.connection.recv(8192)
        total_data.append(data)
        #print(total_data)
        return total_data

    def getAPIStatus(self):
        cmd = b'getstatusapi\n'
        self.connection.send(cmd)
        status = str(self.__readResult())
        status = status.split(':')[1]
        status = status.replace('\\r\\n\']','')
        return status

    def connectLightpack(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.host, self.port))
            self.__readResult()
            if self.apiKey is not None:
                   cmd = bytes('apikey:' + self.apiKey + '\n','utf-8')
                   self.connection.send(cmd)
                   self.__readResult()
                   return 0
        except:
             print ('Lightpack API server is missing')
             return -1

    def getProfiles(self):
        cmd = b'getprofiles\n'
        self.connection.send(cmd)
        profiles = str(self.__readResult()).replace('\\r\\n\']','')
        return profiles.split(':')[1].rstrip(';\n').split(';')

    def getProfile(self):
       cmd = b'getprofile\n'
       self.connection.send(cmd)
       profile = str(self.__readResult())
       profile = profile.split(':')[1].replace('\\r\\n\']','')
       return profile

    def getStatus(self):
        cmd = b'getstatus\n'
        self.connection.send(cmd)
        status = str(self.__readResult())
        status = status.split(':')[1].replace('\\r\\n\']','')
        return status

    def getCountLeds(self):
        cmd = b'getcountleds\n'
        self.connection.send(cmd)
        count = str(self.__readResult()).replace('\\r\\n\']','')
        count = count.split(':')[1]
        return int(count)

    # def setColor(self, n, r, g, b):  # Set color to the define LED
    #     cmd = b'setcolor:{0}-{1},{2},{3}\n'.format(self.ledMap[n - 1], r, g, b)
    #     self.connection.send(cmd)
    #     self.__readResult()

