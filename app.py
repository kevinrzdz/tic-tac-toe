from flask import Flask, render_template, request, jsonify, session
import tictactoe as ttt
import uuid
import time

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
    session["start_time"] = time.time()
    session["move_count"] = 0

    board = session["board"]
    current_player = ttt.player(board)

    if session["user_player"] == ttt.O:
        ai_move = ttt.minimax(board)
        if ai_move:
            board = ttt.result(board, ai_move)
            session["board"] = board
            session["move_count"] += 1
            current_player = ttt.player(board)

    return jsonify(
        {
            "board": board,
            "current_player": current_player,
            "user_player": session["user_player"],
            "game_over": False,
            "winner": None,
            "move_count": session["move_count"],
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
        session["move_count"] += 1
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    user_move = (row, col)
    ai_move_coords = None

    if ttt.terminal(board):
        winner = ttt.winner(board)
        session["game_over"] = True
        session["winner"] = winner
        session["end_time"] = time.time()

        return jsonify(
            {
                "board": board,
                "current_player": None,
                "user_player": user_player,
                "game_over": True,
                "winner": winner,
                "user_move": user_move,
                "ai_move": None,
                "move_count": session["move_count"],
                "game_duration": session.get("end_time", time.time())
                - session["start_time"],
            }
        )

    ai_move = ttt.minimax(board)
    if ai_move:
        board = ttt.result(board, ai_move)
        session["board"] = board
        session["move_count"] += 1
        ai_move_coords = ai_move

    game_over = ttt.terminal(board)
    winner = ttt.winner(board) if game_over else None
    session["game_over"] = game_over
    session["winner"] = winner

    if game_over:
        session["end_time"] = time.time()

    response_data = {
        "board": board,
        "current_player": ttt.player(board) if not game_over else None,
        "user_player": user_player,
        "game_over": game_over,
        "winner": winner,
        "user_move": user_move,
        "ai_move": ai_move_coords,
        "move_count": session["move_count"],
    }

    if game_over:
        response_data["game_duration"] = (
            session.get("end_time", time.time()) - session["start_time"]
        )

    return jsonify(response_data)


@app.route("/game_state", methods=["GET"])
def game_state():
    if "board" not in session:
        return jsonify({"error": "No active game"}), 400

    response_data = {
        "board": session["board"],
        "current_player": (
            ttt.player(session["board"]) if not session.get("game_over") else None
        ),
        "user_player": session.get("user_player"),
        "game_over": session.get("game_over", False),
        "winner": session.get("winner"),
        "move_count": session.get("move_count", 0),
    }

    if session.get("game_over") and "end_time" in session:
        response_data["game_duration"] = session["end_time"] - session["start_time"]

    return jsonify(response_data)


@app.route("/reset_stats", methods=["POST"])
def reset_stats():
    return jsonify({"message": "Stats reset functionality handled client-side"})


if __name__ == "__main__":
    app.run(debug=True)
