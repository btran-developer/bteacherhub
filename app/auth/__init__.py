from flask import render_template, flash, redirect, url_for, session, g, request, Blueprint
from app.models import User
from app.forms import LoginForm
from werkzeug.urls import url_parse
import functools

bp = Blueprint('auth', __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.path))

        return view(*args, **kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.path))

        if not g.user.is_admin:
            flash(message='Insufficient privilege.', category='danger')
            return redirect(url_for('index.index'))

        return view(*args, **kwargs)
    return wrapped_view


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log the user in
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        if user is None or not user.check_password(form.password.data):
            flash(message='Invalid username or password', category='danger')
            return redirect(url_for('auth.login', next=next_page))

        session.clear()
        session['user_id'] = user.id
        return redirect(next_page)

    return render_template('auth/login.html', title='Login Page', form=form)


@bp.route('/logout')
def logout():
    """
    Log out the user
    """
    session.clear()
    return redirect(url_for('auth.login'))
