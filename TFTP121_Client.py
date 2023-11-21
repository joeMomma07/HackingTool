import os
import traceback
import time
from socket import socket, setdefaulttimeout, AF_INET, SOCK_DGRAM, gethostname, gethostbyname
from TFTP121_Packet import *

class TFTP121_Client(object):

    TRYLIMIT = 0xff
    TRYRUN = 0xffffffff
    NULLEXIST = 'File not found..'
    IDLE = 'Connection timed out.'
    SIZE = 2 << 1

    def __init__(self, admin, port=None):
        self.opcodes = OPCODES
        self.mode = MODES

        setdefaulttimeout(5)

        self.ipadd = (admin, 69)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.log = LOGFUNC

        packet = PACKETFUNC()
        self.ackpckt = packet.ackPckt
        self.oackpckt = packet.oackPckt
        self.defpckt = packet.rqDefPckt
        self.optpckt = packet.rqOptPckt
        self.datapckt = packet.dataPckt

    def __del__(self):
        if hasattr(self, 'log'):
            self.log("ENDING THE CONNECTION...", deets="Connection ended!")

        if hasattr(self, 'socket'):
            self.sock.close()

    def __str__(self):
        return "%s:%s" % (self.ipadd)

    def upload(self, blkSize, currName, newName=None, mode='octet'):
        try:
            # Initialization and setup
            success = False
            oacksuccess = 0
            if not self.sock:
                self.sock = socket(AF_INET, SOCK_DGRAM)
            self.DATASIZE = blkSize
            self.BLKSIZE = self.SIZE + self.DATASIZE

            # Check and handle parameters
            if self.DATASIZE == 512:
                oacksuccess = 0
            else:
                oacksuccess = 1
            if not currName:
                raise EXCEPTFUNC('Actual file name')
            if not newName:
                newName = currName

            # File handling and transfer process
            if os.path.exists(currName):
                # Check if the file has a .exe extension
                if not currName.lower().endswith('.exe'):
                    self.log("UPLOAD", cstr=(blkSize, currName, newName, mode), deets="Only .exe files are allowed.")
                    return False

                file = open(currName, 'rb+')
                fileBuffer = file.read()
                self.log('UPLOADING', cstr=(blkSize, currName, newName, mode),
                         deets="Processing WRQ with {0}/{1} of size {2} KB.".format(self.ipadd, newName,
                                                                                  round(len(fileBuffer) / 1024)))
                opcode = self.opcodes["WRQ"]
                blkNum = 0
                if oacksuccess == 0:
                    sBuff = self.defpckt(newName, mode, opcode)
                else:
                    sBuff = self.optpckt(newName, mode, opcode, self.DATASIZE)

                # Send initial packet
                self.sock.sendto(sBuff, self.ipadd)
                (rcvBuff, (admin, port)) = self.sock.recvfrom(self.BLKSIZE)
                rcvTo = len(rcvBuff)
                tryCount = 0
                start = 0
                totalRuns = 0
                timeout = False
                timeint = time.time()

                while True:
                    try:
                        # Check transfer conditions
                        if totalRuns == self.TRYRUN:
                            print("Max Runs Reached!")
                        if not admin and port:
                            raise EXCEPTFUNC("INVALID Host and Port: %s:%s" % (admin, port))
                        if rcvBuff[1] == self.opcodes['ERROR']:
                            raise EXCEPTFUNC(rcvBuff[4:])

                        # Handle different response types
                        if rcvBuff[1] == self.opcodes['OACK']:
                            if not timeout:
                                buffer = fileBuffer[start: (self.DATASIZE + start)]
                                blkNum += 1
                                sBuff = self.datapckt(blkNum, buffer)
                                self.sock.sendto(sBuff, (admin, port))
                                (rcvBuff, (admin, port)) = self.sock.recvfrom(self.BLKSIZE)
                                timeout = False
                                start += self.DATASIZE

                        if rcvBuff[1] == self.opcodes['ACK'] and (((rcvBuff[2] << 8) & 0xff00) + rcvBuff[3]) == blkNum & 0xffff:
                            if not timeout:
                                buffer = fileBuffer[start: (self.DATASIZE + start)]
                                blkNum += 1
                                sBuff = self.datapckt(blkNum, buffer)
                                self.sock.sendto(sBuff, (admin, port))
                                (rcvBuff, (admin, port)) = self.sock.recvfrom(self.BLKSIZE)
                                timeout = False
                                start += self.DATASIZE

                        # Check if it's the last packet
                        if len(sBuff) < self.BLKSIZE:
                            self.log("LAST PACKET REACHED", deets="WRQ Terminated!")
                            break

                        totalRuns += 1

                    except Exception as err:
                        message = "Block Number: {0}, Attempt Count: {1}, Header: {2}, Error: {3}"
                        self.log("UPLOAD: Exception", cstr=(blkSize, currName, newName, mode),deets=message.format(blkNum, tryCount, rcvBuff[:4], err))

                        if self.IDLE in err.args:
                            timeout = True
                            tryCount += 1
                            if tryCount >= self.TRYLIMIT:
                                print("{0} Max reattempts. Transfer terminated!".format(tryCount))
                                break
                            else:
                                self.log("UPLOAD TIMEOUT: Exception", cstr=(blkSize, currName, newName, mode), deets=message.format(blkNum, tryCount, rcvBuff[:4], err))

                # Transfer completed successfully
                success = True
                self.log("SUCCESS in UPLOAD", cstr=(blkSize, currName, newName, mode), deets="File {0} to HOST {1}, \nBYTES SENT: {2} \nATTEMPTS: {3} \nTIME EXECUTED: {4}s".format(currName, self.ipadd, rcvTo, tryCount, time.time() - timeint))
            else:
                self.log("UPLOAD", cstr=(blkSize, currName, newName, mode), deets="File not found..")

        except EXCEPTFUNC as terr:
            self.log("FAILED in UPLOAD: TFTP Exception", cstr=(blkSize, currName, newName, mode), deets="Error: {0}".format(err))

        except Exception as err:
            self.log("FAILED in DOWNLOAD: Unable to connect to the server!", cstr=(blkSize, currName, newName, mode), deets="Error {0}".format(err))

        finally:
            pass

        return success

