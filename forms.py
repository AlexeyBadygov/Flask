from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email('Некорректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=3, max=8, message='Пароль должент быть от '
                                                                                             '3 до 8 символов')])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[Length(min=1, max=5, message='Имя должно быть от 1 до 5 символов')])
    email = StringField('Email: ', validators=[Email('Некорректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=3, max=8, message='Пароль должен быть от 3 '
                                                                                             'до 8 символов')])
    psw2 = PasswordField('Повтор пароля', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Регистрация')
