from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired,url
class UrlShortnerForm(FlaskForm):
    url = URLField('Enter the url',validators=[DataRequired(),url()])
    code = StringField('Enter the code',validators=[DataRequired()])
    submit = SubmitField('Shorten')

class ImageShortenForm(FlaskForm):
    file = FileField('File',validators=[DataRequired()])
    code = StringField('Enter the code',validators=[DataRequired()])
    submit = SubmitField('Shorten')
