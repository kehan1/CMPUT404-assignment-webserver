#  coding: utf-8 
import socketserver
import os
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



class MyWebServer(socketserver.BaseRequestHandler):


    
    def handle(self):
        mimetypes.init()
        self.data = self.request.recv(1024).strip()
        self.data = self.data.decode('utf-8')
        splitData = self.data.split()

        #get_path: https://stackoverflow.com/questions/13503610/how-can-i-get-the-path-of-my-python-script
        dirPath = os.path.dirname(os.path.realpath(__file__))
        basePath = "/www"+ splitData[1]
        path = dirPath + basePath
        self.request.sendall(bytearray("HTTP/1.1 ",'utf-8'))
        path1 = os.getcwd()
        path1 = path1+"/www"
        if os.path.exists(path):
            #get abs path https://stackoverflow.com/questions/51520/how-to-get-an-absolute-file-path-in-python
            path2 = os.path.abspath(path)
        else:
            self.request.sendall(bytearray("404 Not Found \r\n",'utf-8'))
            return
        path_split1 = path1.split('/', -1)
        path_split2 = path2.split('/', -1)
        for i in range(len(path_split1)):
            if len(path_split2)<len(path_split1):
                self.request.sendall(bytearray("404 Not Found \r\n",'utf-8'))
                return
            if path_split2[i] != path_split1[i] :
                self.request.sendall(bytearray("404 Not Found \r\n",'utf-8'))
                return
        self.request.sendall(bytearray("200 OK\r\n",'utf-8'))
        if splitData[0]=="GET":             
            if (".html" not in basePath) and (".css" not in basePath):
                if basePath[-1] != "/":
                    basePath = basePath+"index.html"
                else:
                    basePath = basePath+"/index.html"
             
            path = dirPath + basePath
            #mimetype guess: https://docs.python.org/2/library/mimetypes.html
            textType = mimetypes.guess_type(basePath)[0]
            self.request.sendall(bytearray("Content-Type: "+ textType +";\r\n", 'utf-8'))
            self.request.sendall(bytearray("\r\n",'utf-8'))
            openFile = open(path,"r")  
            self.request.sendall(bytearray(openFile.read(),'utf-8'))
            openFile.close()  
        else:
            self.request.sendall(bytearray("405 Method Not Allowed \r\n",'utf-8'))

    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()