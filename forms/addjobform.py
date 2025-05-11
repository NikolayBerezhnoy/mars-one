from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('ID лидера', validators=[DataRequired()])
    work_size = IntegerField('Объем работы в часах', validators=[DataRequired()])
    collaborators = StringField('Участники (список id)', validators=[DataRequired()])
    end_date = DateField('Дата окончания', validators=[DataRequired()])
    is_finished = BooleanField('Работа закончена?')

    submit = SubmitField('Добавить')