#!/usr/bin/env python3

import drivers.tcp.fartled as driver
import hug
import colour


matrix = [[colour.Color('blue')] * 1] * 2

driver.flush(matrix)


@hug.post('/cell')
def set_cell(row, column, color):
    """Set a single Cell to a Color"""


pass
