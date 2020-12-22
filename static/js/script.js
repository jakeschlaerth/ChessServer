const baseURL = "http://192.168.0.191:5000";
const translate_callsign = {
    P: "pawn",
    N: "knight",
    B: "bishop",
    R: "rook",
    Q: "queen",
    K: "king"
}
const squares = [
    "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8",
    "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8",
    "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8",
    "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8",
    "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8",
    "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8",
    "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8",
]

render_board = (piece_list) => {
    // remove all pieces
    squares.map(square => {
        current_square = document.querySelector(`#${square}`);
        current_square.style = "background-image: none;";
    });

    // render each piece at appropriate square
    piece_list.map(piece => {
        current_piece_square = document.querySelector(`#${piece[0]}`);
        current_piece_square.style = `background-image: url(static/images/${piece[2]}-${translate_callsign[piece[1]]}.png);`;
    });
}

render_board(init_piece_list);

var square_from;
const mouse_down = (e) => {
    e.preventDefault;
    square_from = e.target.id;
}

const mouse_up = (e) => {
    e.preventDefault;
    var selected_bool = false;
    var square_to = e.target.id;
    if (square_from == square_to) {
        console.log(square_from + " selected");
        var selected_square = document.querySelector(`#${e.target.id}`);
        selected_square.style.backgroundColor = "#fff799";
        return;
    }
    var payload = {
        square_from: square_from,
        square_to: square_to
    };
    var req = new XMLHttpRequest;
    req.open("POST", baseURL, true);
    req.setRequestHeader('Content-Type', 'application/json');
    req.onload = (e) => {
        if (req.readyState === 4) {
            if (req.status === 200) {
                // this is where the magic happens
                game_data_array = JSON.parse(req.responseText);
                game_data = {
                    piece_list: game_data_array[0],
                    game_state: game_data_array[1],
                    white_is_in_check: game_data_array[2][0],
                    black_is_in_check: game_data_array[2][1],
                    legal_move: game_data_array[3]
                }
                // console.log(game_data);
                render_board(game_data.piece_list);
                // if (!game_data.legal_move) {
                //     alert(`Sorry, ${square_from} to ${square_to} is not a legal move.`)
                // }

                // is a player in check
                if (game_data.white_is_in_check) {
                    // find white king
                    var white_king = game_data.piece_list.find(piece => 
                        piece[1] == 'K' && piece[2] == "white");
                    var white_king_square = document.querySelector(`#${white_king[0]}`);
                    white_king_square.style.backgroundColor = "red";
                }

                if (game_data.black_is_in_check) {
                    // find black king
                    var black_king = game_data.piece_list.find(piece =>
                        piece[1] == 'K' && piece[2] == "black");
                    var black_king_square = document.querySelector(`#${black_king[0]}`);
                    black_king_square.style.backgroundColor = "red";
                }

                switch(game_data.game_state) {
                    case "WHITE_WON":
                        alert("Game over : white won by checkmate");
                        break;
                    case "BLACK_WON":
                        alert("Game over : black won by checkmate");
                        break;
                    case "DRAW":
                        alert("Game over: draw by stalemate");
                        break;
                } 
            } else {
                console.error(req.statusText);
            }
        }
    };
    req.send(JSON.stringify(payload));
}

const new_game = (e) => {
    var req = new XMLHttpRequest;
    req.open("PUT", baseURL, true);
    req.setRequestHeader('Content-Type', 'application/json');
    req.onload = (e) => {
        if (req.readyState === 4) {
            if (req.status === 200) {
                // this is where the magic happens
                game_data = JSON.parse(req.responseText);
                render_board(game_data[0]);
            } else {
                console.error(req.statusText);
            }
        }
    };
    req.send();
}

window.onload = function () {
    const reset_button = document.querySelector('.reset-button');
    reset_button.addEventListener('click', new_game);

    const board = document.querySelector('.chess-board');
    board.addEventListener('mousedown', mouse_down);
    board.addEventListener('mouseup', mouse_up);
}