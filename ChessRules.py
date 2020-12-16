# Author: Jacob Schlaerth
# Date: 03/14/2020
# Description: a game of chess


class ChessGame:
    """
    an instance of a game of chess
    """

    def __init__(self, moves_made=[]):
        """
        init board, game state, all pieces
        """
        self.moves_made = moves_made  # this data member holds the list of moves made by both user and computer
        self._game_state = "UNFINISHED"
        self._turn = "white"
        self._board = [
            ["-", "-", "-", "-", "-", "-", "-", "-"],  # 1
            ["-", "-", "-", "-", "-", "-", "-", "-"],  # 2
            ["-", "-", "-", "-", "-", "-", "-", "-"],  # 3
            ["-", "-", "-", "-", "-", "-", "-", "-"],  # 4
            ["-", "-", "-", "-", "-", "-", "-", "-"],  # 5
            ["-", "-", "-", "-", "-", "-", "-", "-"],  # 6
            ["-", "-", "-", "-", "-", "-", "-", "-"],  # 7
            ["-", "-", "-", "-", "-", "-", "-", "-"]  # 8
            # a    b    c    d    e    f    g    h  
        ]
        white_pawn_a = Pawn(6, 0, "white")
        white_pawn_b = Pawn(6, 1, "white")
        white_pawn_c = Pawn(6, 2, "white")
        white_pawn_d = Pawn(6, 3, "white")
        white_pawn_e = Pawn(6, 4, "white")
        white_pawn_f = Pawn(6, 5, "white")
        white_pawn_g = Pawn(6, 6, "white")
        white_pawn_h = Pawn(6, 7, "white")
        white_rook1 = Rook(7, 0, "white")
        white_rook2 = Rook(7, 7, "white")
        white_knight1 = Knight(7, 1, "white")
        white_knight2 = Knight(7, 6, "white")
        white_bishop1 = Bishop(7, 2, "white")
        white_bishop2 = Bishop(7, 5, "white")
        white_queen = Queen(7, 3, "white")
        white_king = King(7, 4, "white")

        black_pawn_a = Pawn(1, 0, "black")
        black_pawn_b = Pawn(1, 1, "black")
        black_pawn_c = Pawn(1, 2, "black")
        black_pawn_d = Pawn(1, 3, "black")
        black_pawn_e = Pawn(1, 4, "black")
        black_pawn_f = Pawn(1, 5, "black")
        black_pawn_g = Pawn(1, 6, "black")
        black_pawn_h = Pawn(1, 7, "black")
        black_rook1 = Rook(0, 0, "black")
        black_rook2 = Rook(0, 7, "black")
        black_knight1 = Knight(0, 1, "black")
        black_knight2 = Knight(0, 6, "black")
        black_bishop1 = Bishop(0, 2, "black")
        black_bishop2 = Bishop(0, 5, "black")
        black_queen = Queen(0, 3, "black")
        black_king = King(0, 4, "black")
        self._piece_list = [white_pawn_a, white_pawn_b, white_pawn_c, white_pawn_d,
                            white_pawn_e, white_pawn_f, white_pawn_g, white_pawn_h,
                            white_rook1, white_rook2,
                            white_knight1, white_knight2,
                            white_bishop1, white_bishop2,
                            white_queen, white_king,
                            black_pawn_a, black_pawn_b, black_pawn_c, black_pawn_d,
                            black_pawn_e, black_pawn_f, black_pawn_g, black_pawn_h,
                            black_rook1, black_rook2,
                            black_knight1, black_knight2,
                            black_bishop1, black_bishop2,
                            black_queen, black_king]
        self._captured_list = []
        self.update_board()
        self.update_move_sets()

        for move in self.moves_made:
            self.make_move(move[0], move[1])

    def get_board(self):
        """
        returns self._board
        :return: self._board
        """
        return self._board

    def get_piece_list(self):
        """
        returns self._piece_list
        :return: self._piece_list
        """
        return self._piece_list

    def set_piece_list(self, new_list):
        """
        directly set the piece_list data member
        :param new_list: new list
        :return: None
        """
        self._piece_list = new_list.copy()

    def get_captured_list(self):
        """
        returns the list of captured pieces
        :return: self._captured_list
        """
        return self._captured_list.copy()

    def set_captured_list(self, new_list):
        """
        directly set the captured_piece_list data member
        :param new_list: new list
        :return: None
        """
        self._captured_list = new_list

    def get_turn(self):
        """
        returns the turn data member
        :return: self._turn
        """
        return self._turn

    def get_game_state(self):
        """
        returns the game state data member
        :return: string,  self._game_state
        """
        return self._game_state

    def set_old_board_coord(self, from_rank, from_file):
        """
        takes a board coordinate from make_move and sets the old coordinate to "-"
        :param from_rank: old rank
        :param from_file: old file
        :return: None
        """
        self._board[from_rank][from_file] = "-"

    def set_turn(self, color):
        """
        sets turn to opposite of the piece that just moved
        :param color:
        :return:
        """
        self._turn = color

    def set_game_state(self, game_state):
        """
        updates the game state
        :param game_state: "UNFINISHED", "WHITE_WON", or "BLACK_WON"
        :return: none
        """
        self._game_state = game_state

    def update_game_state(self):
        """
        checks if the current turn has any possible moves
        :return:
        """
        color = self.get_turn()
        all_moves = set()
        for piece in self.get_piece_list():
            if piece.get_color() == color:
                all_moves = all_moves.union(piece.get_move_set())
        if not all_moves:
            # no possible moves, stalemate or checkmate
            if not self.is_in_check(color):
                self.set_game_state("DRAW")
            if color == "white":
                self.set_game_state("BLACK_WON")
            if color == "black":
                self.set_game_state("WHITE_WON")
        if all_moves:
            self.set_game_state("UNFINISHED")

    def update_board(self):
        """
        updates the game board according to piece_list
        :return: None
        """
        # iterate through each remaining piece and place it on the board
        for piece in self.get_piece_list():
            self.get_board()[piece.get_rank()][piece.get_file()] = piece

    def update_move_sets(self):
        """updates every piece's move set"""
        for piece in self.get_piece_list():
            piece.set_move_set(self.get_board())

    def remove_illegal(self):
        """
        remove all moves that cause that color's king to be in check
        """
        # save piece lists to revert back after testing all psuedolegal moves
        reverted_piece_list = self.get_piece_list().copy()
        reverted_cap_list = self.get_captured_list().copy()
        reverted_master_move_set_dict = dict()
        for piece in self.get_piece_list():
            reverted_master_move_set_dict.update({piece: piece.get_move_set().copy()})
        for piece in self.get_piece_list():
            if piece.get_color() == self.get_turn():
                illegal_moves = set()
                color = piece.get_color()
                from_rank = piece.get_rank()
                from_file = piece.get_file()
                current_position = format_to_let(piece.get_rank(), piece.get_file())
                for potential_move in piece.get_move_set():
                    self.test_move(current_position, potential_move)
                    self.update_move_sets()  # this needs to be reverted for each piece
                    if self.is_in_check(color):
                        # this move is illegal
                        illegal_moves.add(potential_move)
                    # now we must revert the potential move, including all pieces positions and the lists of pieces
                    self.test_move(potential_move, current_position)
                    self.set_piece_list(reverted_piece_list)
                    self.set_captured_list(reverted_cap_list)
                    self.update_move_sets()
                    self.update_board()
                    reverted_master_move_set_dict[piece].difference_update(illegal_moves)
        for piece in reverted_master_move_set_dict:
            piece.direct_set_move_set(reverted_master_move_set_dict[piece])

    def is_in_check(self, color):
        """
        returns True if the given color is in check, False if not
        :param color: color of king to be checked for check
        :return: Bool
        """
        for piece in self.get_piece_list():
            if piece.get_callsign() == "K" and piece.get_color() == color:
                king = piece
                break
        king_pos = format_to_let(king.get_rank(), king.get_file())
        for piece in self.get_piece_list():
            for move in piece.get_move_set():
                if king_pos == move:
                    return True
        return False

    def is_castle_legal(self, coord):
        """ checks is castling is possible (illegal to castle into or through check"""
        # white
        if self.get_turn() == "white":
            if self.is_in_check("white"):
                return False

            # king side castle
            if coord == "g1":
                for piece in self.get_piece_list():
                    if piece.get_color() == "black":
                        if "f1" in piece.get_move_set():
                            return False
                        if "g1" in piece.get_move_set():
                            return False
                return True
            # queen side castle
            if coord == "c1":
                for piece in self.get_piece_list():
                    if piece.get_color() == "black":
                        if "b1" in piece.get_move_set():
                            return False
                        if "c1" in piece.get_move_set():
                            return False
                        if "d1" in piece.get_move_set():
                            return False
                return True

        # black
        if self.get_turn() == "black":
            # king side
            if coord == "g8":
                for piece in self.get_piece_list():
                    if piece.get_color() == "white":
                        if "g8" in piece.get_move_set():
                            return False
                        if "f8" in piece.get_move_set():
                            return False
                return True
            # queen side
            if coord == "c8":
                for piece in self.get_piece_list():
                    if "d8" in piece.get_move_set():
                        return False
                    if "c8" in piece.get_move_set():
                        return False
                    if "f8" in piece.get_move_set():
                        return False
                return True

    def test_move(self, from_str, to_str):
        """
        a method that directly moves any piece to any position, regardless of turn or rules
        not to be used by a player
        note: this method does not update the move sets of any pieces on the board
        :param from_str: piece to move's position
        :param to_str: destination
        :return: Boolean
        """
        from_coord = format_to_nums(from_str)
        from_rank = from_coord[0]
        from_file = from_coord[1]

        # format input to_str
        to_coord = format_to_nums(to_str)
        to_rank = to_coord[0]
        to_file = to_coord[1]

        # get piece at from_coord
        piece_to_move = self.get_board()[from_rank][from_file]
        space_to_move_to = self.get_board()[to_rank][to_file]

        # is there a piece at from_coord?
        if piece_to_move == "-":
            return False

        # is this a capture?
        if space_to_move_to != "-":
            # capture
            self.get_piece_list().remove(space_to_move_to)
            self.get_captured_list().append(space_to_move_to)

        # do it
        piece_to_move.set_rank(to_rank)
        piece_to_move.set_file(to_file)
        self.set_old_board_coord(from_rank, from_file)
        self.update_board()
        # self.update_move_sets()

        return True

    def make_move(self, from_str, to_str):
        """
        moves a piece to a new spot on the board
        :param from_str: position to be moved from
        :param to_str: position to be moved to
        :return: Bool
        """

        # format input from_str
        from_coord = format_to_nums(from_str)
        from_rank = from_coord[0]
        from_file = from_coord[1]

        # format input to_str
        to_coord = format_to_nums(to_str)
        to_rank = to_coord[0]
        to_file = to_coord[1]

        # get piece at from_coord
        piece_to_move = self.get_board()[from_rank][from_file]
        space_to_move_to = self.get_board()[to_rank][to_file]

        # is there a piece at from_coord?
        if piece_to_move == "-":
            return False

        # is it this piece's turn?
        if piece_to_move.get_color() != self.get_turn():
            return False

        # is this a possible move for this piece?
        if to_str not in piece_to_move.get_move_set():
            return False

        # is this a capture?
        if space_to_move_to != "-":
            # capture
            self.get_piece_list().remove(space_to_move_to)
            self.get_captured_list().append(space_to_move_to)

        # castling check
        # white
        if piece_to_move.get_callsign() == "K" and piece_to_move.get_color() == "white":
            if to_str == "g1" and "g1" in piece_to_move.get_move_set():
                if self.is_castle_legal("g1"):
                    # move h1 rook if castling
                    self.test_move("h1", "f1")
                else:
                    return False
            if to_str == "c1" and "c1" in piece_to_move.get_move_set():
                if self.is_castle_legal("c1"):
                    # move a1 rook if castling'
                    self.test_move("a1", "d1")
                else:
                    return False
        # black
        if piece_to_move.get_callsign() == "K" and piece_to_move.get_color() == "black":
            if to_str == "g8" and "g8" in piece_to_move.get_move_set():
                if self.is_castle_legal("g8"):
                    # move h8 rook if castling
                    self.test_move("h8", "f8")
                else:
                    return False
            if to_str == "c8" and "c8" in piece_to_move.get_move_set():
                if self.is_castle_legal("c8"):
                    # move a8 rook if castling
                    self.test_move("a8", "d8")
                else:
                    return False

        # then do it
        piece_to_move.set_rank(to_rank)
        piece_to_move.set_file(to_file)

        # if the moved piece is a pawn, check for promotion
        if piece_to_move.get_callsign() == "P":
            piece_to_move.promotion(self.get_piece_list())

        self.set_old_board_coord(from_rank, from_file)

        self.update_board()
        self.update_move_sets()

        # is this piece a king or a rook
        if piece_to_move.get_callsign() == "K" or piece_to_move.get_callsign() == "R":
            piece_to_move.set_has_moved(True)

        # switch turn
        if piece_to_move.get_color() == "white":
            self.set_turn("black")
        if piece_to_move.get_color() == "black":
            self.set_turn("white")

        # remove psuedolegal moves that leave king in check
        self.remove_illegal()
        # update game state
        self.update_game_state()

        self.moves_made.append((from_str, to_str))

        return True

    def print_board(self):
        """
        prints board to console, debugging purposes only
        :return: None
        """
        for rank in range(0, 8):
            for file in range(0, 8):
                if self.get_board()[rank][file] != "-":
                    print(self.get_board()[rank][file].get_callsign(), end="  ")
                if self.get_board()[rank][file] == "-":
                    print(self.get_board()[rank][file], end="  ")
            print(8 - rank, end="")
            print()
        print("a  b  c  d  e  f  g  h")


