from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
                    #field name = datatypefield('label', validators = [LIST of validators])
    name = StringField('Pokemon',validators=[DataRequired()])
    
    submit = SubmitField('Show me!')

class GameForm(FlaskForm):
    choice = StringField('Rock, Paper, Scissors...',validators=[DataRequired()] )
    submit = SubmitField('Shoot!')
