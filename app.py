from flask import Flask, render_template, request, jsonify, session
import tictactoe as ttt
import uuid

app = Flask(__name__)
app.secret_key = "test"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new_game", methods=["POST"])
def new_game():
    game_id = str(uuid.uuid4())
    session["game_id"] = game_id
    session["board"] = ttt.initial_state()
    session["user_player"] = request.json.get("player", ttt.X)
    session["game_over"] = False
    session["winner"] = None

    board = session["board"]
    ttt.player(board)

    if session["user_player"] == ttt.O:
        ai_move = ttt.minimax(board)
        if ai_move:
            board = ttt.result(board, ai_move)
            session["board"] = board

    return jsonify(
        {
            "board": board,
            "current_player": ttt.player(board),
            "user_player": session["user_player"],
            "game_over": False,
            "winner": None,
        }
    )


@app.route("/make_move", methods=["POST"])
def make_move():
    if "board" not in session:
        return jsonify({"error": "No active game"}), 400

    data = request.json
    row, col = data["row"], data["col"]
    board = session["board"]
    user_player = session["user_player"]

    if board[row][col] != ttt.EMPTY:
        return jsonify({"error": "Invalid move"}), 400

    if ttt.terminal(board):
        return jsonify({"error": "Game is over"}), 400

    if ttt.player(board) != user_player:
        return jsonify({"error": "Not your turn"}), 400

    try:
        board = ttt.result(board, (row, col))
        session["board"] = board
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if ttt.terminal(board):
        winner = ttt.winner(board)
        session["game_over"] = True
        session["winner"] = winner
        return jsonify(
            {
                "board": board,
                "current_player": None,
                "user_player": user_player,
                "game_over": True,
                "winner": winner,
                "user_move": (row, col),
                "ai_move": None,
            }
        )

    ai_move = ttt.minimax(board)
    ai_move_coords = None
    if ai_move:
        board = ttt.result(board, ai_move)
        session["board"] = board
        ai_move_coords = ai_move

    game_over = ttt.terminal(board)
    winner = ttt.winner(board) if game_over else None
    session["game_over"] = game_over
    session["winner"] = winner

    return jsonify(
        {
            "board": board,
            "current_player": ttt.player(board) if not game_over else None,
            "user_player": user_player,
            "game_over": game_over,
            "winner": winner,
            "user_move": (row, col),
            "ai_move": ai_move_coords,
        }
    )


@app.route("/game_state", methods=["GET"])
def game_state():
    if "board" not in session:
        return jsonify({"error": "No active game"}), 400

    return jsonify(
        {
            "board": session["board"],
            "current_player": (
                ttt.player(session["board"]) if not session.get("game_over") else None
            ),
            "user_player": session.get("user_player"),
            "game_over": session.get("game_over", False),
            "winner": session.get("winner"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
