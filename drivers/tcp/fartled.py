import socket

sock = socket.create_connection(('192.168.58.131', 41))

CELL_SCALE = 2

print("Connected to %s:%d" % sock.getpeername())


def toStream(matrix):
    for row in matrix:
        for cell in row:
            yield int(cell.get_red() * 255)
            yield int(cell.get_blue() * 255)
            yield int(cell.get_green() * 255)


def flush(matrix):
    sock.send(
        bytes(
            [
                CELL_SCALE,
                1 * 1
            ] + list(toStream(matrix))
        )
    )