class Piece:
    """
    basics of each piece
    will be inherited by all pieces
    """

    def __init__(self, rank, file, color):
        """
        initiates a piece
        """
        self._rank = rank
        self._file = file
        self._color = color
        self._move_set = set()

    def __repr__(self):
        """
        prints the type of piece and its coordinates
        :return: "call sign, str coord"
        """
        return self.get_callsign() + "  " + format_to_let(self.get_rank(), self.get_file()) + "  " + self.get_color()

    def get_rank(self):
        """
        return rank
        :return: rank
        """
        return self._rank

    def get_file(self):
        """
        return file
        :return: file
        """
        return self._file

    def get_color(self):
        """
        return color
        :return: color
        """
        return self._color

    def get_callsign(self):
        """
        return piece._callsign
        :return: piece._callsign
        """
        return self._callsign

    def get_move_set(self):
        """
        returns set of possible spaces to move to
        :return: _possible_moves
        """
        return self._move_set

    def set_rank(self, rank):
        """
        sets the rank of a piece, used in make_move
        :param rank: new rank
        :return: None
        """
        self._rank = rank

    def set_file(self, file):
        """
        sets the file of a piece, used in make_move
        :param file: new file
        :return: None
        """
        self._file = file

    def direct_set_move_set(self, new_set):
        """
        takes a set and sets self._move_set to that new set
        :param new_set: a set of tuples
        :return: None
        """
        self._move_set = new_set


