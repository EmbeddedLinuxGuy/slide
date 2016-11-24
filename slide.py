#!/usr/bin/env python2

from chesstools import Board, Move, List
from chesstools.piece import PIECE_TO_LETTER
import sys
import copy
from renderer import Renderer

class Slide(object):
    def __init__(self):
        self.moves = List()
        self.board = Board(variant="standard")
        self.lineup = "".join([PIECE_TO_LETTER[piece]["white"] for piece in self.board.LINEUP])
        self.white = []
        self.black = []
        self.output = ""
        self.total_moves = []
        self.renderer = Renderer()

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
#            print self.white[index]
            if self.white[index][2] == "" or self.white[index][2] == "+":
                self.white[index][2] = None
            if not self.move(self.white[index][0], self.white[index][1], self.white[index][2]):
                #print ("white error at " + str(index))
                print "error: " + index + " " + self.white[index]
                raise
        else:
#            print self.black[index]
            if self.black[index][2] == "" or self.black[index][2] == "+":
                self.black[index][2] = None
            if not self.move(self.black[index][0], self.black[index][1]):
                #print "error " + index + " " + self.black[index]
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
        
        save_board = copy.deepcopy(self.board)
        save_moves = copy.deepcopy(self.moves)

        try:
            white_output = ""
            these_moves = []
            for m in range(this_move, last_move):
                #print "white"
                self.do_move("white", m)
#                self.turn.color = "white" # for get_fen() always assume white move
                white_output += self.get_fen() + "\n"
                these_moves.append(self.get_fen())
            for m in range(this_move, last_move):
                #print "black"
                self.do_move("black", m)
                white_output += self.get_fen() + "\n"
                these_moves.append(self.get_fen())
            self.output += white_output
            self.total_moves.append(these_moves)
            return last_move - this_move
        except:
            #print "Could not move to " + str(last_move)
            self.board = save_board
            self.moves = save_moves
            #self.render()
            if last_move > this_move + 1:
                return self.cluster_moves(this_move, last_move-1)
            else:
                return 0

    def make_animation(self):
        i = 0
        for fen_list in self.total_moves:
            for fen in fen_list:
                surface = self.renderer.render(fen)
                surface.write_to_png('img/{num:05d}.png'.format(num=i))
                i += 1

if __name__ == "__main__":
    slide = Slide()
    slide.read_pgn("null")
    print str(len(slide.white)) + " white moves"
    print str(len(slide.black)) + " black moves"
    
    last_move = len(slide.black)-1
    this_move = 0

    while this_move <= last_move:
        moves = slide.cluster_moves(this_move, last_move)
        this_move += moves
        print "MOVED: " + str(moves) + " times"
        if moves < 1:
            print "Done."
            slide.make_animation()
            print slide.total_moves
            sys.exit(1)

