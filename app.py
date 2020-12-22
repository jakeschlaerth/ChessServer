#!flask/bin/python
import sys
from flask import Flask, render_template, request, redirect, Response, json, jsonify
from flask_cors import CORS
import random
from ChessRules import ChessGame, Piece, King, Queen, Rook, Bishop, Knight, Pawn, format_to_nums, format_to_let
from sunfish import *

app = Flask(__name__, static_url_path="/static", static_folder="static")
CORS(app) # rpi , resources={r"/": {"origins": "http://localhost:5000"}})

game = ChessGame()


# sunfish code
# hist = [Position(initial, 0, (True,True), (True,True), 0, 0)]
# searcher = Searcher()
# while True:
#     print_pos(hist[-1])
#
#     if hist[-1].score <= -MATE_LOWER:
#         print("You lost")
#         break
#
#     # We query the user until she enters a (pseudo) legal move.
#     move = None
#     while move not in hist[-1].gen_moves():
#         match = re.match('([a-h][1-8])'*2, input('Your move: '))
#         if match:
#             move = parse(match.group(1)), parse(match.group(2))
#         else:
#             # Inform the user when invalid input (e.g. "help") is entered
#             print("Please enter a move like g8f6")
#     hist.append(hist[-1].move(move))
#
#     # After our move we rotate the board and print it again.
#     # This allows us to see the effect of our move.
#     print_pos(hist[-1].rotate())
#
#     if hist[-1].score <= -MATE_LOWER:
#         print("You won")
#         break
#
#     # Fire up the engine to look for a move.
#     start = time.time()
#     for _depth, move, score in searcher.search(hist[-1], hist):
#         if time.time() - start > 1:
#             break
#
#     if score == MATE_UPPER:
#         print("Checkmate!")
#
#     # The black player moves from a rotated position, so we have to
#     # 'back rotate' the move before printing it.
#
#     print("My move:", render(119-move[0]) + render(119-move[1]))
#
#     hist.append(hist[-1].move(move))
#
#     computer_move = (render(119-move[0]), render(119-move[1]))


@app.route('/', methods=['GET'])
def output():
    piece_list = game.get_piece_list()
    json_piece_list = []
    for piece in piece_list:
        json_piece_list.append(
            [format_to_let(piece.get_rank(), piece.get_file()), piece.get_callsign(), piece.get_color()])

    return render_template('index.html',
                           piece_list=json_piece_list)


@app.route('/', methods=['POST'])
def worker():
    square_from = request.get_json()["square_from"]
    square_to = request.get_json()["square_to"]
    legal_move = game.make_move(square_from, square_to)

    piece_list = game.get_piece_list()
    json_piece_list = []
    for piece in piece_list:
        json_piece_list.append(
            [format_to_let(piece.get_rank(), piece.get_file()), piece.get_callsign(), piece.get_color()])
    game_data = [
        json_piece_list,
        game.get_game_state(),
        [game.is_in_check("white"), game.is_in_check("black")],
        legal_move
    ]
    response = jsonify(game_data)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/', methods=['PUT'])
def new_game():
    # reset game
    game.reset()
    piece_list = game.get_piece_list()
    json_piece_list = []
    for piece in piece_list:
        json_piece_list.append(
            [format_to_let(piece.get_rank(), piece.get_file()), piece.get_callsign(), piece.get_color()])
    game_data = [json_piece_list, game.get_game_state(), [game.is_in_check("white"), game.is_in_check("black")]]
    response = jsonify(game_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    # run!
    app.run(debug=True, host='0.0.0.0')