# class king (K)
class King(Piece):
    """
    may move any direction 1 space
    can be in check
    """

    def __init__(self, rank, file, color):
        """
        initiates instance of king
        :param rank: horizontal rank
        :param file: vertical column
        """
        super().__init__(rank, file, color)
        self._in_check = False
        self._callsign = "K"
        self._has_moved = False
        self._strength = 900

    def get_has_moved(self):
        """
        return _has_moved data member
        :return: has_moved bool
        """
        return self._has_moved

    def set_has_moved(self, has_moved):
        """
        set _has_moved data member
        :param has_moved: bool
        :return: None
        """
        self._has_moved = has_moved

    def king_logic(self, rank_delta, file_delta, board):
        """
        adds specific moves to king's move set
        :param rank_delta: change in rank
        :param file_delta: change in file
        :param board: game board
        :return: None
        """
        try:
            potential_space = board[self.get_rank() + rank_delta][self.get_file() + file_delta]
            move = (self.get_rank() + rank_delta, self.get_file() + file_delta)
            # empty space
            if potential_space == "-":
                # if potential space is empty, this is a possible move
                self.get_move_set().add(move)
                return

            # non-empty space
            if potential_space != "-":
                if potential_space.get_color() == self.get_color():
                    # if potential space is occupied by same color piece, this move is not possible
                    return
                if potential_space.get_color() != self.get_color():
                    # if potential_space is occupied by enemy piece, this move is possible
                    self.get_move_set().add(move)
                    return
        except IndexError:
            pass

    def castling_logic(self, board):
        """
        tests if the current board allows for castling, adds castling moves to king's move set
        :param board: game board
        :return: None
        """
        # castling
        # white
        if not self.get_has_moved():
            # king has not moved
            if self.get_color() == "white":
                # king has not moved, check if rook is in place
                h1 = board[7][7]
                # king side castling
                if h1 != "-":
                    # king side corner not empty
                    if h1.get_color() == "white":
                        # king side corner has a white piece
                        if h1.get_callsign() == "R":
                            # right corner is a rook
                            if not h1.get_has_moved():
                                # king side rook has not moved
                                g1 = board[7][6]
                                f1 = board[7][5]
                                if g1 == "-" and f1 == "-":
                                    # intermediate spaces are empty, castling is possible
                                    self.get_move_set().add(format_to_nums("g1"))
                # white queen side castling
                a1 = board[7][0]
                if a1 != "-":
                    # queen side corner not empty
                    if a1.get_color() == "white":
                        # queen side corner has a white piece
                        if a1.get_callsign() == "R":
                            # queen side corner is a rook
                            if not a1.get_has_moved():
                                # queen side rook has not moved
                                b1 = board[7][1]
                                c1 = board[7][2]
                                d1 = board[7][3]
                                if b1 == "-" and c1 == "-" and d1 == "-":
                                    # intermediate spaces are empty, long castling is possible
                                    self.get_move_set().add(format_to_nums("c1"))
        # black
        # king side
        if self.get_color() == "black":
            h8 = board[0][7]
            if h8 != "-":
                # king side corner not empty
                if h8.get_color() == "black":
                    # king side corner has black piece
                    if h8.get_callsign() == "R":
                        # h8 is black rook
                        if not h8.get_has_moved():
                            # rook has not moved
                            f8 = board[0][5]
                            g8 = board[0][6]
                            if f8 == "-" and g8 == "-":
                                # intermediate spaces are empty, castling is possible
                                self.get_move_set().add(format_to_nums("g8"))
            # black queen side castling
            a8 = board[0][0]
            if a8 != "-":
                # queen side corner not empty
                if a8.get_color() == "black":
                    # queen side corner has black piece
                    if a8.get_callsign() == "R":
                        # queen side corner has black rook
                        if not a8.get_has_moved():
                            # rook has not moved
                            b8 = board[0][1]
                            c8 = board[0][2]
                            d8 = board[0][3]
                            if b8 == "-" and c8 == "-" and d8 == "-":
                                # intermediate spaces are empty, castling is possible
                                self.get_move_set().add(format_to_nums("c8"))

    def set_move_set(self, board):
        """
        the king can move one space orthogonally in any direction
        :param board: game board
        :return: None
        """
        # empty move_set
        self.direct_set_move_set(set())
        # orthogonal
        # down
        self.king_logic(1, 0, board)
        # up
        self.king_logic(-1, 0, board)
        # right
        self.king_logic(0, 1, board)
        # left
        self.king_logic(0, -1, board)
        # diagonal
        # down right
        self.king_logic(1, 1, board)
        # up right
        self.king_logic(-1, 1, board)
        # up left
        self.king_logic(-1, -1, board)
        # down left
        self.king_logic(1, -1, board)

        self.castling_logic(board)

        # remove negative values
        self.direct_set_move_set({i for i in self.get_move_set() if i[0] >= 0 and i[1] >= 0})
        # convert to letter-number format
        self.direct_set_move_set({format_to_let(i[0], i[1]) for i in self.get_move_set()})


