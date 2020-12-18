# code written by jake schlaerth
# 12/18/2020


class Chess:
    """instance of a game of chess"""

    def __init__(self, moves_made=[]):
        """init board, game state, starting position"""
        self.moves_made = moves_made
        self.game_state = "UNFINISHED"
        self.turn = "white"
        self.board = list("-" * 64)


class Piece:
    """ basic utilities of each piece"""

    def __init__(self, pos, color):
        """initiates a piece"""
        self.pos = pos
        self.color = color
        self.move_set = set()

    def __repr__(self):
        """
        prints the type of piece and its coordinates
        :return: "call sign, str coord"
        """
        return self.callsign + "  " + computer_to_human_format(self.pos) + "  " + self.color


N, E, S, W = -8, 1, 8, -1
directions = {
    'P': (N, N+N, N+W, N+E),
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}
class King(Piece):
    """may move any direction by 1 space"""
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.is_in_check = False
        self.call_sign = "K"
        self.has_moved = False

    def king_move_logic(self, board):
        pass


def human_to_computer_format(pos):
    """convert a1 to 56, h8 to 7"""
    letter = ord(pos[0])-97
    number = int(pos[1])
    number = abs(8-number)
    coord = (8 * number) + letter
    return coord

def computer_to_human_format(pos):
    """convert 0 to a8, 63 to h1"""
    letter = chr((pos % 8) + 97)
    number = abs(8 - (pos // 8))
    print(letter, number)


if __name__ == '__main__':
    chess = Chess()
