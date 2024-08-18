from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired

class AddAchieveForm(FlaskForm):
    title = SelectField('Предмет', choices=[('Математика', 'Математика'), ('Иностранный язык', 'Иностранный язык'), ('Химия', 'Химия'), ('Русский язык', 'Русский язык'), ('Литература', 'Литература'), ('Физика', 'Физика'), ('Биология', 'Биология'), ('География', 'География'), ('История', 'История'), ('Обществознание', 'Обществознание'), ('Информатика', 'Информатика'), ('Другое', 'Другое')])
    adittion = StringField('Другое', validators=[DataRequired()])
    content = TextAreaField('Описание домашней работы', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Добавить')