# class queen (Q)
class Queen(Piece):
    """
    initiates instance of queen
    """

    def __init__(self, rank, file, color):
        """
        init instance of Queen
        :param rank: horizontal rank
        :param file: vertical column
        """
        super().__init__(rank, file, color)
        self._callsign = "Q"
        self._strength = 90

    def queen_logic(self, rank_delta, file_delta, board):
        """
        adds specific moves to a queen's move set
        :param rank_delta: change in rank
        :param file_delta: change in file
        :param board: game board
        :return: boolean denoting whether the current direction can be continued
        """
        try:
            potential_space = board[self.get_rank() + rank_delta][self.get_file() + file_delta]
            move = (self.get_rank() + rank_delta, self.get_file() + file_delta)
            # empty space
            if potential_space == "-":
                # if potential space is empty, this is a possible move
                self.get_move_set().add(move)
                return True

            # non-empty space
            if potential_space != "-":
                if potential_space.get_color() == self.get_color():
                    # if potential space is occupied by same color piece, this move is not possible
                    return False
                if potential_space.get_color() != self.get_color():
                    # if potential_space is occupied by enemy piece, this move is possible
                    self.get_move_set().add(move)
                    return False

        except IndexError:
            pass

    def set_move_set(self, board):
        """
        queen can move any distance in any direction orthogonally or diagonally, no jumps
        :param board: game board
        :return: None
        """
        # empty move set
        self.direct_set_move_set(set())

        # diagonal
        # up and right
        for up_right in range(1, 8):
            if self.queen_logic(-up_right, up_right, board):
                continue
            else:
                break
        # up and left
        for up_left in range(1, 8):
            if self.queen_logic(-up_left, -up_left, board):
                continue
            else:
                break
        # down and left
        for down_left in range(1, 8):
            if self.queen_logic(down_left, -down_left, board):
                continue
            else:
                break
        # down and right
        for down_right in range(1, 8):
            if self.queen_logic(down_right, down_right, board):
                continue
            else:
                break

        # orthogonal
        for left in range(-1, -8, -1):
            if self.queen_logic(0, left, board):
                continue
            else:
                break
        for right in range(1, 8):
            if self.queen_logic(0, right, board):
                continue
            else:
                break
        for down in range(1, 8):
            if self.queen_logic(down, 0, board):
                continue
            else:
                break
        for up in range(-1, -8, -1):
            if self.queen_logic(up, 0, board):
                continue
            else:
                break

        # remove negative values
        self.direct_set_move_set({i for i in self.get_move_set() if i[0] >= 0 and i[1] >= 0})
        # convert to letter-number format
        self.direct_set_move_set({format_to_let(i[0], i[1]) for i in self.get_move_set()})


