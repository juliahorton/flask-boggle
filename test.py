from app import app
from flask import session
from boggle import Boggle
from unittest import TestCase


class FlaskTests(TestCase):

    def setUp(self):
        """Things to do before each test is run."""
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_start_game(self):
        """Make sure that board is displayed and session request vars are properly set."""
        with self.client as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button id="start">Begin Game</button>', html)
            self.assertIsNotNone(session.get("board"))
            self.assertIsNone(session.get("games_played"))
            self.assertIsNone(session.get("high_score"))
            self.assertIn("<p>High score:", html)
            self.assertIn("<p>Games played:", html)
            self.assertIn("<p>Time remaining:", html)


    def test_valid_word(self):
        """Test if word is valid on a given board by modifying board in session."""
        with self.client as client:
            with client.session_transaction() as session:
                session["board"] = [["P", "L", "A", "C", "E"],
                                    ["P", "L", "A", "C", "E"],
                                    ["P", "L", "A", "C", "E"],
                                    ["P", "L", "A", "C", "E"],
                                    ["P", "L", "A", "C", "E"]]
                
            resp = client.get("/check-guess?guess=place")
            self.assertEqual(resp.json, {"result": "ok"})

    def test_word_not_on_board(self):
        """Test if word is valid on board."""

        with self.client as client:
            client.get("/")
            resp = self.client.get("/check-guess?guess=plate")
            self.assertEqual(resp.json, {"result": "not-on-board"})

    def test_word_not_in_dict(self):
        """Test if word is in dictionary."""

        with self.client as client:
            client.get("/")
            resp = client.get("/check-guess?guess=plade")
            self.assertEqual(resp.json, {'result': 'not-word'})