# Flask
from flask import Flask, flash, request, make_response, redirect, render_template, session, url_for, flash

# Bootstrap
from flask_bootstrap import Bootstrap

# What the forms
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['Buy coffe', 'Go to work', 'Make dinner']

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def not_found(error):
    """
    Not Found
    """
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    """
    Server Error
    """
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    # response.set_cookie('user_ip', user_ip)
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('User Name Register Successfully!')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)