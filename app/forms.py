from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
# from wtforms.validators import DataRequired

class PhotoForm(FlaskForm):
    photo = FileField('Select Image', validators=[
        FileRequired('File was empty!'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Image only!')
    ])
    # submit = SubmitField('Generate Caption')
    submit = SubmitField('Upload Image')

class CaptionForm(FlaskForm):
    submit = SubmitField('Generate Caption')