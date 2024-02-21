from flask import Flask, request, render_template, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle
# from IPython.core.debugger import set_trace

app = Flask(__name__)
app.config["SECRET_KEY"] = "so-secret"

# debug = DebugToolbarExtension(app)

boggle_game = Boggle()
words = boggle_game.words

@app.route("/")
def start_game():
    """Generate and show game board."""
    my_board = boggle_game.make_board()
    session["board"] = my_board
    return render_template("index.html", my_board=my_board)

@app.route("/check-guess")
def check_guess():
    """Check whether the guessed word is in the dictionary."""
    word = request.args["guess"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, word)
    return jsonify({"result": result})

@app.route("/update-stats")
def update_stats():
    """On completion of a game, update stats to reflect number of games played and high score."""

    if session.get("games_played", 0) == 0:
        session["games_played"] = 0
        session["high_score"] = 0
    
    games_played = session["games_played"]
    games_played += 1
    session["games_played"] = games_played

    high_score = session["high_score"]

    score = int(request.args["score"])

    if score > high_score:
        high_score = score
        session["high_score"] = high_score

    return jsonify({"games_played": games_played, "high_score": high_score})