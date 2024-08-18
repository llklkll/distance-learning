from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired


class ChangeForm(FlaskForm):
    group = SelectField('Класс', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11')])
    teacher = StringField('ФИО учителя', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Отправить')