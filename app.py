#!/usr/bin/env python3

import colour
import math
import os

from flask import Flask, request

import drivers.tcp.fartled

display = drivers.tcp.fartled.FartLedTcpDriver()
matrix_width = 8
matrix_height = 8

matrix = [colour.Color("#002000") for _ in range(matrix_width * 8)]
app = Flask(__name__)

display.init(
    os.environ.get("DISPLAY_HOST", "127.0.0.1"),
    os.environ.get("DISPLAY_PORT", 41),
)
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


class LinearTranslator:
    @staticmethod
    def translate_to_position(linear_position: int):
        row = math.floor(linear_position / matrix_width)
        column = linear_position % matrix_width

        return row, column


def is_valid_position(column, row):
    return column in range(matrix_width) and row in range(matrix_height)


@app.after_request
def flush_display(response):
    display.flush(matrix)
    return response


# @app.route('/color/<int:row>/<int:column>', methods=['POST'])
# def set_color(row: int, column: int):
#     """Set a single Cell to a Color"""

#     color = request.json['color']

#     if not is_valid_position(row, column):
#         raise IndexError("Position is out of bounds.")

#     matrix[SerpentineTranslator.translate_to_position(row, column)] = colour.Color(color)
#     display.flush(matrix)
#     return '', 204  # Successful, no content


def set_color_by_natural_index(index: int, color: colour.Color):
    # if color == colour.Color("#00ff00"):
    #     color = colour.Color("#00a000")

    descrambled_index = SerpentineTranslator.translate_to_position(
        *LinearTranslator.translate_to_position(index)
    )
    matrix[descrambled_index] = color


@app.route("/colors", methods=["POST"])
def set_colors():
    colors = request.json["colors"]

    if len(colors) > len(matrix):
        return (
            "Payload Too Large: Your array length of {} elements exceeds the maximum length of {} elements!".format(
                len(colors), len(matrix)
            ),
            413,
        )  # Payload too large

    for i, color in enumerate(colors):
        set_color_by_natural_index(i, colour.Color(color))

    display.flush(matrix)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
