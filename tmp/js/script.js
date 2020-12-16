const baseURL = "http://localhost:5000";
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
    // render each piece at appropiate square
    piece_list.map(piece => {
        current_piece_square = document.querySelector(`#${piece[0]}`);
        current_piece_square.style = `background-image: url(tmp/images/${piece[2]}-${translate_callsign[piece[1]]}.png);`;
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
    var square_to = e.target.id;
    var payload = {
        new_game: false,
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
                game_data = JSON.parse(req.responseText);
                console.log(game_data);
                render_board(game_data[0]);
                if (game_data[1] == "WHITE_WON") {
                    alert("Game over : white won by checkmate");
                }
                if (game_data[1] == "BLACK_WON")
                {
                    alert("Game over : black won by checkmate");
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
                console.log(game_data);
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