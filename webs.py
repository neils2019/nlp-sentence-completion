from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json
import os

from urlparse import urlparse, parse_qs
import db

########
#  Neil Joshi - nnjoshi@gmail.com
#
 
class AutoComplete:

    @staticmethod
    def generate_completions(term):
        return db.generate_completions(term)
        #return db.generate_completions1(term)

class LocalData(object):
    records = {'autocomplete':1}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if None != re.search('/*', self.path):
            #recordID = self.path.split('/')[-1]
            recordID = urlparse(self.path).path.split('/')[-1]
            if LocalData.records.has_key(recordID):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                getArgs = parse_qs(urlparse(self.path).query)
                term = getArgs["q"][0]
                #print term
                res_json = json.dumps({"Completions":AutoComplete.generate_completions(term)})
                print res_json
                #print AutoComplete.generate_completions(term)
                self.wfile.write(res_json+"\n")
                #self.wfile.write(LocalData.records[recordID])
            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
 
    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
        
    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
 
    def waitForThread(self):
        self.server_thread.join()
 
    def addRecord(self, recordID, jsonEncodedRecord):
        LocalData.records[recordID] = jsonEncodedRecord
 
    def stop(self):
        self.server.shutdown()
        self.waitForThread()

########################
#
#  Web server: calls db.py to perform autocompletion on GET request for
#              'autocomplete' with args q.  eg. 
#
#              webs.py 13000 127.0.0.1 ./utt.arpa ./utt.txt
#
#              http://localhost:13000/autocomplete?q=What+is+y
#
#              returns json object {"Completions": ["djf", "df"]
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    parser.add_argument('arpa_file', type=str, help='Language model arpa format filename and path, eg. ./utt.arpa')
    parser.add_argument('sentence_file', type=str, help='Model sentence completion filename and path, eg. ./utt.txt')
    args = parser.parse_args()
 
    if os.path.isfile(args.arpa_file) == False:
        raise SystemError("webs.py : input arpa file not found!")
    if os.path.isfile(args.sentence_file) == False:
        raise SystemeError("webs.py : input sentence completion file not found")

    
    (db.NGRAM,db.UTT) = db.init(args.arpa_file,args.sentence_file)
    
    server = SimpleHttpServer(args.ip, args.port)
    print 'HTTP Server Running...........'
    server.start()
    server.waitForThread()
