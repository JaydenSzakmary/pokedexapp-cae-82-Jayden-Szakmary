from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
                    #field name = datatypefield('label', validators = [LIST of validators])
    name = StringField('Enter the pokemon you would like to see!',validators=[DataRequired()])
    
    submit = SubmitField('Show me!')
