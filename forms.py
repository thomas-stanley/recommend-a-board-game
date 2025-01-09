from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired

class SearchGame(FlaskForm):
    board_game = StringField("Board Game", validators=[InputRequired()])
    search = SubmitField("Submit")

class PickGame(FlaskForm):
    game_name = HiddenField("Game Name")
    add_game = SubmitField()