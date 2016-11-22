from chesstools import Board, Move, List
from chesstools.piece import PIECE_TO_LETTER

class Slide(object):
    def __init__(self):
        self.moves = List()
        self.board = Board(variant="standard")
        self.lineup = "".join([PIECE_TO_LETTER[piece]["white"] for piece in self.board.LINEUP])

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
            if not self.move(self.white[index][0], self.white[index][1]):
                raise
        else:
            if not self.move(self.black[index][0], self.black[index][1]):
                raise
            
    def cluster_moves(self, this_move, last_move):
        # try playing to the last move
        # if success, return number of moves played
        # if it fails, try playing one move fewer
        
        save_board = self.board
        save_moves = self.moves

        try:
            for m in range(this_move, last_move):
                self.do_move("white", m)
            output = "\n" + self.get_fen() + "\n" + self.get_board()
            for m in range(this_move, last_move):
                self.do_move("black", m)
            self.output += output + "\n" + self.get_fen() + "\n" + self.get_board()
            return 1 + last_move - this_move
        except:
            self.board = save_board
            self.moves = save_moves
            return self.cluster_moves(this_move, last_move-1)

if __name__ == "__main__":
    slide = Slide()
    Slide.white = [ [ "e2", "e4" ], [ "a2", "a4" ], [ "e4", "e5" ], [ "b2", "b4" ], [ "c2", "c4" ], [ "f2", "f4" ] ]
    Slide.black = [ [ "d7", "d5" ], [ "a7", "a5" ], [ "e7", "e6" ], [ "b7", "b5" ], [ "c7", "c5" ], [ "f7", "f5" ] ]
    Slide.output = ""
    
    last_move = len(Slide.white)-1
    this_move = 0

    while this_move <= last_move:
        moves = slide.cluster_moves(this_move, last_move)
        this_move += moves
        if moves < 1:
            print "ERROR! Illegal moves!"
    print slide.output
