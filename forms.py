from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError , TextAreaField, SelectMultipleField, URLField, EmailField, IntegerField 
from wtforms.validators import DataRequired, EqualTo, Length , Regexp, ValidationError
from wtforms.widgets import TextArea , TextInput
from flask_wtf.file import FileField ,FileRequired, FileAllowed
import phonenumbers


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    works = StringField("Works", validators=[DataRequired()])
    educations = StringField("Educations", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    language = StringField("Language", validators=[DataRequired()])
    interests = TextInput("Interests")
    url = StringField('URL*', validators=[DataRequired('URL is required'),Regexp('^(http|https):\/\/[\w.\-]+(\.[\w.\-]+)+.*$', 0,'URL must be a valid link')])
    about_info= TextAreaField("About Info")
    profile_picture = FileField('Profile Picture', validators=[FileRequired(),DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    cover_picture = FileField('Cover Picture', validators=[FileRequired(),DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2', message='Password Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Post")
    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
class PostForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    # username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
class RepostForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")
class CommentForm(FlaskForm):
    comment = StringField("Comment", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

class WorkForm(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()])
    company_post = StringField("Company Post", validators=[DataRequired()])
    work_details = StringField("Work Details", validators=[DataRequired()])
    submit = SubmitField("Submit")

# class InterestsForm(FlaskForm):
#     interests = StringField("Interests", validators=[DataRequired()])
#     submit = SubmitField("Submit")    
    

