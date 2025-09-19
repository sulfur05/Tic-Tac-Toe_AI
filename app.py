from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)            # diagonals
]

def check_winner(board):
    for a,b,c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "Draw"
    return None

def minimax(board, player, ai, maximizing):
    winner = check_winner(board)
    if winner == ai:
        return (1, None)
    elif winner == "Draw":
        return (0, None)
    elif winner is not None:
        return (-1, None)

    if maximizing:
        best_val = -math.inf
        best_move = None
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score, _ = minimax(board, "O" if player == "X" else "X", ai, False)
                board[i] = " "
                if score > best_val:
                    best_val = score
                    best_move = i
        return best_val, best_move
    else:
        best_val = math.inf
        best_move = None
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score, _ = minimax(board, "O" if player == "X" else "X", ai, True)
                board[i] = " "
                if score < best_val:
                    best_val = score
                    best_move = i
        return best_val, best_move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]
    ai = data["ai"]
    _, best_move = minimax(board, ai, ai, True)
    return jsonify({"move": best_move})

if __name__ == "__main__":
    app.run(debug=True)
