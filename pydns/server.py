import socket
from pydns.utils.log import logger
from pydns import config
from pydns.db.filebackend import FileBackend


class Server:

    def __init__(self, port=53, ip='127.0.0.1'):
        self.port = port
        self.ip = ip

        if config.getString('database', 'backend') == 'file':
            self.backend = FileBackend()

        # Initialize udp ipv4 socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

        logger.info("Server started on port " + str(self.port))

        while 1:
            self.data, self.addr = self.sock.recvfrom(512)
            resp = self.buildResponse(data=self.data)
            self.sock.sendto(resp, self.addr)

    def buildResponse(self, data):

        # Transaction ID
        TransactionID = data[:2]
        TID = ''
        for byte in TransactionID:
            TID += hex(byte)[2:]

        # Get the flags
        Flags = self.getFlags(flags=data[2:4])

        # Question Count
        QDCOUNT = b'\x00\x01'

        # Answer Count
        anrecords = self.getRecords(data[12:])
        ANCOUNT = len(anrecords[0]).to_bytes(2, byteorder='big')

        # Nameserver Count
        NSCOUNT = (0).to_bytes(2, byteorder='big')

        # Additional Count
        ARCOUNT = (0).to_bytes(2, byteorder='big')

        header = TransactionID+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT
        body = b''

        records, rectype, domain = self.getRecords(data[12:])

        question = self.buildQuestion(domain, rectype)

        for record in records:
            body += self.recordToBytes(domain, rectype, record["ttl"], record["value"])

        return header + question + body

    def buildQuestion(self, domain, rectype):
        qbytes = b''

        for part in domain:
            length = len(part)
            qbytes += bytes([length])

            for char in part:
                qbytes += ord(char).to_bytes(1, byteorder='big')

        if rectype == 'a':
            qbytes += (1).to_bytes(2, byteorder='big')

        qbytes += (1).to_bytes(2, byteorder='big')

        return qbytes

    def getFlags(self, flags):
        rflags = ''
        QR = '1'

        byte1 = bytes(flags[:1])
        byte2 = bytes(flags[1:2])

        OPCODE = ''
        for bit in range(1, 5):
            OPCODE += str(ord(byte1) & (1 << bit))

        AA = '1'
        TC = '0'

        # todo: support Recursion
        RD = '0'

        RA = '0'

        # Must be 0, reserved for future use
        Z = '000'

        # Our Response Code
        RCODE = '0000'

        return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big') + int(RA + Z + RCODE, 2).to_bytes(1, byteorder='big')

    def getDomain(self, data):
        state = 0
        expectedlength = 0
        domain = ''
        parts = []
        x = 0
        y = 0

        for byte in data:
            if state == 1:
                if byte != 0:
                    domain += chr(byte)
                x += 1
                if x == expectedlength:
                    parts.append(domain)
                    domain = ''
                    state = 0
                    x = 0
                if byte == 0:
                    parts.append(domain)
                    break
            else:
                state = 1
                expectedlength = byte
            y += 1

        questiontype = data[y:y+2]

        return parts, questiontype

    def getRecords(self, data):
        domain, questiontype = self.getDomain(data)
        qt = ''

        if questiontype == b'\x00\x01':
            qt = 'a'

        zone = self.getZone(domain)

        return zone[qt], qt, domain

    def getZone(self, domain):
        zone_name = '.'.join(domain)
        return self.backend.getZone(zone_name)

    def recordToBytes(self, domain, rectype, recttl, recvalue):
        rbytes = b'\xc0\x0c'

        if rectype == 'a':
            rbytes = rbytes + bytes([0]) + bytes([1])

        rbytes = rbytes + bytes([0]) + bytes([1])

        rbytes += int(recttl).to_bytes(4, byteorder='big')

        if rectype == 'a':
            rbytes = rbytes + bytes([0]) + bytes([4])

            for part in recvalue.split('.'):
                rbytes += bytes([int(part)])

        return rbytes