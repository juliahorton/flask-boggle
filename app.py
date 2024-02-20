from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "so-secret"
# app.config["SESSION_REFRESH_EACH_REQUEST"] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()
words = boggle_game.words

@app.route("/")
def start_game():
    my_board = boggle_game.make_board()
    session["board"] = my_board
    return render_template("index.html", my_board=my_board)

@app.route("/check-guess")
def check_guess():
    word = request.args["guess"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, word)
    return jsonify({"result": result})
