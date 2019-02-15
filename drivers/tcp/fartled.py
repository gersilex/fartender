import socket


CELL_SCALE = 2


class FartLedTcpDriver:
    sock = None

    def init(self, ip, port):
        self.sock = socket.create_connection((ip, port))
        print("Connected to %s:%d" % self.sock.getpeername())

    def toStream(self, matrix):
        for cell in matrix:
            yield int(cell.get_red() * 255)
            yield int(cell.get_green() * 255)
            yield int(cell.get_blue() * 255)

    def flush(self, matrix):
        bytestream = bytes([CELL_SCALE, 8 * 8] + list(self.toStream(matrix)))
        self.sock.send(bytestream)
