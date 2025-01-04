from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class BoardGameForm(FlaskForm):
    board_game = StringField("Board Game", validators=[InputRequired()])
    submit = SubmitField("Lookup")