# class bishop (B)
class Bishop(Piece):
    """"""

    def __init__(self, rank, file, color):
        """
        init instance of Bishop
        :param rank: horizontal rank
        :param file: vertical column
        """
        super().__init__(rank, file, color)
        self._callsign = "B"
        self._strength = 30

    def bishop_logic(self, rank_delta, file_delta, board):
        """
        adds specific moves to a bishop's move set
        :param rank_delta: change in rank
        :param file_delta: change in file
        :param board: game board
        :return: None
        """
        try:
            potential_space = board[self.get_rank() + rank_delta][self.get_file() + file_delta]
            move = (self.get_rank() + rank_delta, self.get_file() + file_delta)
            # empty space
            if potential_space == "-":
                # if potential space is empty, this is a possible move
                self.get_move_set().add(move)
                return True

            # non-empty space
            if potential_space != "-":
                if potential_space.get_color() == self.get_color():
                    # if potential space is occupied by same color piece, this move is not possible
                    return False
                if potential_space.get_color() != self.get_color():
                    # if potential_space is occupied by enemy piece, this move is possible
                    self.get_move_set().add(move)
                    return False

        except IndexError:
            pass

    def set_move_set(self, board):
        """
        knight can move on space orthogonally followed by one space diagonally away from starting pos
        cannot move that direction if blocked orthogonally
        :param board: game board
        :return: None
        """
        # empty move set
        self.direct_set_move_set(set())

        # up and right
        for up_right in range(1, 8):
            if self.bishop_logic(-up_right, up_right, board):
                continue
            else:
                break
        # up and left
        for up_left in range(1, 8):
            if self.bishop_logic(-up_left, -up_left, board):
                continue
            else:
                break
        # down and left
        for down_left in range(1, 8):
            if self.bishop_logic(down_left, -down_left, board):
                continue
            else:
                break
        # down and right
        for down_right in range(1, 8):
            if self.bishop_logic(down_right, down_right, board):
                continue
            else:
                break

        # remove negative values
        self.direct_set_move_set({i for i in self.get_move_set() if i[0] >= 0 and i[1] >= 0})
        # convert to letter-number format
        self.direct_set_move_set({format_to_let(i[0], i[1]) for i in self.get_move_set()})


