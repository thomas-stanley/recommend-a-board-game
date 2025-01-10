from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField
from wtforms.validators import InputRequired

class SearchGame(FlaskForm):
    board_game = StringField("Board Game", validators=[InputRequired()])
    search = SubmitField("Submit")

class PickGame(FlaskForm):
    game_name = HiddenField("Game Name")
    add_game = SubmitField()


class RateGame(FlaskForm):
    ratings = RadioField("Rating", choices=[(2, "Strongly Like"), (1, "Like"), (0, "Neutral"), (-1, "Dislike"), (-2, "Strongly Dislike")], validators=[InputRequired()])
    submit = SubmitField("Submit")