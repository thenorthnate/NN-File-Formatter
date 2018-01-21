# Initial stab at formatting for .nn files!
# NN DB Engine

import time
import socket
import struct

class NnServer:
    standardFileFormatter = bytearray([ord('.'), ord('n'), ord('n')])
    userFileFormatter = bytearray([ord('u'), ord('.'), ord('n'), ord('n')])
    privateKeyFileName = 'key.nn'
    userFileName = 'User.nn'
    requestTypeSize = 1

    def __init__(self):
        self.headerLength = None
        self.privateKeyFilePath = None
        self.privateKeyFilePathLength = None
        self.token = None

        self.host = ''
        self.port = 5550

        self.dataFilePath = None

        self.username = None
        self.usernameLength = None
        self.password = None
        self.passwordLength = None

        self.bigEndian = True
        self.signedNumbers = False
        self.packMethod = {}
        self.build_byte_format()


    def build_byte_format(self):
        '''Creates byte formatting during initialization.'''
        self.packMethod = {
            'SHORT':'',
            'INTEGER':'',
            'LONG':'',
            'FLOAT':'',
            'DOUBLE':'',
            'STRING':'',
            'ELSE':''
        }
        if self.bigEndian:
            if self.signedNumbers:
                # First bit relates to sign
                self.packMethod['SHORT'] = '>h'
                self.packMethod['INTEGER'] = '>i'
                self.packMethod['LONG'] = '>q'
                self.packMethod['FLOAT'] = '>f'
                self.packMethod['DOUBLE'] = '>d'
                #self.packMethod['STRING'] = str(self.stringLen) + 's'
                self.packMethod['ELSE'] = '>H'
            else:
                # Unsigned values
                self.packMethod['SHORT'] = '>H'
                self.packMethod['INTEGER'] = '>I'
                self.packMethod['LONG'] = '>Q'
                self.packMethod['FLOAT'] = '>f'
                self.packMethod['DOUBLE'] = '>d'
                #self.packMethod['STRING'] = str(self.stringLen) + 's'
                self.packMethod['ELSE'] = '>H'
        else:
            # Little endian
            if self.signedNumbers:
                # First bit relates to sign
                self.packMethod['SHORT'] = '<h'
                self.packMethod['SHORT'] = '<h'
                self.packMethod['INTEGER'] = '<i'
                self.packMethod['LONG'] = '<q'
                self.packMethod['FLOAT'] = '<f'
                self.packMethod['DOUBLE'] = '<d'
                #self.packMethod['STRING'] = str(self.stringLen) + 's'
                self.packMethod['ELSE'] = '<H'
            else:
                # Unsigned values
                self.packMethod['SHORT'] = '<H'
                self.packMethod['INTEGER'] = '<I'
                self.packMethod['LONG'] = '<Q'
                self.packMethod['FLOAT'] = '<f'
                self.packMethod['DOUBLE'] = '<d'
                #self.packMethod['STRING'] = str(self.stringLen) + 's'
                self.packMethod['ELSE'] = '<H'


    def build_bytes(self, value, datatype='STRING'):
        '''Formats the data value into a set of bytes to be sent over modbus.'''
        byteValue = []
        try:
            byteValue = bytearray(struct.pack(self.packMethod[datatype], value))
        except (ValueError, struct.error) as e:
            #logging.debug('(Modbus) build_bytes: ' + str(value) + ' ' + str(e))
            pass
        return byteValue



    def generate_unique_code(self):
        # TODO Perform a check to see if this file name is taken... create a new code if it already exists!
        pass



    def create_user_file(self):
        self.usernameLength = self.build_bytes(len(self.username), 'SHORT')
        self.passwordLength = self.build_bytes(len(self.password), 'SHORT')
        self.privateKeyFilePathLength = self.build_bytes(len(self.privateKeyFilePath), 'SHORT')

        uniqueCode = str(int(time.time()*1000) % 255)
        #TODO: Perform a check to see if this file name is taken... create a new code if it already exists!

        if self.privateKeyFilePath.endswith('/'):
            filePath = self.dataFilePath + uniqueCode + self.privateKeyFileName
        else:
            filePath = self.dataFilePath + '/' + uniqueCode + self.privateKeyFileName


        with open(filePath, 'wb') as outputFile:
            outputFile.write(self.userFileFormatter)
            outputFile.write(self.usernameLength)
            outputFile.write(bytearray(self.username, 'utf-8'))
            outputFile.write(self.passwordLength)
            outputFile.write(bytearray(self.password, 'utf-8'))
            outputFile.write(self.privateKeyFilePathLength)
            outputFile.write(bytearray(self.privateKeyFilePath, 'utf-8'))



    def initialize_new_file(self):
        '''Sets up a new .nn file from scratch.'''
        pass


    def create_private_key(self):
        '''Creates a new file at the directory given with a random private key.'''
        privateKey = []
        for i in range(64):
            curTime = int(time.time()*1000000)
            uniqueEntry = curTime % 255
            privateKey.append(uniqueEntry)
            time.sleep(.001)
        privateKey = bytearray(privateKey)

        if self.privateKeyFilePath.endswith('/'):
            filePath = self.privateKeyFilePath + self.privateKeyFileName
        else:
            filePath = self.privateKeyFilePath + '/' + self.privateKeyFileName

        with open(filePath, 'wb') as outputFile:
            outputFile.write(privateKey)

    def generate_token(self, username, password):
        '''Generates a token that must be sent with each request after the file has been created.'''
        pass


    def read_user_file(self):
        pass


    def read_data_file(self):
        pass


    def write_to_data_file(self):
        pass


    def decode_request_type(self, msg):
        # Should accept 16bit short 0x00 (255 different request types)
        msg = struct.unpack('B', msg)[0]
        if msg == 0:
            # New user - initialize all files
            pass


    def run_server(self):
        '''Creates the server.'''

        c = None
        addr = None
        sendCount = 0
        try: # Socket Exception
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            #logging.info('(Modbus) run: Waiting for a Connection')
            s.listen(1)
            c, addr = s.accept()
            #logging.info('(Modbus) run: Accepted a connection with: ' + str(addr))

            while True:
                #logging.debug('(Modbus) run: receiving header')
                msg = c.recv(self.messageSize)
                if not msg:
                    break
                sent = self.send(c, msg, sendCount)
                if sent:
                    sendCount += 1


            c.close()
            #logging.debug('(Modbus) run: connection closed')

        except (socket.error, socket.herror, socket.gaierror, socket.timeout) as e:
            #logging.warning('(Modbus) run: socket error: ' + str(e))
            pass