# class knight (N)
class Knight(Piece):
    """
    moves one point orthogonally and then one point diagonally away from its former position
    """

    def __init__(self, rank, file, color):
        """
        init instance of Knight
        :param rank: horizontal rank
        :param file: vertical column
        """
        super().__init__(rank, file, color)
        self._callsign = "N"
        self._strength = 30

    def knight_logic(self, rank_delta, file_delta, board):
        """
        adds specific moves to a knight's move set
        :param rank_delta: change in rank
        :param file_delta: change in file
        :param board: game board
        :return: None
        """
        try:
            potential_space = board[self.get_rank() + rank_delta][self.get_file() + file_delta]
            move = (self.get_rank() + rank_delta, self.get_file() + file_delta)

            if potential_space == "-":
                # if potential space is empty, this is a possible move
                self.get_move_set().add(move)
                return

            if potential_space != "-":
                if potential_space.get_color() == self.get_color():
                    # if potential space is occupied by same color piece, this move is not possible
                    return
                if potential_space.get_color() != self.get_color():
                    # if potential_space is occupied by enemy piece, this move is possible
                    self.get_move_set().add(move)
                    return
        except IndexError:
            pass

    def set_move_set(self, board):
        """
        knight can move on space orthogonally followed by one space diagonally away from starting pos
        :param board: game board
        :return: None
        """
        # empty move set
        self.direct_set_move_set(set())

        # up 2 left 1
        self.knight_logic(-2, -1, board)
        # up 2 right 1
        self.knight_logic(-2, 1, board)
        # right 2 up 1
        self.knight_logic(-1, 2, board)
        # right 2 down 1
        self.knight_logic(1, 2, board)
        # down 2 right 1
        self.knight_logic(2, 1, board)
        # down 2 left 1
        self.knight_logic(2, -1, board)
        # left 2 down 1
        self.knight_logic(1, -2, board)
        # left 2 up 1
        self.knight_logic(-1, -2, board)

        # remove negative values
        self.direct_set_move_set({i for i in self.get_move_set() if i[0] >= 0 and i[1] >= 0})
        # convert to letter-number format
        self.direct_set_move_set({format_to_let(i[0], i[1]) for i in self.get_move_set()})


