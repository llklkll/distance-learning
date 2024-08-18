from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    group = SelectField('Класс', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11')])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_agree = PasswordField('Подтверждение пароля', validators=[DataRequired()])
    teacher = StringField('ФИО учителя', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Зарегистрироваться')