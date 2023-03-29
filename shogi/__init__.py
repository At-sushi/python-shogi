# -*- coding: utf-8 -*-
#
# This file is part of the python-shogi library.
# Copyright (C) 2012-2014 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
# Copyright (C) 2015- Tasuku SUENAGA <tasuku-s-github@titech.ac>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

__author__ = 'Tasuku SUENAGA a.k.a. gunyarakun'
__email__ = 'tasuku-s-github@titech.ac'
__version__ = '1.0.16'

import collections

from .Move import *
from .Piece import *
from .Consts import *

PIECE_TYPES_WITHOUT_KING = [
           PAWN,      LANCE,      KNIGHT,      SILVER,
           GOLD,
         BISHOP,       ROOK,
      PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
    PROM_BISHOP,  PROM_ROOK,         SUI
]

MAX_PIECES_IN_HAND = [0,
        18, 4, 4, 4,
        4,
        2, 2,
        0,
        0, 0, 0, 0,
        0, 0,
]

PIECE_PROMOTED = [
           None,
      PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER,
           None,
    PROM_BISHOP,  PROM_ROOK,
           None,
           None,       None,        None,        None,
           None,       None,    PROM_SUI,        None,
]

NUMBER_JAPANESE_NUMBER_SYMBOLS = [
    '０', '１', '２', '３', '４',
    '５', '６', '７', '８', '９'
]
NUMBER_JAPANESE_KANJI_SYMBOLS = [
    '零', '一', '二', '三', '四',
    '五', '六', '七', '八', '九',
    '十', '十一', '十二', '十三', '十四',
    '十五', '十六', '十七', '十八'
]

STARTING_SFEN = 'lnsgkgsnl/1r2z2b1/ppppppppp/9/9/9/PPPPPPPPP/1B2Z2R1/LNSGKGSNL b - 1'

SQUARES = [
    A9, A8, A7, A6, A5, A4, A3, A2, A1,
    B9, B8, B7, B6, B5, B4, B3, B2, B1,
    C9, C8, C7, C6, C5, C4, C3, C2, C1,
    D9, D8, D7, D6, D5, D4, D3, D2, D1,
    E9, E8, E7, E6, E5, E4, E3, E2, E1,
    F9, F8, F7, F6, F5, F4, F3, F2, F1,
    G9, G8, G7, G6, G5, G4, G3, G2, G1,
    H9, H8, H7, H6, H5, H4, H3, H2, H1,
    I9, I8, I7, I6, I5, I4, I3, I2, I1,
] = range(81)

SQUARES_L90 = [
    A1, B1, C1, D1, E1, F1, G1, H1, I1,
    A2, B2, C2, D2, E2, F2, G2, H2, I2,
    A3, B3, C3, D3, E3, F3, G3, H3, I3,
    A4, B4, C4, D4, E4, F4, G4, H4, I4,
    A5, B5, C5, D5, E5, F5, G5, H5, I5,
    A6, B6, C6, D6, E6, F6, G6, H6, I6,
    A7, B7, C7, D7, E7, F7, G7, H7, I7,
    A8, B8, C8, D8, E8, F8, G8, H8, I8,
    A9, B9, C9, D9, E9, F9, G9, H9, I9,
]

SQUARES_R45 = [
    A9, I8, H7, G6, F5, E4, D3, C2, B1,
    B9, A8, I7, H6, G5, F4, E3, D2, C1,
    C9, B8, A7, I6, H5, G4, F3, E2, D1,
    D9, C8, B7, A6, I5, H4, G3, F2, E1,
    E9, D8, C7, B6, A5, I4, H3, G2, F1,
    F9, E8, D7, C6, B5, A4, I3, H2, G1,
    G9, F8, E7, D6, C5, B4, A3, I2, H1,
    H9, G8, F7, E6, D5, C4, B3, A2, I1,
    I9, H8, G7, F6, E5, D4, C3, B2, A1,
]

SQUARES_L45 = [
    B9, C8, D7, E6, F5, G4, H3, I2, A1,
    C9, D8, E7, F6, G5, H4, I3, A2, B1,
    D9, E8, F7, G6, H5, I4, A3, B2, C1,
    E9, F8, G7, H6, I5, A4, B3, C2, D1,
    F9, G8, H7, I6, A5, B4, C3, D2, E1,
    G9, H8, I7, A6, B5, C4, D3, E2, F1,
    H9, I8, A7, B6, C5, D4, E3, F2, G1,
    I9, A8, B7, C6, D5, E4, F3, G2, H1,
    A9, B8, C7, D6, E5, F4, G3, H2, I1,
]

def file_index(square):
    return square % 9

def rank_index(square):
    return square // 9

BB_VOID = 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000
BB_ALL = 0b111111111111111111111111111111111111111111111111111111111111111111111111111111111

BB_SQUARES = [
    BB_A9, BB_A8, BB_A7, BB_A6, BB_A5, BB_A4, BB_A3, BB_A2, BB_A1,
    BB_B9, BB_B8, BB_B7, BB_B6, BB_B5, BB_B4, BB_B3, BB_B2, BB_B1,
    BB_C9, BB_C8, BB_C7, BB_C6, BB_C5, BB_C4, BB_C3, BB_C2, BB_C1,
    BB_D9, BB_D8, BB_D7, BB_D6, BB_D5, BB_D4, BB_D3, BB_D2, BB_D1,
    BB_E9, BB_E8, BB_E7, BB_E6, BB_E5, BB_E4, BB_E3, BB_E2, BB_E1,
    BB_F9, BB_F8, BB_F7, BB_F6, BB_F5, BB_F4, BB_F3, BB_F2, BB_F1,
    BB_G9, BB_G8, BB_G7, BB_G6, BB_G5, BB_G4, BB_G3, BB_G2, BB_G1,
    BB_H9, BB_H8, BB_H7, BB_H6, BB_H5, BB_H4, BB_H3, BB_H2, BB_H1,
    BB_I9, BB_I8, BB_I7, BB_I6, BB_I5, BB_I4, BB_I3, BB_I2, BB_I1,
] = [1 << i for i in SQUARES]

BB_SQUARES_L90 = [BB_SQUARES[SQUARES_L90[square]] for square in SQUARES]
BB_SQUARES_L45 = [BB_SQUARES[SQUARES_L45[square]] for square in SQUARES]
BB_SQUARES_R45 = [BB_SQUARES[SQUARES_R45[square]] for square in SQUARES]

BB_FILES = [
    BB_FILE_9,
    BB_FILE_8,
    BB_FILE_7,
    BB_FILE_6,
    BB_FILE_5,
    BB_FILE_4,
    BB_FILE_3,
    BB_FILE_2,
    BB_FILE_1,
] = [
    BB_A9 | BB_B9 | BB_C9 | BB_D9 | BB_E9 | BB_F9 | BB_G9 | BB_H9 | BB_I9,
    BB_A8 | BB_B8 | BB_C8 | BB_D8 | BB_E8 | BB_F8 | BB_G8 | BB_H8 | BB_I8,
    BB_A7 | BB_B7 | BB_C7 | BB_D7 | BB_E7 | BB_F7 | BB_G7 | BB_H7 | BB_I7,
    BB_A6 | BB_B6 | BB_C6 | BB_D6 | BB_E6 | BB_F6 | BB_G6 | BB_H6 | BB_I6,
    BB_A5 | BB_B5 | BB_C5 | BB_D5 | BB_E5 | BB_F5 | BB_G5 | BB_H5 | BB_I5,
    BB_A4 | BB_B4 | BB_C4 | BB_D4 | BB_E4 | BB_F4 | BB_G4 | BB_H4 | BB_I4,
    BB_A3 | BB_B3 | BB_C3 | BB_D3 | BB_E3 | BB_F3 | BB_G3 | BB_H3 | BB_I3,
    BB_A2 | BB_B2 | BB_C2 | BB_D2 | BB_E2 | BB_F2 | BB_G2 | BB_H2 | BB_I2,
    BB_A1 | BB_B1 | BB_C1 | BB_D1 | BB_E1 | BB_F1 | BB_G1 | BB_H1 | BB_I1,
]

BB_RANKS = [
    BB_RANK_A,
    BB_RANK_B,
    BB_RANK_C,
    BB_RANK_D,
    BB_RANK_E,
    BB_RANK_F,
    BB_RANK_G,
    BB_RANK_H,
    BB_RANK_I
] = [
    BB_A1 | BB_A2 | BB_A3 | BB_A4 | BB_A5 | BB_A6 | BB_A7 | BB_A8 | BB_A9,
    BB_B1 | BB_B2 | BB_B3 | BB_B4 | BB_B5 | BB_B6 | BB_B7 | BB_B8 | BB_B9,
    BB_C1 | BB_C2 | BB_C3 | BB_C4 | BB_C5 | BB_C6 | BB_C7 | BB_C8 | BB_C9,
    BB_D1 | BB_D2 | BB_D3 | BB_D4 | BB_D5 | BB_D6 | BB_D7 | BB_D8 | BB_D9,
    BB_E1 | BB_E2 | BB_E3 | BB_E4 | BB_E5 | BB_E6 | BB_E7 | BB_E8 | BB_E9,
    BB_F1 | BB_F2 | BB_F3 | BB_F4 | BB_F5 | BB_F6 | BB_F7 | BB_F8 | BB_F9,
    BB_G1 | BB_G2 | BB_G3 | BB_G4 | BB_G5 | BB_G6 | BB_G7 | BB_G8 | BB_G9,
    BB_H1 | BB_H2 | BB_H3 | BB_H4 | BB_H5 | BB_H6 | BB_H7 | BB_H8 | BB_H9,
    BB_I1 | BB_I2 | BB_I3 | BB_I4 | BB_I5 | BB_I6 | BB_I7 | BB_I8 | BB_I9,
]


def shift_down(b):
    return (b << 9) & BB_ALL


def shift_2_down(b):
    return (b << 18) & BB_ALL


def shift_up(b):
    return b >> 9


def shift_2_up(b):
    return b >> 18


def shift_right(b):
    return (b << 1) & ~BB_FILE_9


def shift_2_right(b):
    return (b << 2) & ~BB_FILE_9 & ~BB_FILE_8


def shift_left(b):
    return (b >> 1) & ~BB_FILE_1


def shift_2_left(b):
    return (b >> 2) & ~BB_FILE_1 & ~BB_FILE_2


def shift_up_left(b):
    return (b >> 10) & ~BB_FILE_1


def shift_up_right(b):
    return (b >> 8) & ~BB_FILE_9


def shift_down_left(b):
    return (b << 8) & ~BB_FILE_1


def shift_down_right(b):
    return (b << 10) & ~BB_FILE_9

BB_PAWN_ATTACKS = [
    [shift_up(s) for s in BB_SQUARES],
    [shift_down(s) for s in BB_SQUARES],
]
BB_KNIGHT_ATTACKS = [[], []]
BB_SILVER_ATTACKS = [[], []]
BB_GOLD_ATTACKS = [[], []]
BB_KING_ATTACKS = []
BB_SUI_ATTACKS = [[], []]

for bb_square in BB_SQUARES:
    mask = BB_VOID
    mask |= shift_left(shift_2_up(bb_square))
    mask |= shift_right(shift_2_up(bb_square))

    BB_KNIGHT_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_left(shift_2_down(bb_square))
    mask |= shift_right(shift_2_down(bb_square))

    BB_KNIGHT_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_up_left(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)

    BB_SILVER_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_down_left(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_down_right(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)

    BB_SILVER_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_up_left(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_down(bb_square)

    BB_GOLD_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_down_left(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_down_right(bb_square)
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_up(bb_square)

    BB_GOLD_ATTACKS[WHITE].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)
    BB_KING_ATTACKS.append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_up(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)
    BB_SUI_ATTACKS[BLACK].append(mask & BB_ALL)

    mask = BB_VOID
    mask |= shift_left(bb_square)
    mask |= shift_right(bb_square)
    mask |= shift_down(bb_square)
    mask |= shift_up_left(bb_square)
    mask |= shift_up_right(bb_square)
    mask |= shift_down_left(bb_square)
    mask |= shift_down_right(bb_square)
    BB_SUI_ATTACKS[WHITE].append(mask & BB_ALL)

# 128 means 2 ^ (9 - 1 - 1), patterns of emptiness of one row without each ends
BB_RANK_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]
BB_FILE_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]
BB_LANCE_ATTACKS = [
    [[BB_VOID for i in range(128)] for k in SQUARES],
    [[BB_VOID for i in range(128)] for k in SQUARES],
]

for square in SQUARES:
    for bitrow in range(0, 128):
        f = file_index(square) + 1
        q = square + 1
        while f < 9:
            BB_RANK_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << f) & (bitrow << 1):
                break
            q += 1
            f += 1

        f = file_index(square) - 1
        q = square - 1
        while f >= 0:
            BB_RANK_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            if (1 << f) & (bitrow << 1):
                break
            q -= 1
            f -= 1

        r = rank_index(square) + 1
        q = square + 9
        while r < 9:
            BB_FILE_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            BB_LANCE_ATTACKS[WHITE][square][bitrow] |= BB_SQUARES[q]
            if (1 << (8 - r)) & (bitrow << 1):
                break
            q += 9
            r += 1

        r = rank_index(square) - 1
        q = square - 9
        while r >= 0:
            BB_FILE_ATTACKS[square][bitrow] |= BB_SQUARES[q]
            BB_LANCE_ATTACKS[BLACK][square][bitrow] |= BB_SQUARES[q]
            if (1 << (8 - r)) & (bitrow << 1):
                break
            q -= 9
            r -= 1

BB_SHIFT_R45 = [
     1, 73, 65, 57, 49, 41, 33, 25, 17,
    10,  1, 73, 65, 57, 49, 41, 33, 25,
    19, 10,  1, 73, 65, 57, 49, 41, 33,
    28, 19, 10,  1, 73, 65, 57, 49, 41,
    36, 28, 19, 10,  1, 73, 65, 57, 49,
    45, 36, 28, 19, 10,  1, 73, 65, 57,
    54, 45, 36, 28, 19, 10,  1, 73, 65,
    63, 54, 45, 36, 28, 19, 10,  1, 73,
    72, 63, 54, 45, 36, 28, 19, 10,  1
]

BB_SHIFT_L45 = [
    10, 19, 28, 36, 45, 54, 63, 72,  1,
    19, 28, 36, 45, 54, 63, 72,  1, 11,
    28, 36, 45, 54, 63, 72,  1, 11, 21,
    36, 45, 54, 63, 72,  1, 11, 21, 31,
    45, 54, 63, 72,  1, 11, 21, 31, 41,
    54, 63, 72,  1, 11, 21, 31, 41, 51,
    63, 72,  1, 11, 21, 31, 41, 51, 61,
    72,  1, 11, 21, 31, 41, 51, 61, 71,
     1, 11, 21, 31, 41, 51, 61, 71, 81
]

BB_L45_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]
BB_R45_ATTACKS = [[BB_VOID for i in range(128)] for k in SQUARES]

for s in SQUARES:
    for b in range(0, 128):
        mask = BB_VOID

        q = s
        while file_index(q) > 0 and rank_index(q) < 8:
            q += 8
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_L45[q] >> BB_SHIFT_L45[s]):
                break

        q = s
        while file_index(q) < 8 and rank_index(q) > 0:
            q -= 8
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_L45[q] >> BB_SHIFT_L45[s]):
                break

        BB_L45_ATTACKS[s][b] = mask

        mask = BB_VOID

        q = s
        while file_index(q) < 8 and rank_index(q) < 8:
            q += 10
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_R45[q] >> BB_SHIFT_R45[s]):
                break

        q = s
        while file_index(q) > 0 and rank_index(q) > 0:
            q -= 10
            mask |= BB_SQUARES[q]
            if b & (BB_SQUARES_R45[q] >> BB_SHIFT_R45[s]):
                break

        BB_R45_ATTACKS[s][b] = mask

try:
    from gmpy2 import popcount as pop_count
    from gmpy2 import bit_scan1 as bit_scan
except ImportError:
    try:
        from gmpy import popcount as pop_count
        from gmpy import scan1 as bit_scan
    except ImportError:
        def pop_count(b):
            return bin(b).count('1')

        def bit_scan(b, n=0):
            string = bin(b)
            l = len(string)
            r = string.rfind('1', 0, l - n)
            if r == -1:
                return -1
            else:
                return l - r - 1

def can_promote(square, piece_type, color):
    if piece_type not in [PAWN, LANCE, KNIGHT, SILVER, BISHOP, ROOK, SUI]:
        return False
    elif color == BLACK:
        return rank_index(square) <= 2
    else:
        return rank_index(square) >= 6

def can_move_without_promotion(to_square, piece_type, color):
    if color == BLACK:
        return ((piece_type != PAWN and piece_type != LANCE and piece_type != KNIGHT) or
                (piece_type == PAWN and rank_index(to_square) > 0) or
                (piece_type == LANCE and rank_index(to_square) > 0) or
                (piece_type == KNIGHT and rank_index(to_square) > 1) )
    else:
        return ((piece_type != PAWN and piece_type != LANCE and piece_type != KNIGHT) or
                (piece_type == PAWN and rank_index(to_square) < 8) or
                (piece_type == LANCE and rank_index(to_square) < 8) or
                (piece_type == KNIGHT and rank_index(to_square) < 7) )


class Occupied(object):
    def __init__(self, occupied_by_black, occupied_by_white):
        self.by_color = [occupied_by_black, occupied_by_white]
        self.bits = occupied_by_black | occupied_by_white
        self.l45 = BB_VOID
        self.r45 = BB_VOID
        self.l90 = BB_VOID
        self.update_rotated()

    def update_rotated(self):
        for i in SQUARES:
            if BB_SQUARES[i] & self.bits:
                self.l90 |= BB_SQUARES_L90[i]
                self.r45 |= BB_SQUARES_R45[i]
                self.l45 |= BB_SQUARES_L45[i]

    def __getitem__(self, key):
        if key in COLORS:
            return self.by_color[key]
        raise KeyError('Occupied must be looked up with shogi.BLACK or shogi.WHITE')

    def ixor(self, mask, color, square):
        self.bits ^= mask
        self.by_color[color] ^= mask
        self.l90 ^= BB_SQUARES[SQUARES_L90[square]]
        self.r45 ^= BB_SQUARES[SQUARES_R45[square]]
        self.l45 ^= BB_SQUARES[SQUARES_L45[square]]

    def non_occupied(self):
        return ~self.bits & BB_ALL

    def __eq__(self, occupied):
        return not self.__ne__(occupied)

    def __ne__(self, occupied):
        if self.by_color[BLACK] != occupied.by_color[BLACK]:
            return True
        if self.by_color[WHITE] != occupied.by_color[WHITE]:
            return True
        return False

    def __repr__(self):
        return 'Occupied({0})'.format(repr(self.by_color))