# class rook
class Rook(Piece):
    """
    starts next to knight, corners of board
    moves any distance orthogonally
    may not jump over pieces
    """

    def __init__(self, rank, file, color):
        """
        initiates instance of Rook
        :param rank: horizontal rank
        :param file: vertical column
        """
        super().__init__(rank, file, color)
        self._callsign = "R"
        self._has_moved = False
        self._strength = 50

    def get_has_moved(self):
        """
        return _has_moved data member
        :return: has_moved bool
        """
        return self._has_moved

    def set_has_moved(self, has_moved):
        """
        set _has_moved data member
        :param has_moved: bool
        :return: None
        """
        self._has_moved = has_moved

    def rook_logic(self, rank_delta, file_delta, board):
        """
        adds specific moves to rook move set
        :param rank_delta: change in rank
        :param file_delta: change in delta
        :param board: game board
        :return: boolean value denoting whether to continue checking moves in the current direction
        """
        try:
            potential_space = board[self.get_rank() + rank_delta][self.get_file() + file_delta]
            move = (self.get_rank() + rank_delta, self.get_file() + file_delta)
            # empty space
            if potential_space == "-":
                # if potential space is empty, this is a possible move
                self.get_move_set().add(move)
                return True

            # non-empty space
            if potential_space != "-":
                if potential_space.get_color() == self.get_color():
                    # if potential space is occupied by same color piece, this move is not possible
                    return False
                if potential_space.get_color() != self.get_color():
                    # if potential_space is occupied by enemy piece, this move is possible
                    self.get_move_set().add(move)
                    return False

        except IndexError:
            pass

    def set_move_set(self, board):
        """
        list of all legal positions from current position
        :return: None
        """
        # empty move_set
        self.direct_set_move_set(set())

        for left in range(-1, -8, -1):
            if self.rook_logic(0, left, board):
                continue
            else:
                break
        for right in range(1, 8):
            if self.rook_logic(0, right, board):
                continue
            else:
                break
        for down in range(1, 8):
            if self.rook_logic(down, 0, board):
                continue
            else:
                break
        for up in range(-1, -8, -1):
            if self.rook_logic(up, 0, board):
                continue
            else:
                break

        # remove negative values
        self.direct_set_move_set({i for i in self.get_move_set() if i[0] >= 0 and i[1] >= 0})
        # convert to letter-number format
        self.direct_set_move_set({format_to_let(i[0], i[1]) for i in self.get_move_set()})


