from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired


class RegisterTeacherForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_agree = PasswordField('Подтверждение пароля', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Зарегистрироваться')