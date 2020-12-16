#!flask/bin/python
import sys
from flask import Flask, render_template, request, redirect, Response, json, jsonify
from flask_cors import CORS
import random
from ChessRules import ChessGame, Piece, King, Queen, Rook, Bishop, Knight, Pawn, format_to_nums, format_to_let

app = Flask(__name__, static_url_path="/static", static_folder="static")
CORS(app)

game = ChessGame()


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
    print("in post")
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
    app.run()