# class pawn (P)
class Pawn(Piece):
    """
    """

    def __init__(self, rank, file, color):
        """
        initiates instance of Pawn
        :param rank: horizontal rank
        :param file: vertical column
        """
        super().__init__(rank, file, color)
        self._callsign = "P"
        self._promote_to = None
        self._strength = 10

    def set_promote_to(self, promote_to):
        """
        sets the data member promote to
        :return: None
        """
        self._promote_to = promote_to

    def get_promote_to(self):
        """
        :return: promote_to data member
        """
        return self._promote_to

    def pawn_logic(self, rank_delta, file_delta, board):
        """
        adds forward move to pawn's move set
        :param rank_delta: change in rank
        :param file_delta: change in file
        :param board: game board
        :return: None
        """
        try:
            potential_space = board[self.get_rank() + rank_delta][self.get_file() + file_delta]
            move = (self.get_rank() + rank_delta, self.get_file() + file_delta)

            if potential_space == "-":
                # if potential space is empty, this is a possible move
                self.get_move_set().add(move)
                return

            if potential_space != "-":
                # if potential space is occupied by same color piece, this move is not possible
                return

        except IndexError:
            pass

    def pawn_cap_logic(self, rank_delta, file_delta, board):
        """
        adds capture moves to a pawn's move set
        :param rank_delta: change in rank
        :param file_delta: change in file
        :param board: game board
        :return: None
        """
        try:
            potential_space = board[self.get_rank() + rank_delta][self.get_file() + file_delta]
            move = (self.get_rank() + rank_delta, self.get_file() + file_delta)

            if potential_space == "-":
                # if potential space is empty, this is not a possible capture
                return

            if potential_space != "-":
                # if potential space is occupied by same color piece, this move is not possible
                if potential_space.get_color() != self.get_color():
                    # if potential space contains enemy, this is a possible capture
                    self.get_move_set().add(move)
                return
            return
        # if this move is off the board, it is not a possible move
        except IndexError:
            pass

    def set_move_set(self, board):
        """
        populates self._move_set with all possible moves
        pawn:   the space directly in front of it if empty
                diagonal spaces ahead if occupied by enemy
        :return: none
        """
        self.direct_set_move_set(set())
        # white
        if self.get_color() == "white":
            # forward 2 if first move
            if self.get_rank() == 6:
                self.pawn_logic(-2, 0, board)
            # forward 1
            self.pawn_logic(-1, 0, board)
            # capture left
            self.pawn_cap_logic(-1, -1, board)
            # capture right
            self.pawn_cap_logic(-1, 1, board)

        # black
        if self.get_color() == "black":
            # forward 2 if first move
            if self.get_rank() == 1:
                self.pawn_logic(2, 0, board)
            # forward 1
            self.pawn_logic(1, 0, board)
            # capture left
            self.pawn_cap_logic(1, -1, board)
            # capture right
            self.pawn_cap_logic(1, 1, board)

        # remove negative values by set comp
        self.direct_set_move_set({i for i in self.get_move_set() if i[0] >= 0 and i[1] >= 0})
        # convert to letter-number format
        self.direct_set_move_set({format_to_let(i[0], i[1]) for i in self.get_move_set()})

    def promotion(self, piece_list):
        """
        if pawn reaches opposite side of board, it can promote to a knight, bishop, rook, or queen
        :return: None
        """
        if self.get_color() == "white" and self.get_rank() == 0:
            # promote
            # promote_to = input("promote pawn to Q, R, B, or N? >")
            if self.get_promote_to() == "Q":
                piece_list.append(Queen(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)
            if self.get_promote_to() == "R":
                piece_list.append(Rook(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)
            if self.get_promote_to() == "B":
                piece_list.append(Bishop(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)
            if self.get_promote_to() == "N":
                piece_list.append(Knight(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)

        if self.get_color() == "black" and self.get_rank() == 7:
            # promote
            # promote_to = input("promote pawn to Q, R, B, or N? >")
            if self.get_promote_to() == "Q":
                piece_list.append(Queen(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)
            if self.get_promote_to() == "R":
                piece_list.append(Rook(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)
            if self.get_promote_to() == "B":
                piece_list.append(Bishop(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)
            if self.get_promote_to() == "N":
                piece_list.append(Knight(self.get_rank(), self.get_file(), self.get_color()))
                piece_list.remove(self)


def format_to_nums(string):
    """
    changes input string to a tuple of two coordinates
    :param string: letter of a file followed by the number of a rank, ex. "a8"
    :return: converted tuple, ex a8 returns (0, 0)
    """
    # format input
    # ascii code - 97 = x coordinate
    file = ord(string[0]) - 97

    # the absolute value of 8 - rank
    rank = abs(8 - (int(string[1:])))

    return rank, file


def format_to_let(rank, file):
    """
    formats two numbers to the letter of a file followed by the number of a rank
    :param rank: number of a rank, 0 - 7
    :param file: number of a file, 0 - 7
    :return: chess coordinate str
    """
    rank = str(8 - rank)
    file = chr(file + 97)
    return file + rank


if __name__ == '__main__':
    game = ChessGame()
    game.make_move("a2", "b3")
    print(game.print_board())
    game.make_move("a7", "a5")
    game.make_move("b2", "b4")
    game.make_move("a5", "b4")
    game.make_move("a4", "a5")
    game.make_move("a8", "a6")
    game.make_move("c2", "c3")
    game.make_move("a6", "b6")
    game.make_move("a5", "a6")
    game.make_move("b4", "b3")
    game.make_move("a6", "a7")
    game.make_move("b3", "b2")
    game.make_move("a7", "a8")
    game.make_move("b2", "a1")
    game.print_board()
