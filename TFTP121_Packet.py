import os, traceback
from datetime import datetime

OPCODES = {
    "UNK": 0,
    "RRQ": 1,
    "WRQ": 2,
    "DATA": 3,
    "ACK": 4,
    "ERROR": 5,
    "OACK": 6
}

MODES = {
    "netascii": 1,
    "octet": 2
}

LOGFILE = "TFTP121_Log.txt"
ENV = True
WRITE = True

class LOGFUNC():

    def __init__(self, status, deets=None, cstr=None):
        self.log(status, deets, cstr)

    @staticmethod
    def log(status, deets=None, cstr=None, self=None):
        self.log(status, deets, cstr)

    def log(self, status, deets=None, cstr=None):
        if WRITE:
            try:
                log_entry = "\nSTATUS: {0}\n\nDATE: {1}\nINFO: {2}\nMSG: {3}\n".format(status, datetime.today(), cstr, deets)
                if ENV:
                    print(log_entry)
                with open(LOGFILE, 'a+') as logfile:
                    logfile.write(log_entry)
            except Exception as logex:
                print("LOG EXCEPTION: %s" % (logex))

class PACKETFUNC(object):
    def __init__(self):
        self.log = LOGFUNC
        self.opcodes = OPCODES
        self.modes = MODES
        self.toInt = lambda args: [ord(a) for a in args]
        self.toBytes = bytearray

    def argu(self, *args):
        result = []
        try:
            for arg in args:
                if not isinstance(arg, list):
                    arg = [arg]
                result += arg
        except Exception as err:
            print("Concatenate", err)
        return result

    def rqDefPckt(self, filename, mode, opcode):
        try:
            return self.toBytes(self.argu(0, opcode, self.toInt(filename), 0, self.toInt(mode), 0))
        except Exception as err:
            print("RequestPacket", err)
            self.log("RequestPacket", cstr=(filename, mode, opcode), deets="ERR: %s" % err)

    def rqOptPckt(self, filename, mode, opcode, blksize):
        try:
            return self.toBytes(self.argu(0, opcode, self.toInt(filename), 0, self.toInt(mode), 0, self.toInt("blksize"), 0, self.toInt(str(blksize)), 0))
        except Exception as err:
            print("RequestPacket (Add BlkSize)", err)
            self.log("RequestPacket (Add BlkSize)", cstr=(filename, mode, opcode, blksize), deets="ERR: %s" % err)

    def ackPckt(self, blkNum, buffer=None):
        try:
            return self.toBytes(self.argu(0, self.opcodes['ACK'], ((blkNum >> 8) & 0xff), (blkNum & 0xff)))
        except Exception as err:
            print("ACKPacket", err)
            print(self.argu(0, self.opcodes['ACK'], ((blkNum >> 8) & 0xff), (blkNum & 0xff)))
            self.log("ACKPacket", cstr=(blkNum), deets="CREATING ACKPacket: {0}\nERR: {1}".format(buffer, err))

    def oackPckt(self, blksize, buffer=None):
        try:
            return self.toBytes(self.argu(0, self.opcodes['OACK'], self.toInt("blksize"), self.toInt(str(blksize))))
        except Exception as err:
            print("OACKPacket", err)
            print(self.argu(0, self.opcodes['OACK'], self.toInt("blksize"), self.toInt(str(blksize))))
            self.log("OACKPacket", cstr=(blksize), deets="CREATING OACKPacket: {0}\nERR: {1}".format(buffer, err))

    def dataPckt(self, blkNum, buffer):
        try:
            encoding = 'latin1'
            return self.toBytes(self.argu(0, self.opcodes['DATA'], (blkNum >> 8) & 0xff, blkNum & 0xff, self.toInt(buffer.decode(encoding))))
        except Exception as err:
            print("DATAPacket", err)
            try:
                print(self.argu(0, self.opcodes['DATA'], (blkNum >> 8) & 0xff, blkNum & 0xff, self.toInt(buffer.decode(encoding))))
            except:
                pass
            self.log("DATAPacket", cstr=(blkNum, buffer), deets="CALLING DATAPacket, DATA: {0}\nERR: {1}, \nTRACEBACK: {2}".format(buffer, err, traceback.format_exc()))

class EXCEPTFUNC(Exception):

    def startMsg(self, message):
        self.message = message

    def contMsg(self):
        return str(self.message)

