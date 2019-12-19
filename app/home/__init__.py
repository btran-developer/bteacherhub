from flask import Blueprint, render_template
from app.auth import login_required

bp = Blueprint('index', __name__)


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """
    Menu page
    """
    return render_template('index.html', title='Home')
