#!/usr/bin/env python3

import drivers.tcp.fartled
import hug
import colour
import time

display = drivers.tcp.fartled.FartLedTcpDriver()
matrix_width = 8
matrix_height = 8

matrix = [colour.Color('blue') for _ in range(matrix_width * 8)]

display.init('192.168.58.131', 41)
display.flush(matrix)


class SerpentineTranslator:
    @staticmethod
    def translate_to_position(row: int, column: int):
        out = 0

        if row % 2 == 0:
            out = row * matrix_width + column
        else:
            out = (row + 1) * matrix_width - column - 1

        return out


@hug.get('/cell')
def set_cell(row: int, column: int, color: str):
    """Set a single Cell to a Color"""

    if not is_valid_position(row, column):
        raise IndexError("Position is out of bounds.")


def is_valid_position(column, row):
    return column in range(matrix_width) and row in range(matrix_height)


pass
