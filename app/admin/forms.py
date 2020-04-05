from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('密码', validators=[DataRequired()])
    fullname = StringField('姓名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    email = StringField('邮箱')
    phone = StringField('电话')
    status = BooleanField('生效')
    permission = IntegerField('权限')
    submit = SubmitField('提交')
