import socket

CELL_SCALE = 2


class FartLedTcpDriver:
    ip = None
    port = None
    sock = None

    def init(self, ip, port):
        self.ip = ip
        self.port = port
        try:
            self.connect()
        except ConnectionError as e:
            print(
                "Error: Could not connect to TCP socket %s:%s : %s"
                % (ip, port, e)
            )
            raise

    def connect(self):
        self.sock = socket.create_connection((self.ip, self.port))
        print("Connected to %s:%d" % self.sock.getpeername())

    def toStream(self, matrix):
        for cell in matrix:
            yield int(cell.get_red() * 255)
            yield int(cell.get_green() * 255)
            yield int(cell.get_blue() * 255)

    def flush(self, matrix):
        bytestream = bytes([CELL_SCALE, 8 * 8] + list(self.toStream(matrix)))
        try:
            self.sock.send(bytestream)
        except ConnectionResetError as e:
            print(e)
            self.connect()
            self.flush(matrix)  # Recurse