class Board(object):
    '''
    A bitboard and additional information representing a position.
    Provides move generation, validation, parsing, attack generation,
    game end detection, move counters and the capability to make and unmake
    moves.
    The bitboard is initialized to the starting position, unless otherwise
    specified in the optional `sfen` argument.
    '''

    def __init__(self, sfen=None):
        self.pseudo_legal_moves = PseudoLegalMoveGenerator(self)
        self.legal_moves = LegalMoveGenerator(self)

        if sfen is None:
            self.reset()
        else:
            self.set_sfen(sfen)

    def reset(self):
        '''Restores the starting position.'''
        self.piece_bb = [
                BB_VOID,                       # NONE
                BB_RANK_C | BB_RANK_G,         # PAWN
                BB_A1 | BB_I1 | BB_A9 | BB_I9, # LANCE
                BB_A2 | BB_A8 | BB_I2 | BB_I8, # KNIGHT
                BB_A3 | BB_A7 | BB_I3 | BB_I7, # SILVER
                BB_A4 | BB_A6 | BB_I4 | BB_I6, # GOLD
                BB_B2 | BB_H8,                 # BISHOP
                BB_B8 | BB_H2,                 # ROOK
                BB_A5 | BB_I5,                 # KING
                BB_VOID,                       # PROM_PAWN
                BB_VOID,                       # PROM_LANCE
                BB_VOID,                       # PROM_KNIGHT
                BB_VOID,                       # PROM_SILVER
                BB_VOID,                       # PROM_BISHOP
                BB_VOID,                       # PROM_ROOK
                BB_B5 | BB_H5,                 # SUI
                BB_VOID,                       # PROM_SUI
        ]

        self.pieces_in_hand = [collections.Counter(), collections.Counter()]

        self.occupied = Occupied(BB_RANK_G | BB_H2 | BB_H5 | BB_H8 | BB_RANK_I, BB_RANK_A | BB_B2 | BB_B5 | BB_B8 | BB_RANK_C)

        self.king_squares = [I5, A5]
        self.promsui_squares = [H5, B5]
        self.pieces = [NONE for i in SQUARES]
        self.kings_living = [1, 1]

        for i in SQUARES:
            mask = BB_SQUARES[i]
            for piece_type in PIECE_TYPES:
                if mask & self.piece_bb[piece_type]:
                    self.pieces[i] = piece_type

        self.turn = BLACK
        self.move_number = 1
        self.captured_piece_stack = collections.deque()
        self.move_stack = collections.deque()
        self.incremental_zobrist_hash = self.board_zobrist_hash(DEFAULT_RANDOM_ARRAY)
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def clear(self):
        self.piece_bb = [
                BB_VOID,                       # NONE
                BB_VOID,                       # PAWN
                BB_VOID,                       # LANCE
                BB_VOID,                       # KNIGHT
                BB_VOID,                       # SILVER
                BB_VOID,                       # GOLD
                BB_VOID,                       # BISHOP
                BB_VOID,                       # ROOK
                BB_VOID,                       # KING
                BB_VOID,                       # PROM_PAWN
                BB_VOID,                       # PROM_LANCE
                BB_VOID,                       # PROM_KNIGHT
                BB_VOID,                       # PROM_SILVER
                BB_VOID,                       # PROM_BISHOP
                BB_VOID,                       # PROM_ROOK
                BB_VOID,                       # SUI
                BB_VOID,                       # PROM_SUI
        ]

        self.pieces_in_hand = [collections.Counter(), collections.Counter()]

        self.occupied = Occupied(BB_VOID, BB_VOID)

        self.king_squares = [None, None]
        self.promsui_squares = [None, None]
        self.pieces = [NONE for i in SQUARES]
        self.kings_living = [0, 0]

        self.turn = BLACK
        self.move_number = 1
        self.captured_piece_stack = collections.deque()
        self.move_stack = collections.deque()
        self.incremental_zobrist_hash = self.board_zobrist_hash(DEFAULT_RANDOM_ARRAY)
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def piece_at(self, square):
        '''Gets the piece at the given square.'''
        mask = BB_SQUARES[square]
        color = int(bool(self.occupied[WHITE] & mask))

        piece_type = self.piece_type_at(square)
        if piece_type:
            return Piece(piece_type, color)

    def piece_type_at(self, square):
        '''Gets the piece type at the given square.'''
        return self.pieces[square]

    def add_piece_into_hand(self, piece_type, color, count=1):
        p = self.pieces_in_hand[color]

        if piece_type in [KING, SUI, PROM_SUI]:
            return

        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        p[piece_type] += count

    def remove_piece_from_hand(self, piece_type, color):
        p = self.pieces_in_hand[color]
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        p[piece_type] -= 1
        if p[piece_type] == 0:
            del p[piece_type]
        elif p[piece_type] < 0:
            raise ValueError('The piece is not in hand: {0}'.format(Piece(piece_type, self.turn)))

    def has_piece_in_hand(self, piece_type, color):
        if piece_type >= PROM_PAWN:
            piece_type = PIECE_PROMOTED.index(piece_type)
        return piece_type in self.pieces_in_hand[color]

    def remove_piece_at(self, square, into_hand=False):
        '''Removes a piece from the given square if present.'''
        piece_type = self.piece_type_at(square)

        if piece_type == NONE:
            return

        if into_hand:
            self.add_piece_into_hand(piece_type, self.turn)

        mask = BB_SQUARES[square]

        self.piece_bb[piece_type] ^= mask

        color = int(bool(self.occupied[WHITE] & mask))

        self.pieces[square] = NONE
        self.occupied.ixor(mask, color, square)

        if piece_type in [KING, PROM_SUI]:
            self.kings_living[color] -= 1

        # Update incremental zobrist hash.
        if color == BLACK:
            piece_index = (piece_type - 1) * 2
        else:
            piece_index = (piece_type - 1) * 2 + 1
        self.incremental_zobrist_hash ^= DEFAULT_RANDOM_ARRAY[81 * piece_index + 9 * rank_index(square) + file_index(square)]

    def set_piece_at(self, square, piece, from_hand=False, into_hand=False):
        '''Sets a piece at the given square. An existing piece is replaced.'''
        if from_hand:
            self.remove_piece_from_hand(piece.piece_type, self.turn)

        self.remove_piece_at(square, into_hand)

        self.pieces[square] = piece.piece_type

        mask = BB_SQUARES[square]

        piece_type = piece.piece_type

        self.piece_bb[piece_type] |= mask

        if piece_type == KING:
            self.king_squares[piece.color] = square
            self.kings_living[piece.color] += 1
        if piece_type == PROM_SUI:
            self.promsui_squares[piece.color] = square
            self.kings_living[piece.color] += 1

        self.occupied.ixor(mask, piece.color, square)

        # Update incremental zorbist hash.
        if piece.color == BLACK:
            piece_index = (piece.piece_type - 1) * 2
        else:
            piece_index = (piece.piece_type - 1) * 2 + 1
        self.incremental_zobrist_hash ^= DEFAULT_RANDOM_ARRAY[81 * piece_index + 9 * rank_index(square) + file_index(square)]

    def generate_pseudo_legal_moves(self, pawns=True, lances=True, knights=True, silvers=True, golds=True,
            bishops=True, rooks=True,
            kings=True,
            prom_pawns=True, prom_lances=True, prom_knights=True, prom_silvers=True, prom_bishops=True, prom_rooks=True,
            pawns_drop=True, lances_drop=True, knights_drop=True, silvers_drop=True, golds_drop=True,
            bishops_drop=True, rooks_drop=True, sui=True, prom_sui=True):

        move_flags = [False,
                      pawns, lances, knights, silvers,
                      golds, bishops, rooks,
                      kings,
                      prom_pawns, prom_lances, prom_knights, prom_silvers,
                      prom_bishops, prom_rooks, sui, prom_sui]
        drop_flags = [False,
                      pawns_drop, lances_drop, knights_drop, silvers_drop,
                      golds_drop, bishops_drop, rooks_drop]

        for piece_type in PIECE_TYPES:
            # piece move
            if move_flags[piece_type]:
                movers = self.piece_bb[piece_type] & self.occupied[self.turn]
                from_square = bit_scan(movers)

                while from_square != -1 and from_square is not None:
                    moves = Board.attacks_from(piece_type, from_square, self.occupied, self.turn) & ~self.occupied[self.turn]
                    to_square = bit_scan(moves)
                    while to_square != - 1 and to_square is not None:
                        if can_move_without_promotion(to_square, piece_type, self.turn):
                            yield Move(from_square, to_square)
                        if can_promote(from_square, piece_type, self.turn) or can_promote(to_square, piece_type, self.turn):
                            yield Move(from_square, to_square, True)
                        to_square = bit_scan(moves, to_square + 1)
                    from_square = bit_scan(movers, from_square + 1)

        # Drop pieces in hand.
        moves = self.occupied.non_occupied()
        to_square = bit_scan(moves)

        while to_square != -1 and to_square is not None:
            for piece_type in range(PAWN, KING):
                # Check having the piece in hand, can move after place
                # and double pawn
                if drop_flags[piece_type] and self.has_piece_in_hand(piece_type, self.turn) and \
                        can_move_without_promotion(to_square, piece_type, self.turn) and \
                        not self.is_double_pawn(to_square, piece_type):
                    yield Move(None, to_square, False, piece_type)

            to_square = bit_scan(moves, to_square + 1)

    def is_attacked_by(self, color, square, piece_types=PIECE_TYPES):
        if square is None:
            return False

        for piece_type in piece_types:
            is_attacked = Board.attacks_from(piece_type, square, self.occupied, color ^ 1) & self.piece_bb[piece_type] & self.occupied[color]
            if is_attacked:
                return True

        return False

    def attacker_mask(self, color, square):
        attackers = BB_VOID
        for piece_type in PIECE_TYPES:
            attackers |= Board.attacks_from(piece_type, square, self.occupied, color ^ 1) & self.piece_bb[piece_type]
        return attackers & self.occupied[color]

    def attackers(self, color, square):
        return SquareSet(self.attacker_mask(color, square))

    def is_check(self):
        return self.kings_living[self.turn] == 1 and (self.is_attacked_by(self.turn ^ 1,
            self.king_squares[self.turn]) or self.is_attacked_by(self.turn ^ 1, self.promsui_squares[self.turn]))

    @staticmethod
    def attacks_from(piece_type, square, occupied, move_color):
        if piece_type == NONE:
            return BB_VOID
        if piece_type == PAWN:
            return BB_PAWN_ATTACKS[move_color][square]
        elif piece_type == LANCE:
            return BB_LANCE_ATTACKS[move_color][square][(occupied.l90 >> (((square % 9) * 9) + 1)) & 127]
        elif piece_type == KNIGHT:
            return BB_KNIGHT_ATTACKS[move_color][square]
        elif piece_type == SILVER:
            return BB_SILVER_ATTACKS[move_color][square]
        elif piece_type in [GOLD, PROM_PAWN, PROM_LANCE, PROM_KNIGHT, PROM_SILVER]:
            return BB_GOLD_ATTACKS[move_color][square]
        elif piece_type == BISHOP:
            return (BB_R45_ATTACKS[square][(occupied.r45 >> BB_SHIFT_R45[square]) & 127] |
                    BB_L45_ATTACKS[square][(occupied.l45 >> BB_SHIFT_L45[square]) & 127])
        elif piece_type == ROOK:
            return (BB_RANK_ATTACKS[square][(occupied.bits >> (((square // 9) * 9) + 1)) & 127] |
                    BB_FILE_ATTACKS[square][(occupied.l90 >> (((square % 9) * 9) + 1)) & 127])
        elif piece_type in [KING, PROM_SUI]:
            return BB_KING_ATTACKS[square]
        elif piece_type == PROM_BISHOP:
            return (BB_KING_ATTACKS[square] |
                    BB_R45_ATTACKS[square][(occupied.r45 >> BB_SHIFT_R45[square]) & 127] |
                    BB_L45_ATTACKS[square][(occupied.l45 >> BB_SHIFT_L45[square]) & 127])
        elif piece_type == PROM_ROOK:
            return (BB_KING_ATTACKS[square] |
                    BB_RANK_ATTACKS[square][(occupied.bits >> (((square // 9) * 9) + 1)) & 127] |
                    BB_FILE_ATTACKS[square][(occupied.l90 >> (((square % 9) * 9) + 1)) & 127])
        elif piece_type == SUI:
            return BB_SUI_ATTACKS[move_color][square]

    def is_suicide_or_check_by_dropping_pawn(self, move):
        '''
        Checks if the given move would move would leave the king in check or
        put it into check.
        '''

        self.push(move)
        is_suicide = self.was_suicide()
        is_check_by_dropping_pawn = self.was_check_by_dropping_pawn(move)
        self.pop()
        return is_suicide or is_check_by_dropping_pawn

    def was_suicide(self):
        '''
        Checks if the king of the other side is attacked. Such a position is not
        valid and could only be reached by an illegal move.
        '''
        return self.kings_living[self.turn ^ 1] == 1 and (self.is_attacked_by(self.turn,
            self.king_squares[self.turn ^ 1]) or self.is_attacked_by(self.turn, self.promsui_squares[self.turn ^ 1]))

    def was_check_by_dropping_pawn(self, move):
        # NOTE: We ignore the case "Saigo no shinpan" (by Koji Nuita, 1997)
        # We don't use is_checkmate() because it's slow due to generating all leagl moves
        # And we don't consider suicide of a king.

        pawn_square = move.to_square

        # Pawn is dropped?
        if move.drop_piece_type != PAWN:
            return False

        if self.kings_living[self.turn] > 1:
            return False

        king_square = self.king_squares[self.turn]


        # Does king exist?
        if king_square is None:
            if self.promsui_squares[self.turn] is None:
                return False
            else:
                king_square = self.promsui_squares[self.turn]

        # Pawn can capture a king next move?
        moves = BB_PAWN_ATTACKS[self.turn ^ 1][pawn_square] & ~self.occupied[self.turn ^ 1]
        if not moves & BB_SQUARES[king_square]:
            return False

        # Can king escape? (including capturing a dropped pawn)
        moves = Board.attacks_from(KING, king_square, self.occupied, self.turn) & ~self.occupied[self.turn]
        square = bit_scan(moves)
        while square != -1 and square is not None:
            if not self.is_attacked_by(self.turn ^ 1, square):
                return False
            square = bit_scan(moves, square + 1)

        # Pieces besides king can capture the pawn?
        if self.is_attacked_by(self.turn, pawn_square, PIECE_TYPES_WITHOUT_KING):
            return False

        return True

    def generate_legal_moves(self, pawns=True, lances=True, knights=True, silvers=True, golds=True, bishops=True,
            rooks=True, king=True,
            pawns_drop=True, lances_drop=True, knights_drop=True, silvers_drop=True, golds_drop=True,
            bishops_drop=True, rooks_drop=True, sui=True,prom_sui=True):
        return (move for move in self.generate_pseudo_legal_moves(
                pawns, lances, knights, silvers, golds, bishops, rooks, king,
                pawns_drop, lances_drop, knights_drop, silvers_drop, golds_drop, bishops_drop, rooks_drop
            , sui, prom_sui) if not self.is_suicide_or_check_by_dropping_pawn(move))

    def is_pseudo_legal(self, move):
        # Null moves are not pseudo legal.
        if not move:
            return False

        # Get square masks of the move destination.
        to_mask = BB_SQUARES[move.to_square]

        # Destination square can not be occupied by self.
        if self.occupied[self.turn] & to_mask:
            return False

        if move.from_square is not None:
            from_mask = BB_SQUARES[move.from_square]
            # Source square must not be vacant.
            piece = self.piece_type_at(move.from_square)
            if not piece:
                return False
            # Check turn.
            if not self.occupied[self.turn] & from_mask:
                return False

            # Promotion check
            if move.promotion:
                if piece == GOLD or piece == KING or piece >= PROM_PAWN:
                    return False
                if self.turn == BLACK and rank_index(move.to_square) > 2 and rank_index(move.from_square) > 2:
                    return False
                elif self.turn == WHITE and rank_index(move.to_square) < 6 and rank_index(move.from_square) < 6:
                    return False

            # Can move without promotion
            if not move.promotion and not can_move_without_promotion(move.to_square, piece, self.turn):
                return False

            # Handle moves by piece type.
            return bool(Board.attacks_from(piece, move.from_square, self.occupied, self.turn) & to_mask)
        elif move.drop_piece_type:
            # Cannot set promoted piece
            if move.promotion:
                return False

            # Have a piece in hand
            if not self.has_piece_in_hand(move.drop_piece_type, self.turn):
                return False

            # Can move without promotion
            if not can_move_without_promotion(move.to_square, move.drop_piece_type, self.turn):
                return False

            # Not double pawn
            if self.is_double_pawn(move.to_square, move.drop_piece_type):
                return False

            return True
        else:
            # Drop piece or move piece
            return False

    def is_legal(self, move):
        return self.is_pseudo_legal(move) and not self.is_suicide_or_check_by_dropping_pawn(move)

    def is_game_over(self):
        '''
        Checks if the game is over due to checkmate, stalemate or
        fourfold repetition.
        '''

        # Stalemate or checkmate.
        try:
            next(self.generate_legal_moves().__iter__())
        except StopIteration:
            return True

        # Fourfold repetition.
        if self.is_fourfold_repetition():
            return True

        return False

    def is_checkmate(self):
        '''Checks if the current position is a checkmate.'''
        if not self.is_check():
            return False

        try:
            next(self.generate_legal_moves().__iter__())
            return False
        except StopIteration:
            return True

    def is_stalemate(self):
        '''Checks if the current position is a stalemate.'''
        if self.is_check():
            return False

        try:
            next(self.generate_legal_moves().__iter__())
            return False
        except StopIteration:
            return True

    def is_fourfold_repetition(self):
        '''
        a game is ended if a position occurs for the fourth time
        on consecutive alternating moves.
        '''
        zobrist_hash = self.zobrist_hash()

        # A minimum amount of moves must have been played and the position
        # in question must have appeared at least four times.
        if self.transpositions[zobrist_hash] < 4:
            return False

        return True

    def is_double_pawn(self, to_square, piece_type):
        if piece_type != PAWN:
            return False
        return self.piece_bb[PAWN] & self.occupied[self.turn] & BB_FILES[file_index(to_square)]

    def push_usi_position_cmd(self, usi_position_cmd):
        '''
        Updates the position from position command in USI protocol.

        Example:
        >>> board.push_usi_position_cmd("position startpos moves 7g7f 3c3d")
        '''
        if usi_position_cmd.startswith("position startpos") or usi_position_cmd.startswith("position sfen"):
            sfen_id = usi_position_cmd.find("sfen")
            moves_id = usi_position_cmd.find("moves")
        else:
            raise ValueError("Invalid command {0} position cmd in USI protocol must starts from 'position startpos' or 'position sfen'".format(repr(usi_position_cmd)))

        if sfen_id != -1:
            if moves_id != -1:
                sfen = usi_position_cmd[sfen_id+5:moves_id]
            else:
                sfen = usi_position_cmd[sfen_id+5:]
            self.set_sfen(sfen)
        else:
            self.reset()

        if moves_id != -1:
            moves = usi_position_cmd[moves_id+6:].split(" ")
            for move in moves:
                if move != "":
                    self.push_usi(move)

    def push(self, move):
        '''
        Updates the position with the given move and puts it onto a stack.
        Null moves just increment the move counters, switch turns and forfeit
        en passant capturing.
        No validation is performed. For performance moves are assumed to be at
        least pseudo legal. Otherwise there is no guarantee that the previous
        board state can be restored. To check it yourself you can use:
        >>> move in board.pseudo_legal_moves
        True
        '''
        # Increment move number.
        self.move_number += 1

        # Remember game state.
        captured_piece = self.piece_type_at(move.to_square) if move else NONE
        self.captured_piece_stack.append(captured_piece)
        self.move_stack.append(move)

        # On a null move simply swap turns.
        if not move:
            self.turn ^= 1
            return

        if move.drop_piece_type:
            # Drops.
            piece_type = move.drop_piece_type
            from_hand = True
        else:
            # Promotion.
            piece_type = self.piece_type_at(move.from_square)
            from_hand = False

            if move.promotion:
                piece_type = PIECE_PROMOTED[piece_type]

            # Remove piece from target square.
            self.remove_piece_at(move.from_square, False)

        # Put piece on target square.
        self.set_piece_at(move.to_square, Piece(piece_type, self.turn), from_hand, True)

        # Swap turn.
        self.turn ^= 1

        # Update transposition table.
        self.transpositions.update((self.zobrist_hash(), ))

    def pop(self):
        '''
        Restores the previous position and returns the last move from the stack.
        '''
        move = self.move_stack.pop()

        # Update transposition table.
        self.transpositions.subtract((self.zobrist_hash(), ))

        # Decrement move number.
        self.move_number -= 1

        # Restore state.
        captured_piece_type = self.captured_piece_stack.pop()
        captured_piece_color = self.turn

        # On a null move simply swap the turn.
        if not move:
            self.turn ^= 1
            return move

        # Restore the source square.
        piece_type = self.piece_type_at(move.to_square)
        if move.promotion:
            piece_type = PIECE_PROMOTED.index(piece_type)

        if move.from_square is None:
            self.add_piece_into_hand(piece_type, self.turn ^ 1)
        else:
            self.set_piece_at(move.from_square, Piece(piece_type, self.turn ^ 1))

        # Restore target square.
        if captured_piece_type:
            self.remove_piece_from_hand(captured_piece_type, captured_piece_color ^ 1)
            self.set_piece_at(move.to_square, Piece(captured_piece_type, captured_piece_color))
        else:
            self.remove_piece_at(move.to_square)

        # Swap turn.
        self.turn ^= 1

        return move

    def peek(self):
        '''Gets the last move from the move stack.'''
        return self.move_stack[-1]

    def sfen(self):
        '''
        Gets an SFEN representation of the current position.
        '''
        sfen = []
        empty = 0

        # Position part.
        for square in SQUARES:
            piece = self.piece_at(square)

            if not piece:
                empty += 1
            else:
                if empty:
                    sfen.append(str(empty))
                    empty = 0
                sfen.append(piece.symbol())

            if BB_SQUARES[square] & BB_FILE_1:
                if empty:
                    sfen.append(str(empty))
                    empty = 0

                if square != I1:
                    sfen.append('/')

        sfen.append(' ')

        # Side to move.
        if self.turn == WHITE:
            sfen.append('w')
        else:
            sfen.append('b')

        sfen.append(' ')

        # Pieces in hand
        pih_len = 0
        for color in COLORS:
            p = self.pieces_in_hand[color]
            pih_len += len(p)
            for piece_type in sorted(p.keys(), reverse=True):
                if p[piece_type] >= 1:
                    if p[piece_type] > 1:
                        sfen.append(str(p[piece_type]))
                    piece = Piece(piece_type, color)
                    sfen.append(piece.symbol())
        if pih_len == 0:
            sfen.append('-')

        sfen.append(' ')

        # Move count
        sfen.append(str(self.move_number))

        return ''.join(sfen)

    def set_sfen(self, sfen):
        '''
        Parses a SFEN and sets the position from it.
        Rasies `ValueError` if the SFEN string is invalid.
        '''
        # Ensure there are six parts.
        parts = sfen.split()
        if len(parts) != 4:
            raise ValueError('sfen string should consist of 6 parts: {0}'.format(repr(sfen)))

        # Ensure the board part is valid.
        rows = parts[0].split('/')
        if len(rows) != 9:
            raise ValueError('expected 9 rows in position part of sfen: {0}'.format(repr(sfen)))

        # Validate each row.
        for row in rows:
            field_sum = 0
            previous_was_digit = False
            previous_was_plus = False

            for c in row:
                if c in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if previous_was_digit:
                        raise ValueError('two subsequent digits in position part of sfen: {0}'.format(repr(sfen)))
                    if previous_was_plus:
                        raise ValueError('Cannot promote squares in position part of sfen: {0}'.format(repr(sfen)))
                    field_sum += int(c)
                    previous_was_digit = True
                    previous_was_plus = False
                elif c == '+':
                    if previous_was_plus:
                        raise ValueError('Double promotion prefixes in position part of sfen: {0}'.format(repr(sfen)))
                    previous_was_digit = False
                    previous_was_plus = True
                elif c.lower() in ['p', 'l', 'n', 's', 'g', 'b', 'r', 'k', 'z']:
                    field_sum += 1
                    if previous_was_plus and (c.lower() == 'g' or c.lower() == 'k'):
                      raise ValueError('Gold and King cannot promote in position part of sfen: {0}')
                    previous_was_digit = False
                    previous_was_plus = False
                else:
                    raise ValueError('invalid character in position part of sfen: {0}'.format(repr(sfen)))

            if field_sum != 9:
                raise ValueError('expected 9 columns per row in position part of sfen: {0}'.format(repr(sfen)))

        # Check that the turn part is valid.
        if not parts[1] in ['b', 'w']:
            raise ValueError("expected 'b' or 'w' for turn part of sfen: {0}".format(repr(sfen)))

        # Check pieces in hand is valid.
        # TODO: implement with checking parts[2]

        # Check that the fullmove number part is valid.
        # 0 is allowed for compability but later replaced with 1.
        if int(parts[3]) < 0:
            raise ValueError('fullmove number must be positive: {0}'.format(repr(sfen)))

        # Clear board.
        self.clear()

        # Put pieces on the board.
        square_index = 0
        previous_was_plus = False
        for c in parts[0]:
            if c in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                square_index += int(c)
            elif c == '+':
                previous_was_plus = True
            elif c == '/':
                pass
            else:
                piece_symbol = c
                if previous_was_plus:
                  piece_symbol = '+' + piece_symbol
                self.set_piece_at(square_index, Piece.from_symbol(piece_symbol))
                square_index += 1
                previous_was_plus = False

        # Set the turn.
        if parts[1] == 'w':
            self.turn = WHITE
        else:
            self.turn = BLACK

        # Set the pieces in hand
        self.pieces_in_hand = [collections.Counter(), collections.Counter()]
        if parts[2] != '-':
            piece_count = 0
            for c in parts[2]:
                if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    piece_count *= 10
                    piece_count += int(c)
                else:
                    piece = Piece.from_symbol(c)
                    if piece_count == 0:
                        piece_count = 1
                    self.add_piece_into_hand(piece.piece_type, piece.color, piece_count)
                    piece_count = 0

        # Set the mover counters.
        self.move_number = int(parts[3]) or 1

        # Reset the transposition table.
        self.transpositions = collections.Counter((self.zobrist_hash(), ))

    def push_usi(self, usi):
        '''
        Parses a move in standard coordinate notation, makes the move and puts
        it on the the move stack.
        Raises `ValueError` if neither legal nor a null move.
        Returns the move.
        '''
        move = Move.from_usi(usi)
        self.push(move)
        return move

    def kif_pieces_in_hand_str(self, color):
        builder = [[
            '先手の持駒：',
            '後手の持駒：',
        ][color]]

        for piece_type in range(ROOK, NONE, -1):
            if self.has_piece_in_hand(piece_type, color):
                piece_count = self.pieces_in_hand[color][piece_type]
                if piece_count:
                    builder.append('　')
                    piece = Piece(piece_type, color)
                    builder.append(piece.japanese_symbol())
                    if piece_count > 1:
                        builder.append(NUMBER_JAPANESE_KANJI_SYMBOLS[piece_count])

        return ''.join(builder)


    def kif_str(self):
        builder = []

        builder.append(self.kif_pieces_in_hand_str(WHITE))

        builder.append('\n ')
        for file_num in range(9, 0, -1):
            builder.append(' ')
            builder.append(NUMBER_JAPANESE_NUMBER_SYMBOLS[file_num])
        builder.append('\n+---------------------------+\n')

        for square in SQUARES:
            piece = self.piece_at(square)

            if BB_SQUARES[square] & BB_FILE_9:
                builder.append('|')

            if piece:
                builder.append(piece.japanese_symbol_with_direction())
            else:
                builder.append(' ・')

            if BB_SQUARES[square] & BB_FILE_1:
                builder.append('|')
                builder.append(NUMBER_JAPANESE_KANJI_SYMBOLS[rank_index(square) + 1])
                builder.append('\n')

        builder.append('+---------------------------+\n')

        builder.append(self.kif_pieces_in_hand_str(BLACK))

        return ''.join(builder)

    def __repr__(self):
        return "Board('{0}')".format(self.sfen())

    def __str__(self):
        builder = []

        for square in SQUARES:
            piece = self.piece_at(square)

            if piece:
                if not piece.is_promoted():
                    builder.append(' ')
                builder.append(piece.symbol())
            else:
                builder.append(' .')

            if BB_SQUARES[square] & BB_FILE_1:
                if square != I1:
                    builder.append('\n')
            else:
                builder.append(' ')

        if len(self.pieces_in_hand[BLACK]) + len(self.pieces_in_hand[WHITE]) > 0:
            builder.append('\n\n')

            # pieces in hand
            for color in COLORS:
                for piece_type, piece_count in self.pieces_in_hand[color].items():
                    builder.append(' ')
                    piece = Piece(piece_type, color)
                    builder.append(piece.symbol())
                    builder.append('*')
                    builder.append(str(piece_count))

        return ''.join(builder)

    def __eq__(self, board):
        return not self.__ne__(board)

    def __ne__(self, board):
        try:
            if self.occupied != board.occupied:
                return True
            if self.piece_bb != board.piece_bb:
                return True
            if self.pieces_in_hand != board.pieces_in_hand:
                return True
            if self.turn != board.turn:
                return True
            if self.move_number != board.move_number:
                return True
        except AttributeError:
            return True

        return False

    def zobrist_hash(self, array=None):
        '''
        Returns a Zobrist hash of the current position.
        '''
        # Hash in the board setup.
        zobrist_hash = self.board_zobrist_hash(array)

        if array is None:
            array = DEFAULT_RANDOM_ARRAY

        if self.turn == WHITE:
            zobrist_hash ^= array[2268 + 81 * 2]

        # pieces in hand pattern is
        # 19 * 5 * 5 * 5 * 5 * 3 * 3 = 106875 < pow(2, 17)
        # just checking black side is okay in normal state
        i = (
                self.pieces_in_hand[BLACK][ROOK] * 35625 +
                self.pieces_in_hand[BLACK][BISHOP] * 11875 +
                self.pieces_in_hand[BLACK][GOLD] * 2375 +
                self.pieces_in_hand[BLACK][SILVER] * 475 +
                self.pieces_in_hand[BLACK][KNIGHT] * 95 +
                self.pieces_in_hand[BLACK][LANCE] * 19 +
                self.pieces_in_hand[BLACK][PAWN])
        bit = bit_scan(i)
        while bit != -1 and bit is not None:
            zobrist_hash ^= array[2269 + 81 * 2 + bit]
            bit = bit_scan(i, bit + 1)

        return zobrist_hash

    def board_zobrist_hash(self, array=None):
        if array is None:
            return self.incremental_zobrist_hash

        zobrist_hash = 0

        squares = self.occupied[BLACK]
        square = bit_scan(squares)
        while square != -1 and square is not None:
            piece_index = (self.piece_type_at(square) - 1) * 2
            zobrist_hash ^= array[81 * piece_index + 9 * rank_index(square) + file_index(square)]
            square = bit_scan(squares, square + 1)

        squares = self.occupied[WHITE]
        square = bit_scan(squares)
        while square != -1 and square is not None:
            piece_index = (self.piece_type_at(square) - 1) * 2 + 1
            zobrist_hash ^= array[81 * piece_index + 9 * rank_index(square) + file_index(square)]
            square = bit_scan(squares, square + 1)

        return zobrist_hash


class PseudoLegalMoveGenerator(object):

    def __init__(self, board):
        self.board = board

    def __bool__(self):
        try:
            next(self.board.generate_pseudo_legal_moves())
            return True
        except StopIteration:
            return False

    __nonzero__ = __bool__

    # TODO: Counting without generating actual moves
    def __len__(self):
        return sum(1 for _ in self)

    def __iter__(self):
        return self.board.generate_pseudo_legal_moves()

    def __contains__(self, move):
        return self.board.is_pseudo_legal(move)


class LegalMoveGenerator(object):

    def __init__(self, board):
        self.board = board

    def __bool__(self):
        try:
            next(self.board.generate_legal_moves())
            return True
        except StopIteration:
            return False

    __nonzero__ = __bool__

    def __len__(self):
        count = 0

        for move in self.board.generate_legal_moves():
            count += 1

        return count

    def __iter__(self):
        return self.board.generate_legal_moves()

    def __contains__(self, move):
        return self.board.is_legal(move)


class SquareSet(object):

    def __init__(self, mask):
        self.mask = mask

    def __bool__(self):
        return bool(self.mask)

    __nonzero__ = __bool__

    def __eq__(self, other):
        try:
            return int(self) == int(other)
        except ValueError:
            return False

    def __ne__(self, other):
        try:
            return int(self) != int(other)
        except ValueError:
            return False

    def __len__(self):
        return pop_count(self.mask)

    def __iter__(self):
        square = bit_scan(self.mask)
        while square != -1 and square is not None:
            yield square
            square = bit_scan(self.mask, square + 1)

    def __contains__(self, square):
        return bool(BB_SQUARES[square] & self.mask)

    def __lshift__(self, shift):
        return self.__class__((self.mask << shift) & BB_ALL)

    def __rshift__(self, shift):
        return self.__class__(self.mask >> shift)

    def __and__(self, other):
        try:
            return self.__class__(self.mask & other.mask)
        except AttributeError:
            return self.__class__(self.mask & other)

    def __xor__(self, other):
        try:
            return self.__class__((self.mask ^ other.mask) & BB_ALL)
        except AttributeError:
            return self.__class__((self.mask ^ other) & BB_ALL)

    def __or__(self, other):
        try:
            return self.__class__((self.mask | other.mask) & BB_ALL)
        except AttributeError:
            return self.__class__((self.mask | other) & BB_ALL)

    def __ilshift__(self, shift):
        self.mask = (self.mask << shift & BB_ALL)
        return self

    def __irshift__(self, shift):
        self.mask >>= shift
        return self

    def __iand__(self, other):
        try:
            self.mask &= other.mask
        except AttributeError:
            self.mask &= other
        return self

    def __ixor__(self, other):
        try:
            self.mask = (self.mask ^ other.mask) & BB_ALL
        except AttributeError:
            self.mask = (self.mask ^ other) & BB_ALL
        return self

    def __ior__(self, other):
        try:
            self.mask = (self.mask | other.mask) & BB_ALL
        except AttributeError:
            self.mask = (self.mask | other) & BB_ALL
        return self

    def __invert__(self):
        return self.__class__(~self.mask & BB_ALL)

    def __oct__(self):
        return oct(self.mask)

    def __hex__(self):
        return hex(self.mask)

    def __int__(self):
        return self.mask

    def __index__(self):
        return self.mask

    def __repr__(self):
        return 'SquareSet({0})'.format(bin(self.mask))

    def __str__(self):
        builder = []

        for square in SQUARES:
            mask = BB_SQUARES[square]

            if self.mask & mask:
                builder.append('1')
            else:
                builder.append('.')

            if mask & BB_FILE_1:
                if square != I1:
                    builder.append('\n')
            else:
                builder.append(' ')

        return ''.join(builder)

    def __hash__(self):
        return self.mask

# 81 * (14 piece types * (white or black) - 1) + 9 * (ranks - 1) + (files - 1) + ((white or black) - 1) + (current turn) + log2((19 pawn in hand) * (5 lance in hand) * (5 knight in hand) * (5 silver in hand) * (5 gold in hand) * (3 bishop) * (3 rook))
#  = 2268 + 1 + 17 = 2286
#
# Genetation code example:
# import random
# for i in range(2286):
#     if i % 4 == 0:
#         print '    ',
#     print '0x{0:016X},'.format(random.randint(0, 0xffffffffffffffffL)),
#     if i % 4 == 3:
#         print ''

DEFAULT_RANDOM_ARRAY = [
    
0x6B85EEFFF1AAA0A8,
0xC2BCEEEF83845F41,
0x384892D2C269A81A,
0xC672BBDF70D767D9,

    
0x92F2DA3D3ABC1091,
0xB557D980C13A1958,
0x82F36459618E9E42,
0x27D92AC3820DA361,

    
0xA88AA87962E4E0F0,
0x3103D0B1A37B8B6D,
0xD631FF02385CF223,
0x275624B84CBFE035,

    
0x792A2D5D9CE52F9A,
0xE203C8455626C19E,
0xA2F29307A83F2018,
0x6056CAC1661D812B,

    
0x773589D826A311E3,
0xC2826BAC070324E1,
0xAE119EADD18AED84,
0xF27803DA2C3482AB,

    
0x7C9C26F36C7F61C4,
0x16F7FE9A90306C64,
0x1CCA4F20AF97B355,
0x5B8358C5C0208BC1,

    
0xB070E0A2D0574D39,
0xF9D493A8E37E19BF,
0xA244E692206335D0,
0x1559BA6E8D454486,

    
0x9F0EDFD2A4A3BBE7,
0x43C42D0B8FE323FD,
0x4CBAB6B136D1E84C,
0x8CDC69653BABD2B8,

    
0xC7A5EF2D467235CF,
0x566B2E73180CDB61,
0xB0800A73E1789661,
0x1EDCBC623DE2BBAE,

    
0x755BB314788A23DD,
0xE83D285E5A07FD94,
0xAD9BF5613D418479,
0x0A970AE76395AD80,

    
0x0B1D63E372DF091A,
0xB9E57EB6312369EF,
0xC81A6F0EAFAAF73B,
0x8DB2DFA95B2B0ADB,

    
0xFDA89C9578498403,
0x32B112F74EC2FB5E,
0xF1FDD0C5B50D4141,
0xAA69861D89D938AF,

    
0x370C4A501B8CDDB8,
0x923EEEAF791F5F28,
0x0B35E795C30E184B,
0x00F77040E4AF1D73,

    
0x266881C75B4C6096,
0xD2C820A5A470E03B,
0x40C3292357CB7AB5,
0x48711693A268D030,

    
0x17D0A61031147155,
0xA04790B8F1E52EB1,
0xB513122C6390AD03,
0x3A39469E5B944F40,

    
0xF13366B714D27A97,
0x56DD30E900FAE61A,
0xCD430B9AB373835A,
0x930E3205D62FD616,

    
0xA8A80C3C60EB4025,
0x18FFF168B21B2E84,
0xC0A7F564CFA33BC8,
0x9B8CC0D691B67939,

    
0x890A242A3C254925,
0x1D954A7065486BEF,
0xDE140290C443B19A,
0x68A8067AD4B7D2A3,

    
0x02FF613ED33249C4,
0x021D901451A43462,
0x5853EAFE2AA3E802,
0x26F484FE75BF7E11,

    
0x0425134807C7F459,
0xC5651A556C7C266F,
0x47C49754B7CBE22B,
0xD793099355A99A3A,

    
0x6C341460BDC859F6,
0x7C5C076597D06C81,
0x317E7DA2599BF8D1,
0x024AA784330D6068,

    
0xCFCC18828DEF786B,
0xEA83DA87C6B1A5E6,
0xE46B559F9054523E,
0xDF4CE6C28D623381,

    
0xA6EC93E5EB4D3359,
0x4591A6748BBD4C12,
0x96450B61B23DD89A,
0x92364C52CB1FFE63,

    
0xA97CF88BFA226484,
0x8179181C708FE915,
0x1DF76EA4732F2EB2,
0x8C325682D8A05E3F,

    
0x7635F8581B1903B7,
0xE8418240185B2A57,
0x232C36EFFFA34395,
0x8D9613AB30E781D0,

    
0xA7429880D1388F8C,
0x7822B753DDE2EB1E,
0xE16057E88D1BBDC8,
0x0DBF2EECFEBE6EE7,

    
0xC3B5D98E4E7BD88D,
0xF47712D6A8862520,
0x16383EACC3F8052F,
0xAC35ED552855C088,

    
0x521C57A42FDBC691,
0x9126845C24B5F0CA,
0xB7E631E7A1C376BD,
0x4791D247A391D234,

    
0x02D1E5A39690A5BD,
0x5BC34B7DCC467BAE,
0x003FB2AC46D9CE4B,
0xC3E77E92BD04BDD0,

    
0xB0E503290F0D725A,
0xB3DE79184F2368EC,
0x3DD4DACD62B1D545,
0x89FC148D23216AB2,

    
0x82BFB502192A1274,
0xDB40B9F183DCDCE3,
0x000A8A863F4C9AA6,
0x2F460F7A9FACC1A4,

    
0xE46C052E668EDC50,
0x3D3EB6D64EC97352,
0x3F6CD8E22FECF087,
0xE4E3D99BC4950BDA,

    
0x7652FC004D899291,
0x12A9448A2C5C2930,
0x6241AB7D6CBEFD5D,
0xF79B815C091757E8,

    
0x35DED3B0E5EC4535,
0x18FE3BA5668331BC,
0x497DF625D91B1B80,
0x7CF24AA7F0E3CFE7,

    
0x989823841D9BEC52,
0x0282AD589B27AFD9,
0x7729A91E1EF9178E,
0xDE9148D074065C8E,

    
0x8015B7C612F2F853,
0x6B14FFBD04E7EF24,
0xAF9A6B5762B3D0A2,
0xB73D896F01A79DC4,

    
0x5ADC6E8517E62D3C,
0x4DC7E67BDC72C3FD,
0xCDC6B7C62B2B6D50,
0xCDDA1416951ED0A6,

    
0x23FE350CF1EF9CA7,
0x352CF5436630F871,
0xA86A47908F71C650,
0xAEC2623BCEF51BCD,

    
0xEAF49942784C67DB,
0x3DDE5BF6B35BF6EC,
0x1F21FF72D25A6524,
0xE1F483058F060B8A,

    
0x5D1E4D3EA90C1392,
0x63ADE98219909F8C,
0x3089111809CD95F9,
0x0D316EC9AD7859CB,

    
0x44B5CA4CE06DF96E,
0x29ADB7A9D27E473F,
0x468DE761D411DC70,
0xC21EAAA2BA71DF14,

    
0xD4789E421A307059,
0xD1B13D71CC560945,
0x1CC789B5F58E699D,
0x3C9CFA4D5FD2D89C,

    
0xB8F4BB2C467B621C,
0x0CB93796A9949D3F,
0xDCBC9615AB1F4D38,
0x12A5ABB7AEEAD382,

    
0xF085E045753E1718,
0x50AB882A4167DA85,
0xFF1D4CE44D9F6D5A,
0x34C97393B01054BD,

    
0xD8F68ADAD92F820E,
0x51F532EB0F8F3D66,
0xDB7A010DD22F66CD,
0xD73F454D93E3E94A,

    
0x8A39830DD2138EB5,
0x88498BCEB293428A,
0x436ED552D1197979,
0x4ADA28652B30A893,

    
0xAD140AB33B0CFC74,
0x42CCA313055B099B,
0xC6E6EE548F7944FF,
0xB3DAD67AAD5EFFEA,

    
0x1090C303E161CCB7,
0xC02D1E761D35D4DD,
0x8CDCDFCFAFA51406,
0x85D0331AAA57A545,

    
0xB69A84A0C896869E,
0xEBA95016562EDD21,
0x6EF69EE4127754AC,
0x3BDA916CD7AE8DD0,

    
0x1FFA3803A0815946,
0x6B47B7A3847CEF6E,
0x1598B838FECA29D9,
0x3247D0ADC8A26B1A,

    
0xDEF98E2D78610D10,
0xB827A2BEFE89A861,
0x91314D22304E4818,
0x1E15B18571F26CD6,

    
0x427283A38A2364E3,
0xBF4C2497A3490A98,
0xCAFE5AD2B9F0867C,
0xC16C2A372F5E9142,

    
0xD6E08D635BC3E1C6,
0x50C2954FDF6B92D7,
0x0A6A313960F32A87,
0xD4643A0AFDB65D0C,

    
0x4EECD5CD76AFA730,
0x204C1F51292D0439,
0x2900187A65FA4A30,
0xCC21A09B43C8E0C2,

    
0x62002904519567AF,
0xD9E27664668F8DA8,
0x42448C9F3B5F7139,
0xC9CE8A3BB9EEDF78,

    
0x7C2EAD139786369F,
0xC57AB9681A07C57E,
0x43D5F1B532DFE44E,
0x95006BBD68A130A2,

    
0x610AEB35A0B5BEF9,
0xE44E31FFC898B56B,
0x9277F091C11F88B5,
0x71090358DE782F9A,

    
0x82E052751577F61A,
0x497D51A97A4C7C11,
0xC5F49FF33BE5CDE3,
0xFA141091CAD7F4D5,

    
0x0679AF56FFEC6674,
0x4FCAA6C39B3E1DE0,
0x1D16C841EDD646C5,
0x5E7A006839671CE5,

    
0x71916AAD2C1459F1,
0xF5A4992DC9D41C0E,
0x6F7CEB952EC6CA07,
0xA19D1FF6229E71F3,

    
0xDA5B518EBFCF7B79,
0xEE508903A52603A5,
0xBE08E553AB8D1752,
0x86498AD408EF30AD,

    
0x30031A0E4DBC1946,
0xAA59A41580D86791,
0x0D5C704178338464,
0x15BC3A489FA39E53,

    
0x90D9E890D26B5319,
0x8CA406AC07B12437,
0xBA49859AD2D9A619,
0xF1CB797CFB289620,

    
0x0CF34AF9F617A443,
0x8FC20BF7BAD4D387,
0xD6FE4D9887526828,
0x3AA48B5C55DDAC20,

    
0x48048D5AFF7F0A9C,
0xAFA8130519863D25,
0x251FA7F7BE7D7228,
0xCB3F6522E395A785,

    
0x94B295594F5F8123,
0xD1E126C6543F2F12,
0x8013555B89B6D354,
0xB1895088480A9C2F,

    
0xE1925E23E8612158,
0x44272CFD04C00256,
0x2D81ACF5C6427FA3,
0xD719CA2CA9982BD4,

    
0x82B751A79CF267B7,
0x13ED990F222EA741,
0x2F7216BA64479466,
0x029E1C46E04B7608,

    
0xA21173D0637A2761,
0x9C33DA91175A050A,
0xF51B305972764D87,
0xF8A395F605B4892F,

    
0x04A1BA8603A30C39,
0xB4ACDE23209CCE07,
0x6D15F25305196799,
0x3C7D7B1EC079F5A7,

    
0xE710FB9158EDFBB7,
0xDFDD58E3277F1465,
0xB2852950250FFE5A,
0x521CDB1783E065A2,

    
0xDF72F03CC0F2AC16,
0x683C03E5405C0FB1,
0xE5AEC9259B2935BE,
0xFCBEFB7447EE7940,

    
0xB1F09687A9C01E59,
0x5D0BF925F1E73521,
0xF62D6D0FBBF2ABB8,
0x876757F4327BFC36,

    
0x754471F13F08CE79,
0x0E524947446ABAAE,
0x8EA3A5175468A716,
0x1D6FDCBEB9A414F0,

    
0xC6FFAEC584DD1A4A,
0x082C658C6AEDA86D,
0x9D014345CE911347,
0x6E5CE7ACD0905F51,

    
0x82F859F9C1014412,
0x5F434E72400A9329,
0x83838129F91E2F41,
0x087C5BB654B0EA6A,

    
0xCEFF23C04AC1515C,
0x63140DE2D76D1C9A,
0x6237F22301CD11C8,
0x4BB32C1DF6F6BFC9,

    
0xA46DE3AA5784A204,
0x6CE3C62A0D717A99,
0x0BEBF0A34B87D664,
0xBE41F9516E34805F,

    
0x9379E5002839E9F9,
0x6DB5EBD12BC7B051,
0x176E721C999021D3,
0xB227069126E5FC36,

    
0x1934D715E74BD22F,
0x61CDE6220E813407,
0x9E0143B508CB0330,
0x3504CE50341DDE7A,

    
0xA7315F3152DA03D4,
0x724B7F880906F28F,
0xEA8ADE4AE6C0FEB0,
0x4404E66F1565BB3F,

    
0xAB6F2AE9EFCE7226,
0x458F6F5C6453F4BF,
0x300F9F5F7ADC3642,
0xC6618D166851BDE8,

    
0xCAB36C6B629980B3,
0x3E7D08B6C8681777,
0x980F9FF97F47868B,
0xD864D52876AD362D,

    
0x590903CE35C2BEE5,
0x21A001186A21789D,
0xA62B8323CA820EDC,
0xE5B6CB0B89EB8185,

    
0x6415DE5DF04DA704,
0xEA90F2F183B27DF8,
0x859C9948FF62606D,
0x19F80EDA15102933,

    
0x86380C3D37F14BB8,
0x81D00555F21C81E1,
0x9EB5A8EB2A1E271E,
0x88915DE3D885B53B,

    
0x8395069E9C3A5C41,
0x2B9693367CA475B3,
0x356A36C50936DF3D,
0xFAD37DFF6CB8EDBA,

    
0xFAA083299E4BCFE6,
0x320A2376D9FDB954,
0xAB26C6297D5E37BE,
0xD8D546C2E3367D30,

    
0x9554CCBDB67557A6,
0xA6B0B02738006D8C,
0xB84662B85ED71DDC,
0x7F649BB3636CE964,

    
0x1035EDE564E61638,
0x1842EF6CD3573D4C,
0x6CEC7F9BD02924EE,
0xD353A883AC0261F3,

    
0xF0E22A0B45680F81,
0x55FC62C8ED661089,
0x193876CF9AFCC3AA,
0xFD2EE6EBF81A8861,

    
0x62C45BDB921C5827,
0x5360F87E4C1D1F31,
0x363735E90B74BE51,
0x591B35F05CED355A,

    
0xAE452F1F741211B9,
0x8AFF1B21F0A7EF58,
0x8EABF478A0D3A9E8,
0x34B45A847890D862,

    
0x56EDD061F1F35847,
0x8CBCA94171CC9F75,
0x3BA1D27F6AA43EF0,
0x836284A0A5498436,

    
0x9480E90E4F462392,
0x19AAFE60862592EE,
0x885A1B288FCC86A6,
0x151084007C18FAB0,

    
0xFF638C249CD4F9DF,
0xB68C7E623313AD30,
0xDC9BFAA887A3B9D3,
0x294EB45F1E321D1F,

    
0x9AFE216D1B8AC08C,
0x7B5DED3531A7480B,
0xA9A1D841BEFB343B,
0xC9F62526EAEA8DEE,

    
0x1EE11ED41E9EAAA5,
0x003D87F5E27220B7,
0x6D293EBD8524CABD,
0x1C2B3BBFB61DF3C9,

    
0x346716505D2E38BC,
0x72929D07E201075A,
0x0389230A0495D161,
0x1FD509B95A38808C,

    
0x88259BBABEF336EC,
0xD2151565C72CB88A,
0xA37E30207B624663,
0x79947A1AA2E5375A,

    
0x5082AE4ECFD5D246,
0x62B54D4EC94C651D,
0xE730EEE2A2587494,
0xC02D6E794FA4ADF7,

    
0x2EA422C0CD0A5E50,
0x31EF60C083455538,
0xD2124E58A4671235,
0xA7EFE180879DD338,

    
0xC2BD1B122A23220E,
0x66505FD9CDDD1818,
0x6EC8609CBFB0C116,
0x02E57B6ACC17CE1C,

    
0x43508BF2E02DF25A,
0xB5854B5C768AF84B,
0x3BC89B99A6F3FA1F,
0x1BA8329BBA6C2B2B,

    
0xA66E775939792DC4,
0xECD7A7572F277EDA,
0x23C2C267E6C160A5,
0x0FEC03280D2FAB7A,

    
0x6BF0C930AA6B7D3D,
0xF4498AC90C592416,
0x9A0812F7F0AE1AAB,
0x3AA3ED8550856E8B,

    
0x8473171154DB173B,
0x0A903FBB538A048F,
0x9F335516B7A71FD6,
0x4AA636071E14DF36,

    
0x4E0A18FB5E993ABB,
0x009B20951986AFD0,
0x0F9A24E3AB483D83,
0x96EA4CCA1594A2D3,

    
0x0942467FC59F5A0B,
0xD6D9F138C9D50BA2,
0x6F53C7B48A2F6692,
0x72366AB0E3FAA1E6,

    
0x8E478975542D612B,
0xCC01B2DF27127B45,
0xECF506F32AFA364A,
0xE6879C3EAAAA4B9D,

    
0xB70400854DFCBB52,
0x1BD6506A3E34BB01,
0x52FB750568C64DC8,
0x56FAE6215B31F881,

    
0x12BA55690B70D69D,
0xFC55867D14E27819,
0xEDC7CFB9CF7E64F7,
0x068B6F126FDABE9F,

    
0xAF58DAEF5AAB83A1,
0xEDC129B8F9F6B2A3,
0x8547CFF2FA442B7F,
0x583BC98071C9091A,

    
0xC55F49EC8DFCFD66,
0x4DD1913779F212F1,
0x63786B644868016E,
0x1EFF6A2A11AA4A85,

    
0x19EE71C92A4A87FB,
0xF397F931A6B25AE6,
0xE9D474C24145ABD8,
0x6B5A82FC6ECB2460,

    
0x35685D8DACC7D7D5,
0x57EB12780F71C73A,
0x76FDFCAAC1EFF06D,
0xB8282DC89BEA2EE0,

    
0xF10E9C15B9A61BC4,
0x15FC35921544A3A5,
0xC5804A663808B29A,
0x721E8DAD00682002,

    
0xA4BFAB50726AC7F2,
0x796FEA220FF86673,
0x4BC235E4494BF0F0,
0x28FABD2E35755991,

    
0xC0752D833EAB0ECB,
0x8C6248A900753DD1,
0x73F8086B6ACB81E6,
0x2D6DCD00DBF69B64,

    
0xA3A8ABAD2423F30F,
0xFD55C9BDB5CD7D1E,
0x5707253FDABC17D1,
0x92BB5204E6AB4694,

    
0xF9D24CEEAFA1F577,
0xC621E6EC5541F1AF,
0xDB74B42F54533402,
0xCA8BE0738D106083,

    
0x0F1174C67948DB3E,
0xB676A5CD33624200,
0x535D0753B1EF7ED2,
0xD77518BAECD69418,

    
0x0F99B14B58DA8AFD,
0x7B23DAC50B2FF20F,
0x5522F11EE6D18386,
0x1DEEE12D9C19585E,

    
0x955626B48A7E6C8C,
0x687590ABA770A3BD,
0x5F242C879BA5946B,
0xE1727EF16D1F9771,

    
0x31064B9C8ECD1D1A,
0x9E3C485AD2BDA3C6,
0xD40528A7153C643D,
0xDB68A4EA87C9B10A,

    
0xA9C216FF3B27252C,
0x5D1552F7AB5DE36A,
0x5F63A8E3EE224E5B,
0x6ED29B15FC62F257,

    
0xE8EECC9E7D457ED5,
0x3573A052286045CE,
0xA726A2B38C3FA043,
0x78861713562890D3,

    
0x67622F660F8B6BC8,
0xB9A0B578762756A3,
0xA3C0BF03907D2C2B,
0x9C7076A21DFA4F4A,

    
0x34847233931AC68D,
0x6637523408DE475D,
0x246D0CEF02578953,
0x2F332111B9208F51,

    
0x76BA7BFB9E7352A9,
0x5C0851BE3AB40D02,
0x54F097968F0A9215,
0xC15506194A95B294,

    
0xF2D0991C148D5D79,
0x453A9EF202ECA216,
0x9B9648D3BBED3B04,
0xD87839058EB1E1F9,

    
0x4E0C4B205CD60B53,
0x818BAEED6BDE28E1,
0xD1D57B3FBE4A4759,
0xD7AD658AC37897E5,

    
0xF8A2EACFF8C1E6E7,
0xC7DA25E11BE381BE,
0x6EBEC726901F2ECF,
0x10FB65D2C1422C70,

    
0xA7A46C9D607B96CF,
0x9F7BBE6B7485431B,
0x20403BE59C66CCD1,
0x7BE7B887661A54FC,

    
0xB05A9185242790EC,
0x65C5A702346C0DB6,
0x8171754230C3F3A8,
0x23AA2022F94BA276,

    
0xD7A431A092F27274,
0xA855AA81E1BD37A7,
0x2F2AB9CA5C04F532,
0xF60FF0D7AB8B5471,

    
0x9D97041FCB91AFEF,
0x8FEA37BD3378CD5C,
0x2E52F7A0AED4FB54,
0xC17A8246C671F695,

    
0xEABDB3E1BB8B280D,
0x5946E04295B31B6D,
0x5006D3540CC2E5A4,
0xFD71122561E41DAB,

    
0x4739B59A934CB24D,
0xB1C7463763F5C40F,
0x7EF1A029E751CFF5,
0x5F72D3D97616CC41,

    
0x80E6795CAB94AEE3,
0xBB7337A856D74DCB,
0xE9C5C200DB0D6201,
0x08E118EF90C6F254,

    
0x3A4BC41344D2BDBC,
0x7E73B2C75C160BC0,
0x84D4F056560FFC7E,
0xE5292F759AD075C0,

    
0x6C7D91A97BC87C96,
0xAC83556314103C0E,
0x00D2A661EEF97A93,
0x6A5FD248D1BC86AF,

    
0xF33DF23A5FC9EF02,
0x5C7DC724BA3ADBE0,
0x6BA899B679021ABF,
0xFC5DC26CA9336786,

    
0x9CAB7E770EB0CC0A,
0xC79E1AEDCF6A107A,
0x26D432146039DBEA,
0xB5E847935F10D0E1,

    
0x414AC0CE7D6B62D4,
0x09AC08B7F81A357C,
0xADFF586EA4222BC7,
0x6A6620C84AD1821E,

    
0xA5E92D2EF3A67EF3,
0x5425A93016595D41,
0x4F8EBE989C2D765B,
0x3C541A63A35159FB,

    
0x71F149CDEA186DAC,
0xC5A820F305DA54D4,
0xFEA9C8F4ABCA84F2,
0x636C1D7E02E3476A,

    
0x0E41566A8C0347F1,
0x7F26457F7CBE40E7,
0xE9CCDBE35819AD25,
0xBC6AE0C6A1B8A45A,

    
0xE9CA208D6F82C996,
0x49EFBDC56F8C3653,
0x4B414186C31D0131,
0xBAFB3E0BAFC09B1B,

    
0xD5466ED6644F877D,
0x8094165E9C2BAE79,
0xB33815E796B4280F,
0x50EE0B593A436516,

    
0xBA58AE83533C1CCE,
0x210E13E95D465C25,
0x919FE22EA15E2FA9,
0xA5F94EC725DF4F0F,

    
0x0452AA12669F6027,
0x2AE9C44D61B169C3,
0xD04F33E4BE92977A,
0xD685F05EF12DB7D8,

    
0xDA476751D53B4E9F,
0x9A295758720C7166,
0x1352BABF7705192A,
0x14E118FC35ABB02F,

    
0x8DE22242E04CF9DE,
0x95CB138C4B9AE0A9,
0xF7E7C370CBE6FD03,
0x43174ECD25CCB57E,

    
0xE894908E8DF3F231,
0x8AFEEDE0DD0691E1,
0x1B8787487EEB9480,
0x38F5EEB04B8E7831,

    
0xFB9064E0F49F9FA8,
0x60ADE4E0D2224FA1,
0x3DA6B935EB6D8D81,
0xFC7916D9659A8FFC,

    
0xAF063161BC1FBAC4,
0xC490F259681D487C,
0x2C4F2A21512FB0D7,
0xAFE55913517F08E1,

    
0xCFB664CCE0733379,
0xE086AFE36D2E5888,
0x81296B057027E415,
0xFB84CAFAA2D1D91F,

    
0xEA0588D5184E764E,
0x0720A1A6D789AB69,
0x5828A595296C30B9,
0x432DCBF5E28199D7,

    
0x47ED85B6D0422167,
0xB31A35831E610A57,
0x5C735D1E67D0596C,
0xE55D6B631E272BB0,

    
0x40B38DBB316E826C,
0xF862D41EE8818140,
0x83AC1D3367A55B3C,
0xB3BEFAB71D4AA402,

    
0x40A64E2B6D3ACDDA,
0xA281FFD2549FEA88,
0xA495B26ECF3CA9FF,
0x4EE009D6B2C2609D,

    
0x6D07C5B0EB45B7A8,
0x1B93CA19ADAC60A2,
0xFD076CEAAEEEC88F,
0x1BDE1AD2B4673D72,

    
0x48BDA926CB334895,
0x2E08E6900A8651D8,
0x054CD275B1D2552A,
0xEC7D503F9D23C5D0,

    
0x5BA8691678118AC5,
0x3B27A57045A68704,
0x02269B43DDFD4E93,
0x9C751347634B59F4,

    
0x213CF2D0F2AC6725,
0xCF5EE8CB1DC555D6,
0x85977DB8A3F421C5,
0xB251423DA3BC7857,

    
0x15EF328A509852D5,
0x9028249778622CF7,
0xC11166B029411BA9,
0x6EF34A5A81106F03,

    
0xAE113BAB1721249D,
0x48CA15EAA58CB661,
0x8A718A53B2D4ECA3,
0xF83A87CF1F5C800E,

    
0x77921EEE293EA3D4,
0xC42BE1F00E1CA1C0,
0xD77CB98EB69CFA33,
0xDE0EC358C62783B0,

    
0xBD66FAD622F8E839,
0x8D80AFC4DEEA040B,
0xB33F2C004F62C681,
0xDA1F6AF921B6FEB5,

    
0x82BA2E876C606F92,
0x2B5216A911876E16,
0xBEAF9C9E16657034,
0xE41B8099D7730506,

    
0x53CE65B89A7E0998,
0x9CE42AA89BE259E2,
0xF80530E74959AC1E,
0x76A109DB63E67D28,

    
0xB5872A1064C51E71,
0x6A1E98A56976CE5B,
0x4BE22EE093788E25,
0x720FC60E13B31A41,

    
0x83317D2B6D9F3466,
0xB9E66993548380A9,
0x130DE8225CC06BD8,
0xDF4363E53F0EBF09,

    
0xDF536661E811B14B,
0xA6F55983EFDAF365,
0xFC2A613A46CC5AC3,
0xC7EFA98E0960C266,

    
0xBFFF39912DF28C13,
0x067977E527115518,
0xB65A6B19226821DF,
0x27843C0D77000E1B,

    
0x1F23078F898F0BE8,
0xD7B3C2160807EE2E,
0xEC38DE6E0FB6FF0A,
0xCF41CCA1829BB5D7,

    
0x4A0B55239C0C1F22,
0x11E6634622B2F788,
0x26C5E45FD01841B9,
0x30E5F1D5F787BCD3,

    
0x19F3EBCB8CB89F81,
0x2EBCA8033E17F897,
0xB2D1BEC19184FA22,
0x2E32DC66C6706CF7,

    
0xCC00D60CBC47D36A,
0xFA173DC37A6E69AC,
0x13402E84FEEF5CF3,
0xD6B629A24DC7C76E,

    
0x1FB355EA8A143C17,
0x7D2693C7A9D39011,
0xD5CDBA5A37EE1E4D,
0xBE8444CE975DC5DB,

    
0x05A338522633D07A,
0x62B19050EDC9E95F,
0x7E69ADA1782B3278,
0xD8A27437D0F9C3C4,

    
0x70A9A83B6E34B35F,
0xCD2A1C4312814B47,
0xC9DE677AA59C6029,
0x030D7224FAC6F415,

    
0xF3850F3E3FF7C4DD,
0x32DA201D70A8ED9E,
0x9F371C6BD1D3FCCE,
0x557CEC0B8DE809C9,

    
0x1E098D63EC805948,
0x99C07E3E2D13F7BE,
0x5A8433BD17B76616,
0x1C9DB9AAC11A3911,

    
0x9D0206BBBB29D7D8,
0xB09E74BC53F94028,
0x14B7167B60D70FD4,
0x1D52E19B3E0D0244,

    
0xC6B7928CC2BE490D,
0xCEE72D432EB2C8BD,
0x7E208BB3A8CEA850,
0x2547ED30BCF829A2,

    
0x3018789F188ADCD9,
0x6B54DC7436CDEF69,
0x7AB8E6A1F4B0418F,
0xAA15641595F5647B,

    
0x20E6C46E34177351,
0xFE9F49DF50B3FE17,
0xCC637A9675C9CB13,
0xD269EA9A6D19179D,

    
0xB860AB92FF7492D6,
0x58A83FE7B989A256,
0xFBFE3F8EE108C14C,
0x8949A5A9E273504C,

    
0x8DB4C5C9501FD4BA,
0x3F3191EAB4DDE347,
0x3BF8C452D4661781,
0x56E4364D6EF60851,

    
0x76C123D13C0BCAB1,
0x72ECDFCD5DD22AE5,
0x873D1B274EAC2527,
0xDA45C13898A1F1C6,

    
0xCE29CC4DB291CB08,
0x051DFF1AEA51C982,
0x9C4FB593973F141B,
0x9F943822CC3EC2CC,

    
0x283BC75202CB2A31,
0xB3D5C61372374C96,
0xD3E4D782BA5C6AA4,
0xE447AE3EA8E300C9,

    
0xD9C3BD0281365AEE,
0xE5D54F3C23CD93C2,
0x4743A7DB90671907,
0x54645303F27B40B5,

    
0xDBDD4756E7A58A34,
0x2C8DBEA47AD920DB,
0xADA8003127821B6A,
0xD95EF2C8200DA160,

    
0x15A5FEC7B049E3F2,
0xD4C99E4FE22857CA,
0xB244AD6D81C07E88,
0x884594D8BD23C626,

    
0xAC955086AB7C7002,
0x8B867C59958E589D,
0xB29CEE06596EEB4B,
0xE387B0F605E0FFB5,

    
0x0BE0192E3D1F6014,
0x668FBCB429B8BC74,
0xE2526E38C18660EC,
0x581656AE2C4F6B4F,

    
0x4E087E9FFEA94179,
0x39D49AF8CFBFEC04,
0x7426D0044758CCB1,
0xA03F199B38812443,

    
0x46ADD27D47C98528,
0xE898F870CAFA9971,
0xC52C804FC5CA346A,
0xFDD88FEC7CC4C8CF,

    
0x8AD7F3247879DE75,
0x5CFB744F1229C833,
0x488EDCB39F2DAC86,
0x35D4CF311B81C91C,

    
0xE465651B37DEDEEC,
0xFA0F99FFC264C343,
0xF018F9DA82E63CA5,
0x9AC1DB862DD7E37C,

    
0x9694E5AC20110204,
0xF4CE63288A887766,
0x19AE699C8038F94F,
0xC87CDA19E76C0F4E,

    
0x071727E927F15505,
0xB28AB95AD78477BC,
0xB187DBCB437C4129,
0x278B28F8CDBFFFD9,

    
0x43B3E737D3C5CFC1,
0x34F973B5BCA6E456,
0xC5001C6315E338EA,
0x8D0A8254ACEAF6B5,

    
0x324F707D41EFDA9E,
0x1A7F30CE0BFB4D56,
0x2FAC71358FB284ED,
0xC744DB33B2325705,

    
0x06842C9DA70658BE,
0x58118D284C6D7855,
0x69DB6B81C0D12580,
0xDA0623D07C977EDC,

    
0x91BC5E08E9A8D461,
0x0D9DE956D3C2B12B,
0x5CD25106250FA07E,
0xB334CDDC10058693,

    
0xAA6A6979EA7258E9,
0x19BA97D11715CC4E,
0xDEBF0166E1AC6E7F,
0x4AE0517F12BFF4A9,

    
0x6A03E2083FF6D63C,
0xA8AD1E6D285FA418,
0x436B52A2B55F41B5,
0x5FF94007AF7B3A52,

    
0x4905B1B44A76B5C0,
0xF447E92868342692,
0x5D6FC2A071BC60D4,
0x946E9687BBE72E0B,

    
0x0E268F27D6DD6A19,
0xA6FDDC7A7A089A1D,
0x3D2D5BF0110544D9,
0x834B1C82BE757DBD,

    
0x1ADB33F42B660DF4,
0xCA45D6E90CBD1376,
0xC475DF979B9F7178,
0x512AF40BA1E019DE,

    
0xD5EEC3796E08EE9B,
0x3F12C5A2F6729607,
0xB0818F316ADB90A9,
0xF0EC633008351953,

    
0x93B1F5156DC71D57,
0x4FB213852C9850D4,
0x7D8C08087701158B,
0xE5015FFFEF7939ED,

    
0xDF4A7EEB94831718,
0x7986125C4AEB75D2,
0x2AE2E3387D06236C,
0x527F9F8FF7771D32,

    
0x614069D4E4AC8DB5,
0x672BBE4E8BECB880,
0x672AA76E809ED516,
0xB59B2F37106E4525,

    
0x717152CA2228C920,
0xE0434A6AC3B039FC,
0x82B4062DA8AA4FFA,
0x569DDE9A7E4427E5,

    
0xC9E0182BB15C7467,
0x3A8D16942933CFF6,
0x358CD060F91592D6,
0x24909C40312EFC69,

    
0x9303B76BBF690745,
0xCED70A744BF33E0C,
0x4A4194F15650AD13,
0x209A5C9424135F08,

    
0x0F5336FD282BD360,
0x3EF0CF4FC35572DB,
0xB16410125545577C,
0xD4F112E086857DF3,

    
0x35A3D6FB9FB6C428,
0x42856890DBAD9F3D,
0xEF5A13D89E2DBDAE,
0xA1ED2B9CD5ADEB55,

    
0xCEC50315F43A33CB,
0xB6FF19AC2E370D79,
0x6E1512F366991795,
0x6FAA9F7250C9293B,

    
0x2D0794728A59CF83,
0x634B80EF4CBA9119,
0x704004F1D1B4AEF1,
0x1423B345E61C8A73,

    
0x669CECF870345231,
0xB8EEDB50102F5B71,
0xADB13C4AB2393931,
0xB109724DD60B32E2,

    
0xDC3E9446351C9D2E,
0x15C7053FC2A127AB,
0x95679115B44F647F,
0xB3284A2DAD28B593,

    
0xB59DAE1C2ED3CB9C,
0x6605809F6587C337,
0x6D4E314BE4431356,
0x8B1C3D2E2CF1583F,

    
0x568326B30CDB2BBE,
0xDD2A8B91C2F142C7,
0x4CEC5B695F1E10F0,
0x1179CE97CC4F7A13,

    
0xCBA611F5AA04F9F9,
0x9DF70F3ADA43C113,
0xF5FC3B6B26EFE247,
0xC5A083FEF66186AA,

    
0x2D10E90139B9393D,
0xC7A4D6B22BA00FF2,
0xF21EAEB373B18C0F,
0x9881E2873B4C4C42,

    
0x09253D03EE14EDFD,
0x39F2D6B753681248,
0x1DC864070086B68E,
0xCEE77E0EF92D5BA8,

    
0x103DD274E08D418E,
0x45BC2D8D06A0339A,
0x4F6C8E96D0C22366,
0x159483A55B8CE6A3,

    
0xBE5A131B9B23A7B6,
0xA32EA526D23AFFEC,
0x128F4A355E7BA7AE,
0x024929E54C88D81E,

    
0x0F07EEC500E038CE,
0xEAA65446AC941AEA,
0x656D686A3E6DEC13,
0x6462C89537549ADD,

    
0xAF102F178DAC0687,
0x8FF20F0AD7EC54F9,
0x303B785BF277023A,
0x8373509CB743F0BD,

    
0x20596FECC57B6AC7,
0xBCC2B3CF25EFC898,
0xDE2C13B91096CC60,
0xE4F401A5CB0484F4,

    
0xE4621FECD35CF752,
0xC52D171E1181A6D7,
0x08D9EF79581167F1,
0x5FDBAD4C4D43C147,

    
0xEFD28D09309A64DF,
0x166EB7DFE40F4454,
0xAFF2E785FD6E29D0,
0x637B934F30BB3CCD,

    
0x57A0AFFC90248BBD,
0x99A0F431A70E6BFB,
0xE96B093F3348A98D,
0x8E32F280297D7DEC,

    
0x6A067A21BF1CE9EF,
0x2920B3E9AB9E33A5,
0x80C5DE3640E59AA4,
0x891D7761D77EF9E0,

    
0x05C56BD3A816B51A,
0x6D3E331569B250DC,
0x9627F25C283AC191,
0x985FEEEB7E150AEB,

    
0x004EE6C949D8E7F2,
0xF1B4703BB87EC989,
0x6D70867FB5FD3E47,
0xD9F07570F47A9581,

    
0x27B8AC6242D68BA0,
0xD345A4B3C8A9BF07,
0xF8556593D1B7DEB2,
0x416693233DB36B9B,

    
0x8E3AED465E03D5BF,
0xB09B5926D759B010,
0x83D4572753357363,
0xF24C12A80A9C7C33,

    
0x4E56716961C4E717,
0x067CFDE4F86B1E21,
0x2331851D73F3FFDE,
0x31613EFDE0BD8191,

    
0x910C6189C9BD553C,
0x84E6027E65168E63,
0x5E11EA7C3BEAB1D9,
0x09C3B7C3DAB1FF64,

    
0xF633C22553C0DA54,
0x0E65215F64AFDF8F,
0x17F83F580AB003ED,
0x9748CD5AF6532268,

    
0x6446F901297C2CDE,
0xC42ECEF392A04C50,
0x7DB0566F24978C1E,
0xE53C2E00B4654E75,

    
0x1A932AE0DDB09961,
0x04B95277D351EA07,
0x71D0D319E6D397A0,
0x750C5E3CEF0EE2DC,

    
0x818531C3801AA991,
0xD04F2B87273925DD,
0x82E112B2D142B65C,
0xF017C117AA615C66,

    
0xD17BF1FB19C3C781,
0x376E2502531442ED,
0x24E736E492F88F01,
0xE09D2BAC68F43418,

    
0x787BE013E285D816,
0x8D005088F4C251C3,
0x890393932D93208F,
0xB5671CDB536470F3,

    
0x4CFEB58056B8B13F,
0xF416D20257474FF2,
0xBB992B927AF7348B,
0x43F9F314CA7A898E,

    
0x263345B2E17F8887,
0xF23DF01BBAD696D4,
0xC4B062BB54D6A535,
0x620FBE1F24A7CC63,

    
0xE2F1E98DA34D4D41,
0xBC44E6613B5ABF51,
0xA900CF57D88AE885,
0x83B9CB6B0AB4F2A3,

    
0x862A32257D60E544,
0xF676427F881E3853,
0x9D37A07021FFC541,
0x17A5AD5C00E7D861,

    
0xEBB901D78551EE56,
0xE0EB7DDFF439CF21,
0xD4AF54265A5F8C7C,
0x53F645EC80C423A2,

    
0x8F1C52C176649F30,
0x102BBABF53CD1ED4,
0x252EE72DBF47E84B,
0x836DB96B16887499,

    
0xE056D823A73A0E04,
0x41316EC7015CE46D,
0x6B23E4940731DF8D,
0xBAC2C7B5B1BA83B5,

    
0x59AC9995CC28CDDC,
0xADF1868A357F7335,
0xEC006E1896FB7641,
0x2FB36B4DB41B8F99,

    
0xF0A356D7648E661A,
0x691FA0234C017EFC,
0xC7922787769BFD7D,
0x1BB40C9099BAE042,

    
0x9745754C5D19089B,
0x6DB884BF86C00FD9,
0x42F41B002DEA306D,
0x9D88AB38FC522F5C,

    
0x071C8D97F172D6A3,
0xBCF76DBC57815852,
0xB24D40FF8F00B2ED,
0x8890F93B50AB4BC6,

    
0x873DADE063B1CD06,
0x5D8C3D2F2DF768D1,
0x84CEAD8C3517E734,
0x15E6A52CCD0A43DF,

    
0x493B6F22AF388717,
0x173FE329338AD3B7,
0xA47B5A2C01E9CB80,
0xD5E8A0F00346F3A0,

    
0x29775164EB2C3F2E,
0xF0EE6B83A3A9008E,
0x6C716AF488DF6554,
0xFE576015B67523B7,

    
0xC26CAC2273783E3C,
0x102C03F2107D4A70,
0xF24965D8807B155F,
0x3BF9A5949FAD1FEC,

    
0x4B94986B1DE56C28,
0x90B7B1872B5BF747,
0x491EEE28B3313472,
0xF3CEC41BC8DA393A,

    
0x38D83A471DF5B0D7,
0x20B465633BE7531C,
0x9A61A6B81D72FC5F,
0xE58F2BADBFAB6493,

    
0x4F70A249B3C1FCE0,
0x51A68D4B4875C89C,
0x94A5F0F0A6E09AAF,
0xE562350A66F9EBC4,

    
0xFD21A000CB2ACE8D,
0x4CF35307B5575C10,
0x597E815CB1722B9F,
0xD08F1C04D2F13366,

    
0x8DC6F790BB3A95B2,
0x5C78BBEFAC95FC8E,
0x594721FC950FEAA7,
0x226698509ECC3399,

    
0x72159FFF47D867D9,
0x4DC5CFDD90DA5F8A,
0xB8284A541A81ECDF,
0x5267B916B16253F3,

    
0x3162715B4D3F45F3,
0x2B97AA1C8013EADC,
0xEC13B91A57999042,
0x82A8F4661D32BA0C,

    
0xE77A740A8829FCCC,
0xB967C92645846A7C,
0xC1EF95EE5422817E,
0x1FEBBF987F0FDB08,

    
0x2E4823F375864C8E,
0x87FDB00D13D3A279,
0x2B2795834672E5E4,
0x6AFE615D5B92B656,

    
0x587B39CF7911DDA8,
0xD5244463976191FC,
0x6D873EFE971BC917,
0x7C8034A25172538C,

    
0x51FEE19B55993FAA,
0xA44574D7BB848BFC,
0xC6842A0AE80C0094,
0x7F2055102C0ECB6A,

    
0x224B57ACB8153484,
0x1DE8FD1B5021E01B,
0xEE5D6926C0ACD7F0,
0x898E11725822B297,

    
0x1C3AEB16D847FF5F,
0x4214ACC8BFB70278,
0xFB202E75A7340B1C,
0xEDE07D0F47821AC0,

    
0xE559F4EEF2F05C31,
0x77268ACE51AF3466,
0x2D48F6158D177523,
0xB9F6AE7ED30BF06F,

    
0x9A337254C75EBCE1,
0x3812A308E7A9CB6A,
0xE1BA647894070871,
0xF0EF35B38A7B683B,

    
0x59A4689D1DABCADD,
0xC292593C695FEE5D,
0x2974081A30BF324B,
0xF004C1177408ACC4,

    
0xE52A82437B3D67B4,
0x1E7FD9ED8C999745,
0xEA7EC4DE678E69BF,
0xF05D35DEEC565CFA,

    
0x1AAC4E9F68E188E2,
0xACD0E0F5E95C7CBA,
0xDDEBA7075CFB423F,
0xE45A2932625B9C15,

    
0x76CDA395F186C523,
0xD991AF00CF28DE63,
0xE509122AA39CA6D6,
0x939CC5B8346C54C7,

    
0x1872E76DBCC2EBEA,
0xA6455C9895E96C2E,
0x34CCEA48D64A93DB,
0x16FE193629CB7872,

    
0x8A12FC2217E580A1,
0x10DCBCBD9EC1337E,
0x0BEBB0139F735B42,
0xF48A07A3995B5CE9,

    
0xBBDD47872BBB4A14,
0x55A88C58033ECF9A,
0x45A3C9C2520CB334,
0xB5349423FDA9EA47,

    
0xA556A3B708267A87,
0x375A0420F90C8DBA,
0x5E267B51CF768655,
0xD801B14A40DE2B10,

    
0x7F1DA004D6CCC04F,
0x8F3B2B4A91AA3C12,
0xE3DAC3164F04A444,
0xF1D5E2C4C1822E6A,

    
0x9E29FDF306DD5783,
0xA25CA692E3C7D7A7,
0xE1BE09D412786AEB,
0xBF452E9CF834AA05,

    
0xB1F1221FDC639E76,
0xC5D52A0A31887CD0,
0x9A475DA5ECFAFAC3,
0x046B8106355F4739,

    
0x780F22CECB332054,
0x6208AF14BF69DE62,
0x327E26724A9ADF57,
0xAD5D68B8CA05171B,

    
0xC5AC0270062E9BA5,
0xDE6C64C61730D6A8,
0x159922E4C5E1232D,
0xDB03FB2C5170CCBB,

    
0x7683B178DD5DAB29,
0x880AC914AB3762F1,
0x348791EEA69B3F3F,
0xC6DFCC0EA100A78D,

    
0x52EC9558C7422370,
0x87AC552DCD31457B,
0x8C80F95533EA60FD,
0x788C672680667385,

    
0x88CE84FDD683156A,
0x1566BB64E0876DE6,
0x2B7B11012E4333B9,
0x564B8F098DD617A4,

    
0x184ED70894A790C0,
0x9D0F8F75E3E497A0,
0xC1FC5B13ED437B9A,
0x8FC05A43BA229E7F,

    
0xB71C6FB910B3E796,
0x8AE9082F16780DB4,
0x3CF2C91B5F0E03F7,
0x1838BD498B901B84,

    
0x665410C3D03F8D2C,
0x368DC78ED0E32185,
0x0054926E0CF63941,
0x1309638ADEDE8D24,

    
0x335A75ABA51A1A60,
0xCC42BC6FFC1FCD36,
0x3E7DF03A9AD0B1DE,
0x7CD084BF556D9463,

    
0xD319C334D3DC8C6B,
0x879259443838AFE5,
0xD862C1F73852866F,
0x5A2EC01CF9768A39,

    
0xD8F8730BAFAC4558,
0x975F6CDC991BA4DE,
0xD78860352F7D258C,
0xF7BF2709303CB575,

    
0xF369693F0603382D,
0xA42FDDC479B4E417,
0xBF2B5990DE961BAB,
0x3CE135AFE1AD29B1,

    
0x08D844EA64B1D6E6,
0xAF75F003FFEF9387,
0xC6BE1655314A2A41,
0x5280583CB6FBD4E5,

    
0x83986478976C3802,
0xAD70B26435201CE1,
0xC1FBBDE66869CBA4,
0xAD80EABAE3010CAB,

    
0xE3F8F9D49E81B025,
0x7F50C6F8FF8E7DF5,
0xF43A14894F670662,
0xFB9A5E022F2524F7,

    
0x2274204A3EFF7D22,
0xDF8F0C1DA6DDD254,
0x535A1BB04B3A8D06,
0x846E62B515130069,

    
0xDD4CC4935E96410D,
0x4EBDA134A52432FC,
0xC42D3886419335AD,
0x4E6D7C85D26CD3C3,

    
0x12F6AD319CB07FE9,
0x3DC72082DA17918D,
0x0D7D14D0C572005D,
0xC1CD2C766570D4EC,

    
0x5ED7DCF701D9203A,
0x9C34F4F72CF4EBBA,
0x03BB347A2F5F25EF,
0x97BE8287B0857E79,

    
0x7EBE94F3578B2C73,
0x7884646E54C775B0,
0x645BECF43E5D299E,
0x0851210C0215EA6B,

    
0xBB5CF71046B5336E,
0x2488DFD65FB4ADFE,
0x15345E984727B57D,
0x9D0FA0570F6AE535,

    
0x1FC238FEF9F69D68,
0xB77403F4082BFBA2,
0x5116F2B95EE568AD,
0x36C4C31FE479179B,

    
0xDC9112FE6C1B0A32,
0x70CE7FF2D3BD6EB1,
0x54F9310170CA0C64,
0xFBF7A7D12FE82FCB,

    
0x49D3A0C13AFCCF0B,
0xE5ED41EDF297DF90,
0xF70A076127D2BAC0,
0x9CE3F2BF01B52FC9,

    
0x450DCCC2CD0CEDFD,
0x6CB78FF9F8A024B7,
0x00768327C196B39F,
0x1C8EA1BF0EEDD6C0,

    
0xB8723D943DE11D51,
0x2C6C7539882714F5,
0xCA0BC14B7896E788,
0xAA80028260D22F0E,

    
0xE86A6FE7D41A72F3,
0xBACB9280AFA2CDD7,
0x2263555F600C9B8A,
0xA2BBED3760E623D7,

    
0x898700971737E326,
0x6B9F84407248A962,
0xAFD34E682D841218,
0xE7B7DDDED0958C21,

    
0xF3C2630755829C71,
0x14129D3883D68295,
0xF6818E8FCD01DF89,
0x61A988FF3E8DFC0C,

    
0xFD7349760EBB38F1,
0x316CD62290D11357,
0x09A6943D8D49933D,
0x6C9EB748DCDC8C9C,

    
0xBE72C12C5399BBE2,
0xA9E224857FD610E6,
0x427BB4734886F3D0,
0x10F9CEE29C17F6CF,

    
0x036EC69A0B5118F6,
0x0D17542983546E67,
0x987A2C9CE70695BB,
0x120978919102AE59,

    
0xBC2C9F7A0C30D28F,
0x00895DD0F4FF3FB5,
0x2C6751FE49CABC84,
0x89490478F3D94896,

    
0x39B05F1D1143E9C3,
0x6A71AC9FACFE2F18,
0x9344D3A403B30DE3,
0x895D3286533BF9F3,

    
0x205DCB1F2B3A4D94,
0xA84BB49E0FD0137B,
0xBE1CF9833096755A,
0x05CEEC6254A9AF0A,

    
0x62AE82C3C1C7CC60,
0xB692EEC031F2A132,
0x37303284F8E99167,
0x3D6DCBFAE9F0BA0C,

    
0x2C8F5FB67FA3AD09,
0x8BB43FC7E957EE9D,
0x4900735EED09F6E5,
0x719746463D50CAC9,

    
0x07A786CD6E065FD1,
0x03ADBEE210663AF3,
0xF898868DCFD52B78,
0x04D56CEA9E98B70F,

    
0xF4384D7D1F2E7D3D,
0x633DDE26BBDDCF49,
0x166DB136F2030F07,
0xBBC63558FA333527,

    
0xA13F29D20FC1BAF6,
0x54DE6E7A3589D508,
0x44974CA49E1834D2,
0x3B89026FA57F318D,

    
0xC16F0997409F84C8,
0x71563D5F35B88378,
0x5FDB12BF825D6E45,
0x6F1535475B465505,

    
0x5BA3A318FD9BBF19,
0xF5169D5D239E06E8,
0x1141968EE949061E,
0x4935134FBC124531,

    
0xA5CAFD5273BD2D1E,
0x7A4C484F551D1AD8,
0x0D16482424B10573,
0x869EBB4877119ED5,

    
0x98DF591146D61BF7,
0x17E56350EB23604D,
0xE46EEE4A8ABBFF87,
0x8A454A88ECC2ED9A,

    
0x77E5FF6E5E272094,
0x7D67B8E9E5D94001,
0xE8C248D6E37B05E4,
0x541A5371CCB2F0C1,

    
0x8363FE6EA0AA3D62,
0xCD87DE5D1B1AF03F,
0xB0A14FED98AAA4A3,
0x5F6342412EEFE612,

    
0x0AB6B062E4CF8A68,
0xA9D5C534C7F2DBDE,
0x0E07F943A9D5F617,
0x141A3DA92A20B95F,

    
0x56BA54A68A868DE1,
0x2FA08211BFBB5162,
0x62462F9AD0B9BF5E,
0x704FC56CF8BD2C80,

    
0x5B7939843AF6C28E,
0x52CB42837C9BFE20,
0x00E35092B33E0187,
0xA28CD1243BC2DB1A,

    
0x69830583169114A7,
0x32178CCE1D42B051,
0x8631D215B6B249D6,
0x0332B7695DEC6C78,

    
0xB3DC2AAAD8A1A12F,
0x9D714F1588798BC7,
0x9F9A2D7D39CF9066,
0xFFC98D27B06AC6EA,

    
0x8844E075454B872B,
0x519039BEC2BEE951,
0x07F98713936EB8D9,
0x444BB3490953F67F,

    
0xC4531CA4ABA61A88,
0xEEDB8F6FD7F47CF4,
0x35C910C2BAC37B79,
0xDCE2A071FB8C8515,

    
0xCCA3A2EFD236A5F2,
0xE1300D885350FB00,
0x0B4C1C4C415003F9,
0x63AF2A8DD304E3A5,

    
0x8192E17327F9D670,
0xDF54D0B8471F62AC,
0x0A491B23300E807C,
0xCA4D2569E677C68A,

    
0x6AE7064F02503579,
0x17992E1B2C6C5198,
0x3FAB815F048AA8B2,
0x739E5201C889DFF6,

    
0x916D9C4A24347437,
0x5517A4C992474A89,
0xEB40E1029A568B08,
0x5D62757A60B37A97,

    
0x192A2471B41D2573,
0x2EE5E941AB95C8B8,
0x4C52A8351EF87ECF,
0x31260B3517F121F3,

    
0x4DE972AA83F3A6C6,
0x9A873A5699652D5F,
0xF62508B111B99F87,
0x353B4BE81075CAA0,

    
0xD647C996F890BFC6,
0x687F3C4BF6FFD510,
0x9C400190BCEFFF64,
0x7BBA5D56AD6731BE,

    
0x63FA9DB87E66B595,
0xC56916FC69DEE60F,
0xDB565AA1630DDF9A,
0x4139EA86A3330C9A,

    
0xE4FE8B3F89408577,
0x049C6EFB069DA5D0,
0x610D247F4F414B59,
0x7A495F3088C6607E,

    
0x4C72CE20DB96E1B1,
0xB2FA1C8A323553FF,
0x3E05C69A792DFCBF,
0xE87DB7455D50F3E3,

    
0xE9B0E02DB52547BA,
0xD71DC114D60A6B4E,
0x72D412A89E90143F,
0xC4C7BBFA2991B1BA,

    
0x9413CDDEF5708FDC,
0x87A0C3E7B1705194,
0xECBF93AD94F426BC,
0x75C0577E9B8DDB9D,

    
0xE7E477105440E6AB,
0xD30D5016A907EFAA,
0x8334A34ACCDEBCEF,
0x5B76486BA3E5B881,

    
0x1F42B364AA8CA380,
0x84684250D1BC6AF1,
0x7121C692DB2D1039,
0x9F3B8A66F825FF0F,

    
0xA4097234BA983EBA,
0x1FD32F398A4189B1,
0x49641EDF9887421E,
0x12C1D520FEA29C9C,

    
0x085BA2B566D2F941,
0xBCFAB512DC50454C,
0x3096849A347339A0,
0xDB91E7593C31E391,

    
0xAD244D2D9570D1BD,
0x2D9AEA7B2ED41D23,
0x7644F91517DD1816,
0xAD60FC40B7F75CCD,

    
0xFD10929652E1423C,
0x39E4A1215C3AAA0A,
0x02428B9C21665D99,
0xBBB2DA6968EFE484,

    
0x3124FAD80178D70B,
0x1CA50C0061A0A398,
0x2610929E8F075EC7,
0xF8E767C8CF17C497,

    
0x0849BEC0578D51AA,
0x018F66D6A41606AF,
0x28AF8395518936F6,
0x4BC58324541C78FF,

    
0x32C67FEEC5874CEB,
0xF57C05A94487AD55,
0x14A4DAB89679A089,
0xE88C5F68B738119A,

    
0xA4C1646327110FFD,
0xD8D08B664F4A61A2,
0xF0A202E96832932F,
0x0D36921EFADCF9D4,

    
0xAFFD27BD4294F4A5,
0xCE76AEAED66D5D30,
0xF5501BD8B012571E,
0x57F8D903F14E356B,

    
0x42CB0F90B26D1095,
0x5F30EB31D9C14B6E,
0x09EA83DD99196FE2,
0xF329CE500F5131E7,

    
0x868FB5375F79E3E0,
0x7B760AB840714F61,
0x0E471B98D1BFFC9C,
0xADF9AC0B4A07C0AA,

    
0xC44D8826F3EE437A,
0x8239C93311423449,
0xE706D97846EA6871,
0x87F7C137627C51C0,

    
0x7ECC400C0127B399,
0x2C5EF531D9465F4A,
0x838869B3CC701598,
0x50DFC6ECEED6F0AA,

    
0x3D362168783AE1EF,
0x9F9DDFEBFD7E4EBE,
0xE8529B1DBDAD098B,
0x75338CD8138BB40A,

    
0x487A09A9DC642753,
0x4656ACE78D126B7E,
0xEDAAE9F0DA64373F,
0x85BFA18C23173AF0,

    
0x5FA8C870E1D2A43C,
0x7EBF3C48DE6AA177,
0xA08368FB98ADADDB,
0x36022E3D57C03494,

    
0x48F6F267BA219D96,
0x9B0DC158E1BE34E6,
0x4359F25EC1BDADFA,
0x73792899E1B4D030,

    
0x2EE1A4BF74AA1BE2,
0x03741B6519DD9EE3,
0x9B166197551C358F,
0x6ECDB9A53A19B03D,

    
0xA809F9D15D25BDB3,
0x9602606C100BED11,
0xB57E2C1B5F6F0B15,
0x24369A2E7298F30A,

    
0x0559C306052FAEA1,
0x508B056DEA0BAC97,
0xC749E44823BA29CF,
0xFA589004F6B90B7F,

    
0x670A7DCCD14B6355,
0x0DDA94B3C462D462,
0x06AA9EDABEA01D00,
0x6877F4314BE1B0E6,

    
0x3C704CCF250A3A66,
0x75C158A00255D7A6,
0x3849759C001B0C84,
0x1B754800C99DD774,

    
0xD93E37FD2F46B5FD,
0xB53861391A0CF6C3,
0x7A0F76669E3B6CE9,
0x378EB3612925E7A8,

    
0xC03E453E4838F5FF,
0x397EA3E2FFBAD35F,
0x1165FF0674872CD1,
0x31D93B9BFF78399C,

    
0x68E3BB34B7C1D9DF,
0xBF39058556632B43,
0x593EBD812D45045A,
0xCE4CC87B3D0607B7,

    
0xE03C4E1AA7B30FAD,
0xA469B3B304B2F57B,
0x5BB310808E159B0A,
0xEF13DAE9CD3786A4,

    
0x3CA8B7820BAA5D44,
0x4ABD9ACBE2D44EF8,
0x7AFDF80197894A3C,
0x31F19D94B14D2C16,

    
0x8AAA3431CFF530BD,
0x27B377863CFBABF1,
0xF5E6820F21C39D7B,
0x3EBEFD26DA7D245E,

    
0x767460062A091757,
0x35F523AD1E9F03F3,
0xA1187E7A39CBF2E9,
0x82A3BD19B0DEB74A,

    
0x2991080D7210620E,
0xB860BAFBEFD4B5F7,
0x172C212FB4D9F0B2,
0x5647EA46CAF6FCE8,

    
0x976C3945619C7439,
0xAE0FBCEC61222E67,
0xA0CCC46FD5934C8D,
0x050EF398A841BFE0,

    
0xF22B9798381F813B,
0x5B4C38B4E7651670,
0x105E68A65387F6A7,
0x99E40BF7C0290B48,

    
0x6CF9441235A94EBC,
0xA35E372624538E4B,
0xC5E4DE7ECC770F16,
0x754A8B1872542416,

    
0xD12A7C8AAA405EB1,
0xA365B39F9038745F,
0x5E7BF98B898AC1F2,
0x77C431E8CC554A20,

    
0x151EF035F469771F,
0xA09A9DA6860BD2EE,
0x8FC08C0285F5E95A,
0x5AA9F07DCAF7523F,

    
0x433CA07C77FDEDB7,
0x3B3A9D62BB2FFC57,
0x6A4687FDF5C5841B,
0xA00A83028387C1C0,

    
0x8FCDCB09A8C07826,
0x946B3414B6DDEECF,
0xC05AD8F7742F73C0,
0x8D41AA6AC4A1B62B,

    
0xF2FE80E8EA9EF41F,
0xBC533E11A0F68D0D,
0xA8C41D0927025C04,
0x8E306A22C35FA29A,

    
0x0F98861003292C58,
0xAE73A1CDB6708B1A,
0x6550B8DE87EB9C63,
0xA6D820E83D157269,

    
0xA0EE55AE508FE3AF,
0x8904D53AB5623D13,
0xD181DED97D8BF4FC,
0x9F6551535BA9725D,

    
0xD3968357C3BAB40C,
0xCDDE2BC1513B6243,
0x1EFC6A475DF2D9C9,
0x0559A37F6F07FF1F,

    
0xED4D34B26C015FE4,
0x9756ADF106F0A712,
0xDE2835794AEF9FA4,
0xB109EC6549948355,

    
0x86EE760A266DEC0A,
0x5E9D3EDF8D9887A9,
0x426F76C717393FB2,
0x1E7EC484B9ECE9B3,

    
0xE5AE0E1E8F3F7876,
0xE74C3ED6A4E5FC61,
0xD7DC922D7E201F68,
0x87DC4207A85601F1,

    
0xE691D343168EE9DF,
0x831753275CCAEFA4,
0xEE7CED48495B0FF5,
0x7794891CC895234F,

    
0x13C4BBEBB5D71859,
0xA9254950B8B34FD3,
0x90018FA06C78CC8A,
0x83F2A694F0F158D7,

    
0xB0C30AD2C0F01233,
0xC98EEC4C69C54FED,
0xA7FAFF80ADC5459B,
0x2D7FAFA0930A2185,

    
0xE1C0A948E4F79DA1,
0x7051FB224578706B,
0x6A4E146603ABB4E0,
0xDEBB5EF09D2B87CF,

    
0x1BF2500CF91E9BA0,
0xDDB8EACC01E8E577,
0xB6124DA964EFC07E,
0x8A26F43B96609F8C,

    
0x9526B73D17A93CB0,
0xF7089B95C90829D5,
0x5BBD958988DAB1E3,
0x9D3AB4001C3DCA04,

    
0x20FD4C54AFB20FAF,
0x3EAE6B0BCF15A612,
0x91A90342BA4BA7B8,
0x2F3D2A65CDF35FDF,

    
0x81BB39AD13EB1379,
0xF022110025DD8019,
0xF83A67C83BBF2AB8,
0xFD26D59A005B5DA9,

    
0x155BAF9606683E1B,
0x4BDA77CE51471C79,
0xACFFFE5D2A8DE27F,
0xD31761F3335A38C6,

    
0x6CEEDA6DE5443C92,
0xAA51A6CDEC3D368C,
0x9A571B10EFBDF79B,
0x9C93D97F6CFBD6FE,

    
0xEC37C1BD15B6F583,
0x6C6C53E356017D9D,
0xB7323C87D28C493B,
0xF06B2343F2D9F584,

    
0x7EBAA23423458E9F,
0x65AC54DEF1AC4485,
0x0D7EFB1985969EE5,
0x9156884FF4BF8CF8,

    
0xD400EF0D75CA3A19,
0x6F4A5E9330457675,
0x8A444DD6ABB1BA41,
0x0C563CE58EDDBC45,

    
0xD4163B9ABE2916C1,
0x4A48696355A19439,
0x6B9B0B4685EB8DF6,
0x709FDA64FB4D9682,

    
0xC3B46D879A41B9A7,
0xD055831DC228E896,
0xFE42755F9DC3DB7E,
0xB2FFE8BA53A09C15,

    
0xADAE5A6B8C2EAA49,
0x235EA53F3F1AE8E2,
0x742CF7554F701E1C,
0x002999E17792AB57,

    
0xFFD3B7BEC2603CD7,
0x72FC32A3D7D79238,
0x1895AAD115904420,
0xA3328212297379ED,

    
0xB9E5F909C35FB49E,
0x1FD594C49BC53338,
0x1473AA0541CBC65E,
0x9DF82A0419AA4FF2,

    
0x3BFD7E9698331CF5,
0xCB461ED8747F875A,
0x1B749E22557654F6,
0x7285422BE2383D1D,

    
0x56EC13E727555784,
0xC80A2D3CB7A580FF,
0x03EA8AA6CE146FE8,
0x7C20AD21D72B7F47,

    
0x87D363CD98972261,
0xC4837D640F4080F7,
0x8369B3E4623184F8,
0x6BB8A385C41CEFD9,

    
0xFE011650A7C3BA6E,
0x387CB2D60AD4B8A3,
0x583C98498DEE211F,
0x360BCC449B3C2565,

    
0x71B82039316C11F2,
0x8F425DF63858B4AE,
0x3B82981D84691EBC,
0xD8183B9C12C39F65,

    
0x3EDC92678FD2041B,
0x3F5EA1358C8FC767,
0x5E86F40ADDDAE521,
0x6EA16FA22B0335D7,

    
0xEB6D1AC819308496,
0x620F9DE60A894E34,
0x281E5B9B4787C85D,
0xFAF30A72A01F75FD,

    
0xA372A7ECA82CCCFD,
0x284DE9E0DBD45B6F,
0x213FD62E71AECB27,
0x30F5AF6912C6E1B4,

    
0x3170A2E6488DBA86,
0x3F0664288B696431,
0x326BBECA809EDB0E,
0xB7DED7827D461620,

    
0x596CE95B2A26DA78,
0x4979E50F29B69949,
0xE932706D1C383080,
0x670B859D8A8F9982,

    
0xF9AED4A964589783,
0x748121E5FEAF0596,
0x0B40FA2A4A4BB390,
0x80D6BABBB89379BF,

    
0xD4B6DDE284E67B7B,
0xDD3AA97E7D3DE06A,
0xA11EF777E1E3082B,
0x65CEFD3098B737F2,

    
0x5FDB8AC8EBB608CF,
0x64E53DA0EA666C2B,
0xEE7458ECC1D4FF45,
0x74DDEAEE2734B5C3,

    
0x3A294B94721838CB,
0x187F08B7B1E296E0,
0xBE155C3AE63F0DF4,
0x86228ADAAA0789C4,

    
0x34F24ED7CA2CFF0F,
0x2DE5DBE935F232E5,
0xD4BAB988AEAC5140,
0xD1058B448A827DB0,

    
0x13774ED5D4742F56,
0x4278DDA1830DCFC9,
0xDAA37F89FBBD09B0,
0xBECCEAAEC3DB6E07,

    
0x0E501665B647C557,
0x9A668F858B3B7F62,
0x607DCE8145C7B404,
0x0A2E5391F5DDEFA2,

    
0x69F958C3A1EF6182,
0x22943DA6F99D3311,
0x86D45B514266FA49,
0x2D3928F5C476FB41,

    
0x3DC898A1DF39F203,
0xB61137B9CA69A2B3,
0xD81E959A861E5DBA,
0xC3D1BF72F72B2CF7,

    
0x7BFB2B40757C81C1,
0xAD4A4F20ED35B6EA,
0x68EE23460E083420,
0xED161B8451820C3A,

    
0x52B06505DF76C44E,
0xB5D823F88D025CD9,
0xA3E6FC9C5196523F,
0xFBE487B43346E998,

    
0x3F50B937066707D4,
0xD7B6D99A05A6855D,
0x4854BB4C507CA983,
0x7CE5D62B8D0FA9C8,

    
0x90E1404E2D65D88B,
0xEC7B2C174B2DF3E7,
0x8998C03677DFA159,
0x2D5F3810674732FC,

    
0xA52F2669B1D1863E,
0x6DE0C94348AADEB9,
0xC75CACF53C3F6298,
0xF96410971A2D20CE,

    
0x9C656CAFD6AE4DD1,
0x54E0D455D5A6A0EC,
0x559DF1C626DB3C25,
0x1DB9B13E67AB5B1C,

    
0x15DA9CD3241DF2D7,
0x0A97A2EE8F389A4D,
0xE6C32D8F34F9C2D5,
0x061AAAB6218B4E52,

    
0xF47878362AD6E73E,
0xACAA61FCB05BE1FA,
0x7C263C50E8607386,
0x0003CBEC27E31F6A,

    
0x9573455F7A869FE3,
0xE630889A702272ED,
0xA5F5019CCE52C1D7,
0x0FF6C694FEC10AD6,

    
0x15ECF2A39A536890,
0x4A25A599822AB7C2,
0x44A6C1CF92EE1ECB,
0xF209C69ED5FFF85A,

    
0x965169B72C0130C4,
0x843EA541EAEDBF6D,
0x60EECC16A05D736C,
0x2BC557B6B4CE307D,

    
0x615D207B79555A1E,
0xC99F73FCAE632A47,
0x8249AE76C139B5A9,
0xAB3865A54D4E4473,

    
0x4D2E56F0472E8C18,
0x77704DE630113581,
0x9C203C9011747B80,
0xD181C133A28320B1,

    
0xF8EB4C3139E01F36,
0x388067635EDCDA92,
0xD7C6C3BD67B5FA83,
0x1CC70B9C185DF2FA,

    
0x3C7877CB945DED01,
0x7A8ADB6FF1BD038F,
0xBBE4034D855CDC55,
0xBBD9EAB8DFE4A4D7,

    
0x1B1A1DAB887623CB,
0xB8EE92B89F803745,
0x11C4481FD5564BF8,
0xCC6823FA2E65D21C,

    
0x1810B0300783493C,
0xF33AD29D8004AFC5,
0x35E65D8BD545AABD,
0x9A22B249A39583BC,

    
0x0B76408FF573168D,
0x737F179670E6D67A,
0x60A651987FC0B596,
0xFD1906E64CE31BD4,

    
0x0D19E37F3D3A8842,
0x3FAD50ED5522DE43,
0xE180F5EAB3018EA7,
0x2A1BBA1EDACE3235,

    
0xC32531F0A9177C25,
0x4A06A157A337021F,
0xE6FA2408585D088F,
0xBEDCE78BAE3BFF20,

    
0x3B4BC8BC94E8D7DB,
0x835516392CB857F8,
0x959606B15975FC95,
0xE53592D36A4C408E,

    
0xC9565A59517FBBFE,
0x0AB717D3D5C82072,
0xB2DB6C508A301233,
0x505010F6A5DFA0F5,

    
0xE2EA0F3698D720CD,
0x8CEAFCA92D9E473C,
0x5396FD7CE43A7925,
0x976CCB0985151D1A,

    
0xC42A9890BB894323,
0x2DB101D2145D4443,
0xF6D51676BC790750,
0x184D06A58AD974A4,

    
0xEBC8EA661A4BDCAE,
0x68C06EA71B07CCD5,
0x83BD09B7E64C795B,
0x4D4CBB16777267D1,

    
0x80235F042A8A3830,
0xC3A9D4E107332FF7,
0x5C4BCF6E79BEA333,
0x1E0D5E043DB60CFE,

    
0x320BA2BD7F29F9DB,
0x95CEA4D472E01B43,
0x32E127574BBFB538,
0xB0DC35E7FC1FC565,

    
0xD90F7FDD6E1DF893,
0x4B51B12BC97DB20E,
0xE388BB00FF15E3F8,
0x58B2480AEC373196,

    
0x34231E7D8B415F15,
0x38C551168729D22C,
0x5A2FF82AD7D3CC1E,
0x7947578D9DC90C1D,

    
0xFF1F26CE4AB1A7F0,
0x6896D3C90F2DBC41,
0x4828D8C44C0B2B2D,
0xF1F124F93216DEE1,

    
0xA7C8F17D0F8A5415,
0x1C4D7B16BF0AFE18,
0x53CAD9ED98924839,
0x35CBE95525E98B50,

    
0xE332A256F3BA458A,
0x8AB19FE12B60399F,
0xB366ACB5310E66C7,
0xC45B4C8163B33696,

    
0x717CBF80B4403E99,
0x93AD1E2A1B9C271D,
0xC8E417CA65910219,
0x1BE329E7BFAB440C,

    
0x7263EC155A0CE028,
0x5628FE9532B21B57,
0xFEA657259261A884,
0xDFCA68F6281347EB,

    
0x1B72CCFC132F70A3,
0x2CE6D1362323A2D7,
0x6570A4EAA2CEEC86,
0x43783FD1B6C1E2E8,

    
0x8930A790B578218D,
0x93D990AB9F914803,
0xA3FA121C32C94838,
0x4F8F5A563E4694A8,

    
0x6820798C79C2497E,
0xA2152197F20C55A5,
0x0675FCC359F8AFBC,
0x68EF7352085BF60E,

    
0x28C9AF91A40CBCE3,
0xF73F1FBBE96727CA,
0x20A16AE084CBA03C,
0xEF522DC5636E0E0E,

    
0xB8D75A2D50A7E0FA,
0x7DAEF34499452F25,
0x95000422BDAA9DB4,
0xA790B4F7E30C9110,

    
0x560B3C3D280730F4,
0x7A9E2C6DEA2D2BCB,
0x54D3E48AD9D77FF0,
0x6FC0F5181B19E24D,

    
0xD742F1BE1C1CCD13,
0xFC57A854A8A07E03,
0x6615A807394587AF,
0xD7FB32C0D2464BF3,

    
0x4E66959D1B62F391,
0xCA27EE8E5683B217,
0xAD9D1349AAA8A5CB,
0xF1C373BBB782C4B1,

    
0xAFB63ECF50081C76,
0xC1D2053935F19B43,
0x9F1B973B1850E44C,
0x498EDB0630F729C8,

    
0x060B03627E65B6DF,
0xDAE64F834CB0DEB1,
0xF28AA28B4889A032,
0x30A0D4E5EB360616,

    
0xEC19FC68B9220B68,
0xDB0AB4D23F494AEB,
0x321FC5FD9575A126,
0x82A048968F355701,

    
0x402869F9AB51EAB1,
0xB3A22A746CFC62E5,
0x3A2EF159BAB10307,
0x9349BD8852C6B415,

    
0xF26C6B77FF779688,
0x861B9FC2DC7BBDA5,
0x7945AB26206E73D1,
0x531FF7B72F8C557F,

    
0x6F7D29F49321EA30,
0xAB228CCCDA8C8006,
0x55B2FD2B5BB04DB1,
0x456838E3C51BDE75,

    
0xBF48FA4054C2D73A,
0x99FC3D615593569E,
0xE05EB08465F79C4C,
0x0B1F63DBD1EAAC66,

    
0x6CE097BD79E3DAC0,
0xDB939CD1CD66A544,
0x2C37B1CC0718F35D,
0xC3F5400AFD0515D0,

    
0x18E60B5871A321A7,
0xD977CCEE56AAE968,
0xCC3A40A74E056B3B,
0xD379F57836E5347B,

    
0x8C97EE4E4CFABDB0,
0x9DE7A0DDC4D2DE49,
0x84A1DE062B6E3977,
0x86E03A4E6D19A6BB,

    
0x62C505785AD2E6D8,
0xCADE3992C6D5550B,
0x0E1DB076584C0116,
0x41D93B57F29F8941,

    
0x215B116E0CA00B68,
0x5EBAA0D3FFEB024B,
0x5C75874EE6D02F2E,
0x96F52DB4F2BAD3F8,

    
0xE723D1F49EB5DA2B,
0x41A23B0144586807,
0xA31D500F78DA2F7E,
0x90C0734237239803,

    
0x8711BB05A5AC0439,
0x5BF040A5A5160CB8,
0xCA450A06C0F5B144,
0xC7610BED93317AA1,

    
0x65770E07F4298845,
0x2D30DE1F8013EAB9,
0x94485E2F86E62EF8,
0x85BD05692685A120,

    
0x852E9423633440DF,
0x1BCD6172A749AD3B,
0xD2C70CF41DEF0778,
0x9DC8BEEA4C0D5E2A,

    
0xD18183490CA00FB3,
0xC32D1DE41252562F,
0xCEC3FCCF4223C316,
0x02505BD96496C634,

    
0x5EAF8A9F76FF2994,
0x68AA5F6B61639946,
0xFC5189002A3A8E0A,
0x939477B4B1153C85,

    
0x8F9964DEB76F0E31,
0x8650DB15EFF4AEFF,
0x625E761985230BDC,
0x41566181943D2D80,

    
0x65B7E1F9681393B6,
0xB8A2AB9FE4B4C3AA,
0x2BA3065D42576B64,
0x029C89157CA66BB2,

    
0x2135FA622B6D1A24,
0x5BA4B4F8DF00F38F,
0x4BEEE99F10C6B7AE,
0xC039A76495E1FF03,

    
0x4FD5E2A83C143DF3,
0x00F8EF0351AE9178,
0xE12FC929A07743BC,
0x5761213BB99F3FD3,

    
0xE0E7CF3BCFB6B039,
0xE3ECAB1F31913D73,
0x20E64E6C1EF1B2F2,
0x083630F16D692007,

    
0x0730AFFFD25BFD5D,
0x4905EEC6382ADD75,
0x5B9CF975E8140C66,
0xA2566748AA1E97D7,

    
0xBB1D10D595DBE5AB,
0x965AA79486B9D1AF,
0xBF6568DEF3EBE49A,
0xA8D46EE8588B741A,

    
0xBDC4A8F6861D7A56,
0xB71CEEE165B641BF,
0xAC822A0D96A7F724,
0x2593161D8288C9D0,

    
0xE5AF0A4BCE9539BC,
0x51444CD211D672CB,
0x30A27D98ACBCCE48,
0x14D2504547AEC0AB,

    
0xC39AECDCD5E171E5,
0xD91172C35E07F728,
0x1408D1EB258B54A9,
0x74959DB79213E89D,

    
0xB1200F21497E2922,
0x419E4B465B3A7FAF,
0x7E62D7F1D6FC2E94,
0x0AA36315FA866A0C,

    
0x8747DA3C126B39F1,
0xA2F1E14546A4D506,
0xCDFC02C9AC6E1127,
0x44A44D6ADAABB8A4,

    
0x34E78D95E1C52736,
0xC5CA2BAEC54ED60A,
0xBA6C3794AF307BB5,
0x95AAE56430FCACF8,

    
0xB4A6642B0E0221B1,
0xD8659483F4436F8E,
0xC8ABD6B24F67601B,
0xBC815F8F73046BDE,

    
0x203C6F0AF3D1D24E,
0xC1E6CEFD8E80D533,
0x1A7303A3D5253D96,
0x90E3F7F13C1CA054,

    
0x2D48E92F32B48B58,
0x45EEAC338513073F,
0xA32EAC5E174EC181,
0x34F44F691E4AF562,

    
0x50A0C937273CF5CA,
0x835730ADCC3DD9B8,
0xF316D31B8F71D05C,
0x567F91D6917DFEF7,

    
0xA6180A2EA1D06B56,
0x9A52786A4A069B49,
0xA27E763B87E1994E,
0x2E7F9307D1712793,

    
0xA80CCA3AF037CCC0,
0x521C9078DDFE7D6D,
0x1D31E13F1D7D16D9,
0x49EF261C49C7F85F,

    
0x0B6DD780E4771E43,
0x764D899B54A86B11,
0x244FC908E5BA0525,
0xD8B01ADF446FE316,

    
0x6D3613D45FE8007C,
0xEDC9A3C192CDF0EB,
0xCA7CFD41D13AE30B,
0xFF5058FF968B6547,

    
0xBB90326AB5F0E179,
0x44B8B594500833BF,
0x3A71050121E9D736,
0x150ABE8795807383,

    
0x44F2F400E900149A,
0x157108C2DAC05D34,
0x6EFE9A1DF6DFD808,
0xA5EF1C5B9B1445EB,

    
0x43A05352BD5EEAA4,
0xAA734973D0997F90,
0xAAA48151F73B506C,
0x7D108283C028CCF4,

    
0xA12758F75C2F861A,
0x16406FC9EBF4EF16,
0x3A1230EFD1C8C9BE,
0x8E908A1D4EF5FC4D,

    
0x3FA597BDE148F3A9,
0xB934483B2CE3A186,
0xBC7EE85833AE9424,
0x166EC157C832E450,

    
0x4EA93541C7C631B3,
0x471E6F6ACE4DCADA,
0x9CF3826B7D4EF679,
0xB9FA8EBCC6FB0BF9,

    
0x885842B8238C9781,
0x26AE3CC3D496F3EE,
0xAD6C9DAC74D5C1F2,
0xF9B227C2AB7192A9,

    
0x7C622E222470887D,
0xC9E226C7DA75F45C,
0x599789C671D7A3F9,
0x50425E4BA689723D,

    
0x8E884C7131856D42,
0xA897C7938C2245D9,
0xC6DADEBC31A823FE,
0x2E4FAB89D248CE38,

    
0x8566CFABEE4382FD,
0xE1B3363F0B003DB4,
0x2DAEA90E8D13C83C,
0x47A25BFA08287E9B,

    
0x9601DA9E0851BB31,
0xA73B955D584EBD7E,
0xDA06BC3F53272276,
0x5D5107865088B58E,

    
0xA16A8875CE413B88,
0xF738688AF1D64CEA,
0x50BD7593C813B759,
0x6F5A4D18BC163030,

    
0x18ED1438F8CFAB0C,
0x3F4413F04F37188F,
0x2726E0E9A84C5F3A,
0x8D2BF52469FF240A,

    
0x1C364FE2EBC411F0,
0xBC76395138BF4C65,
0x6377FA5F1440EABC,
0xFFEDC2B13C88999F,

    
0xCB954751B6C777F4,
0x1F0168F7FF47034F,
0x8DC1842822508DFC,
0x5BFADC94C4F208DE,

    
0xD9A469A42E84C844,
0x92D73F594D4FCF40,
0x6F34A5ACA95F0A4A,
0xBE057EAA515EF067,

    
0x109E5B138DAF0287,
0xFE3AD8D935FA0720,
0x1DB7DBEBB3903CC5,
0x40FA50C17A654B21,

    
0x32D13E06B527E18C,
0x78817DC6F8443DE5,
0x9C0F31E5FC8C373A,
0x89CEBD52BD763ED0,

    
0xF701D50C931E42E4,
0x28C1F8B96E2F2BBE,
0x6B219A70B60AED05,
0x3B8042E286C9AED3,

    
0xB260E9C0089A40CE,
0x36852ECE3B46AB9C,
0xCF5E305D4F9CEB2E,
0xFB1CCA9F01C9B8AD,

    
0x346C99F9E9A5FF81,
0x1D6366204EF1706F,
0xAF5B75339ED5831F,
0x7952C1020C46BD8F,

    
0x911831EDC3200738,
0x2F6160483BD3E2E8,
0x254771990ED3A0BE,
0xAB1FFC8C6892E278,

    
0x513EFF25954B6CF2,
0x3326F2F79A7C1706,
0x1C571EBD3B20F269,
0x3162B8B6CDDE00B0,

    
0x61AA55FB63BF243F,
0x6DF461B8DBD4A6AD,
0xF9821CBEF16B0DF7,
0x0352A517B2ABD2D6,

    
0xAC4EFA779A241BEF,
0x52F26E4488AEB601,
0x7DAAEE164813C0EE,
0x5A6FB2CD914F937F,

    
0xA613BDCD4681DD8A,
0x04FC088404AEEDE9,
0xA26E6A4FEB0CEA58,
0x68518C2127068FE7,

    
0x112987EE57A00E85,
0xD023908D0CFAA998,
0x4825D4116EBC1EF4,
0x89530CC659671CC3,

    
0x39B852D59A9BE2E0,
0xF415036C81159293,
0x6BE6DC20D9FC804F,
0x69C870631681806E,

    
0x6AF9EEF1D316682C,
0xFEBB53F80FD370E5,
0xC97055EDB2A71632,
0xB421DAD7F181736F,

    
0x2CAB9677FF0584FF,
0x93FA1108B658D73F,
0x129171EEA1243728,
0xE0874BC496396705,

    
0x243734816D9CA9A7,
0xD97B6D79CD201F32,
0x61D1C75C00D7BF58,
0xD23437B2C56EA37E,

    
0xF0C6BBEDF13BB614,
0x5F8F165B6175E6A0,
0x6A9E1A07F5F54504,
0xB247BBB7561A05DA,

    
0xB069D4F9EA566187,
0x35BF519BF705AEB4,
0xB1BF24944D7DE6C6,
0xBF09874872A07E1D,

    
0x654C7E16BD76C555,
0x2636E0B3E47178DB,
0x307ED49D60CB9CB0,
0xE2B569C85893152A,

    
0xBF9CE4B8C9BB19A6,
0x0F6F332FF09B987D,
0x25CD7FE3B2851647,
0x6059F05B64C1A22A,

    
0xBCFFDD075079B0AB,
0x4624AE3969D6E0F4,
0xE3644BCEF37D49C0,
0x583D49AB5BAD415B,

    
0xF52DC633948DDBC9,
0x8985BEF75FFC0266,
0x260757606AF1604D,
0x00347228A7F7BF9E,

    
0x59F9F8F3F971E536,
0xF338B4078F486491,
0x18C32580B34A8726,
0x113B0961F7953B1D,

    
0x9EB4A1CCF25A5CD8,
0x3DFF855AA1039E30,
0x110C2865C459C45A,
0x12E22FDD4B4A1AEF,

    
0x665FDB5BDA1FCB1F,
0xE89B951F7C1111DA,
0x08C1CF3BA4568604,
0x44C9DB8809E62544,

    
0x9E59DC6C1A1F5F38,
0xD9B56541200DF8CB,
0xA23CA09E658AB9C3,
0x0767DCA14F2C72CB,

    
0x51B61C35FA45010A,
0xB0FB280C2DD0366A,
0x9ED98C571179A8E7,
0xC7F39FE23E91335A,

    
0x604753F41CD8D115,
0x21A2D7B5D78D802D,
0x4AE6FDD67F4B0A6E,
0xAF4B159AEDC99931,

    
0x3610552D37F0E6DB,
0xE38E6CC440D8CBEF,
0x760231345D28F4F4,
0x28248CDBA0EDB31F,

    
0xDE399D92C5D53326,
0xE9135FB12EE30AEE,
0x5A9DF776DA69567C,
0x1B2A57AF9499BD26,

    
0xCDD1A6D279C29E2A,
0x450B0EA15E46A467,
0xB584768595BEE16F,
0xAC6CBFFB6A010996,

    
0xBC9FB5B01E5E1672,
0xBADF6D820EE0C999,
0x2EDE392A15AE7786,
0x5E3E43953CA3858D,

    
0x673DA6FCC578B174,
0xBB5988D76623867F,
0x0B63FD7CCAE209CD,
0x8D995000B6CAB0D9,

    
0x6F4FB9C0F867F695,
0xE94BDDC7EA2C03C2,
0xD44B8AD0FDF57741,
0x1B10BDA8D65E95B6,

    
0xCCE5B87F56D24262,
0x8DAC843E7DB7A2E6,
0x0ABA4CE735F3C1B2,
0x977D2BFD34E0F569,

    
0x0C8C9074173132E8,
0x6BDF5D06F84C38B6,
0x8938CC203E90D87C,
0x1817710430C214C6,

    
0x1DDA5BEF471D0818,
0x46BC18EA73F2FC35,
0xF7E5DE669CF074F7,
0x9FD67C166ACAE0D1,

    
0x77221342DD99DE6C,
0xBE40211AC965233C,
0xE722C8D94C228295,
0x6C2884E0343EA702,

    
0x922C97C8704D99C2,
0x075F7EF8DCE261AE,
0x5E1C79B5D149E038,
0x9A6195E08F06A06E,

    
0x7B6822030B9FA638,
0x73DC6804EE0D0950,
0x02B60CF3E5CF9C7E,
0xAE921AFB68BCBEA0,

    
0xAD446E5EB2746D4A,
0x1DC7B24A9EE8ABC6,
0x4323571D25EE32AC,
0xA45138A5015CE595,

    
0x8B66A2094809CFD5,
0xC32AFD0826677ADE,
0x5575595D25BD5C84,
0x5C81A62E617BE26B,

    
0x059A88DCF9D6E135,
0x7058BE4874076200,
0x6267202D26639147,
0xE138B206B106F3C2,

    
0x610BAC8FD4C0C7D2,
0x2FF10048928495E5,
0xFAADF0AEC329C653,
0x1967879046E2CCC4,

    
0xC58CA6773E7411DE,
0x59FD5C8362D5BFE3,
0x2181E3CDFCED020E,
0xF921E3A83C96C483,

    
0x56A7094705F9D968,
0x5B7856C1CD5A54C4,
0xB4CBBA647E781A8D,
0xA67656D1F94C5A51,

    
0x35E3C3ED20316470,
0xB34521490B1040AA,
0x743590C9AD7D24E7,
0xD4337B729544D6A1,

    
0x7298208D0E80D2E8,
0xC5B8CD70B2D03211,
0x86D8347BDDBA957F,
0xC090603D429D62A7,

    
0x0235ABA3C6901CB4,
0x0528A92887BDF615,
0x2E44CC0369590E85,
0xAD02B1D05421BDE8,

    
0x68D417EB0D3F9032,
0xF9A7D5E6634187E8,
0x43169AEC90D5025B,
0x4C2B9DBED875F144,

    
0xE5DE45E48A570B3B,
0xD9C0D8951BAE9D96,
0x1B1ACE5F64DE77CA,
0x9D761F5389E6C998,

    
0x4EB831FD2BBB77E6,
0xA4B136D42251FB74,
0xF2830331DDFE4547,
0x2A6447E1DEBFA061,

    
0xC9841806A598426E,
0xBF16EA745AE7E9BC,
0xB36C28F201F79F4A,
0xA98579C7D6AEC72B,

    
0x893922174E8B8677,
0x913AE9D467501D9E,
0x3E2D63025ACD7F03,
0x5BE849ABD5BA1458,

    
0x449FBFDC7E263EF8,
0x3407C08D952B7968,
0x776D9D1E34112AB0,
0x15445825ABB665AA,

    
0xD30D8C219808786D,
0xE6675A7717B60CDD,
0x9B3FF2D65785B39F,
0x6FA1CF2B3F17A6F5,

    
0xF395EDD33DBE0610,
0xFC653F59F4E1B87A,
0x2DACA68BB81F7DA6,
0x206C77148946236D,

    
0xC81A1EFB3751A538,
0x6409F2AEDC0EED11,
0x3189DAAD5737F77D,
0x3D3BBD38CB86E7CF,

    
0x725AE7DB17E853B0,
0x2800486CD1171716,
0xD735E9D2B8B640AA,
0xDDF5519F2483A6F8,

    
0x3131B875F05D3528,
0x8DCE9D5B6484B894,
0xB093C2D54E4AFA63,
0x65E2372A8E53B46F,

    
0xAA8F0682007BE35D,
0xD69A9CA93D25ED2A,
0x6CD691A50B3162D6,
0x809E4825E754BB66,

    
0x220319E38497A08D,
0x63B12F27E7025E2E,
0x2AE5C7C31B391CA2,
0x21BAE14A36021B8F,

    
0x5AC1DCEA550C0DCF,
0xA5444C19847C54A4,
0x94E6824A5EEFE6C4,
0xE4333A50D152CD0C,

    
0x797164FAA2239023,
0x264B8D9CD54E7E1F,
0x444C3B9CBA2D8356,
0x06ABEEBAC74A0787,

    
0x569C22DE3BE50980,
0x279B489C4949DA5E,
0x77089BB807B5A0B1,
0x13DC56583559394A,

    
0x7539F6C9A2EC1BA0,
0x109E930DFDA4185A,
0x6700F1724CB02B85,
0xD7C5D07325AF1CAD,

    
0x718724E8128738E9,
0xE1B0D23478A7F891,
0xFF46BE608736FB9A,
0xF9F73D748FA40B7E,

    
0x3B2BE3A79DE348D6,
0xEE1283643874FD42,
0x649BA6A4CDD401F4,
0x2F089F15CEF67AFE,

    
0xCF0CA18CA921F123,
0x76C29224A2384570,
0x2BD353109934B2C0,
0xC94421A2E98F3D10,

    
0xE72A8D68171459B7,
0x36892055321DB339,
0x4EDF5E5721D217DC,
0x6452B546F814D01F,

    
0x86DF9438E8A87602,
0x1935C4F814BB279E,
0x85B5B29AC838281D,
0x4C9C5381293D8E55,

    
0xBDCDCB5A88C414DC,
0x5166F43F110CFAB1,
0xCDE80C0B72AE5A51,
0x0BAEFC91871D774D,

    
0x7DB98011B74847B4,
0xF9B5407AF41DE099,
0x1B44BF731A45A54D,
0xBF694CB97EA7D45C,

    
0xD6D02B2A3E23FF69,
0x0E7EBF21682A9D48,
0xAAF053FD50E584CF,
0xCE11948D7145812C,

    
0x350201B0D29AE7D4,
0xB5EB76FD9D4FC92F,
0x68FDE647C12588FA,
0x80B6CECE2EC02382,

    
0x5A29210080C3E2AE,
0x0881C67CB95F0DF6,
0xAF7AA6C06A636E3E,
0xF3741C273BBB6AF9,

    
0x9402EB452D72EFD4,
0x6EC26F80CDA9E3BB,
0x1B2496F8336BE27A,
0x4EBB379532FBFA03,

    
0x411C5ECE692FD205,
0x554A7A5822BC1562,
0x6ACAE36472E01000,
0x9A306AFEB1E4E78A,

    
0x424385B0753C6BAD,
0xA6F6008CCF71AC07,
0xB327763BB08E1398,
0x1C795E1A9B94E73F,

    
0xA0E3073C0D163B41,
0xF2A8B4CAEECE1AD9,
0x7E2A46B32477DC99,
0xD38E6576267F3DE9,

    
0x035815E08F8C26B4,
0x8EC6808F275355E8,
0x0E466AB79AC2E59C,
0x03CE6C6D9E179F54,

    
0xE82ECACFAA40DF7E,
0x8B7DB54AEE03F6F3,
0x73F0E57EBE66CE13,
0x467CE159A4987475,

    
0xCFA9EEC39378A73E,
0xC8EAB1765E913DEB,
0x2EE85FAAC5B4D814,
0xA3E54D4809FB2E79,

    
0xE79DF073FF6B0218,
0xFDB8E65BE078ACBA,
0xC7B0A06AC0E39D5D,
0xD1A1A2EED123200C,

    
0xD386CEF30A03B363,
0x7512341C6B99172D,
0x675259128A507865,
0x553D59C6FCC91A78,

    
0x49506CB9761FAEA3,
0x47CF736453521A0A,
0x41EAD980596DFD94,
0xD95F5137BCEBDB25,

    
0xC838D324296E6B02,
0x56B8896E64F1E19A,
0x58767B596305AE34,
0x63A43905FE1C4208,

    
0x8EE620E14EF5E0ED,
0x1F02A0FE0254F334,
0x9E4BC218936BDC57,
0x197259EA1A4D7626,

    
0x56EB409FDAFAA5B2,
0xE9FBB85A20D6BA1C,
0x6284E86E7879F6D7,
0xF7CEA3965587A590,

    
0x416FC66A88C2323F,
0x32AFABF7657D18EC,
0x18930FE6E3034561,
0x3045664559EB540B,

    
0x6BAA893C26F28744,
0x495BA7ADEE4DE1BD,
0x81768D08828907FB,
0xED907FAD722CC71E,

    
0xB1DE2CF2E3AC5A23,
0x9CE01455BA130278,
0xDB41EFCA7E450F50,
0x021B148E042B4FBF,

    
0xC742B013502F5BC8,
0x3B99457C5BDC2BD1,
0x80E371379653AE63,
0x003EA2BD031C32BC,

    
0x0EC4EFE4A67052C0,
0xF2F9C749E8B86A84,
0x83964219C0439938,
0x3300F8457488FA7C,

    
0x3881A249E51BF9EB,
0x28505E371FE46766,
0x09A9C430269D6089,
0xC5C7331508662B37,

    
0xE9FF1E14A40DE6FE,
0xE92A64373CD15AA7,
0x825BEC8918599C0A,
0x50D7AE5D836D00E1,

    
0x357D2E9DE4508CB8,
0x69E62254CCE064CD,
0x8479AC1F4984A65C,
0x5D07E7F66BBC2CFC,

    
0xAEC99B4396F373E5,
0x0DEB36E5208612DB,
0x6FA16B6F4D6D5327,
0xDDD14F38C208F153,

    
0x2850ED56A3F3CAAF,
0xDE683A6D5B439087,
0x6719D463641A0286,
0x2BC3FA675229F17B,

    
0x7CF99A7FA60FE7B5,
0xCE83E8C3B5452252,
0xE4F6754504851FCF,
0xFCBD4D48126E31F9,

    
0xF9A6313AF0B2C03F,
0xC651FA868EC26476,
0xBA8995A48D3725E1,
0xCE839FED0F4266DF,

    
0x930744CABCE7FF66,
0xB5885C2BF3509EEE,
0x5A8D4EE67BE62266,
0xEDA276883262BB94,

    
0x1D4FD941B04601E7,
0x9FE9EC4F4A131497,
0x9F848CCEE1F80DBF,
0x6E279A5473E06AB1,

    
0x6E88D9ED9658660F,
0x2B8791AECCA8D0E4,
0xE672328AA9ED7C83,
0x6361413214B5AAD8,

    
0xD58E6FF6B86A584B,
0x4FCED369A7C3FEF4,
0x5548612F5FA13FD2,
0xFA6424995A34F4B7,

    
0x441BAB6F7B395805,
0xE0528B385B8D73FD,
0xC5300F79F0FC07E8,
0xAA825834D1E45903,

    
0x3B9641D6F60EF961,
0x52CC7BD14060E61D,
0x830B28E092F143CF,
0x8EDA30CE5077DE27,

    
0xC674ABA94B80417D,
0x9DCE6B0D69790A78,
0x5B224EB078AA0997,
0xAEDDF6FE5BC0D387,

    
0x07BBF4D18336C879,
0x09927659357EFCA2,
0x3BB9F2BD99539534,
0x2AFFF4179B7A0B69,

    
0xD634959529A582A2,
0xE513C3224510C84A,
0x668857460A95E64C,
0x8B5B8F582B5CEA6F,

    
0x4AA7A5BF91CC2050,
0x361F8298822B7357,
0x5E974F800AA08F28,
0x44833EE5A79C6FDA,

    
0xC201005A6EC1CF88,
0xD6ED94186F338734,
0x18063447FA294CB7,
0xD9BA7C25DC9C819F,

    
0x0E4DDC1138BEFDB0,
0xB8EF64B180C99966,
0x5BF5D5C501B9CE37,
0x963310BC26D99539,

    
0x733CBDD7A3BBB4EA,
0x167E816C2A9D909F,
0xF987189D44E7CAEB,
0xD269483BB58E08D0,

    
0x8C729CB915915345,
0xDDA1462C3585913B,
]
