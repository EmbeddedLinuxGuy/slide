#!/usr/bin/env python2

from chesstools import Board, Move, List
from chesstools.piece import PIECE_TO_LETTER
import sys

class Slide(object):
    def __init__(self):
        self.moves = List()
        self.board = Board(variant="standard")
        self.lineup = "".join([PIECE_TO_LETTER[piece]["white"] for piece in self.board.LINEUP])
        self.white = []
        self.black = []
        self.output = ""

    def move(self, start, end, promotion=None):
        m = Move(start, end, promotion)
        if self.board.is_legal(m):
            self.moves.add(m)
            self.board.move(m)
            return True
        else:
            return False

    def check(self):
        return self.board.check_position()

    def turn(self):
        return self.board.turn

    def get_fen(self):
        return self.board.fen()

    def get_board(self):
        return self.board.render()

    def get_moves(self):
        return str(self.moves)

    def render(self):
        print self.get_fen() + '\n' + self.get_board() + '\n' + self.get_moves()

    def do_move(self, color, index):
        self.board.turn = color
        if color == "white":
            print self.white[index]
            if self.white[index][2] == "" or self.white[index][2] == "+":
                self.white[index][2] = None
            if not self.move(self.white[index][0], self.white[index][1], self.white[index][2]):
                print self.white[index]
                raise
        else:
            print self.black[index]
            if self.black[index][2] == "" or self.black[index][2] == "+":
                self.black[index][2] = None
            if not self.move(self.black[index][0], self.black[index][1]):
                print self.black[index]
                raise

    def read_pgn(self, filename):
#        with open(filename, "r") as f:
        with sys.stdin as f:
            line = ""
            while line != "1.":
                line = f.readline().strip()

            while line != "" and line.find("-") < 0:
                #print "[" + line + "]"
                # white move
                line = f.readline().strip()
                #print "WHITE: " + line
                self.white.append([line[0:2],line[2:4],line[4:5]])
                # black move, or outcome
                line = f.readline().strip()
                if line.find("-") > 0:
                    return
                #print "BLACK: " + line
                self.black.append([line[0:2],line[2:4],line[4:5]])
                # next move number, blank line, or outcome
                line = f.readline().strip()

    def cluster_moves(self, this_move, last_move):
        # try playing to the last move
        # if success, return number of moves played
        # if it fails, try playing one move fewer
        
        save_board = self.board
        save_moves = self.moves

        try:
            for m in range(this_move, last_move):
                print "white"
                self.do_move("white", m)
            white_output = "\n" + self.get_fen() + "\n" + self.get_board()
            for m in range(this_move, last_move):
                print "black"
                self.do_move("black", m)
            self.output += white_output + "\n" + self.get_fen() + "\n" + self.get_board()
            return last_move - this_move
        except:
            print "CRAAAP"
            self.board = save_board
            self.moves = save_moves
            if last_move > this_move + 1:
                return self.cluster_moves(this_move, last_move-1)
            else:
                return 0

if __name__ == "__main__":
    slide = Slide()
    slide.read_pgn("null")
    print len(slide.white)
    print len(slide.black)
    
    last_move = len(slide.black)-1
    this_move = 0

    while this_move <= last_move:
        moves = slide.cluster_moves(this_move, this_move+1)
        this_move += moves
        print "MOVED: " + str(moves) + " times"
        if moves < 1:
            print "ERROR! Illegal moves!"
    print slide.output
