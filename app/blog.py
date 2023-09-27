from flask import Blueprint, render_template, session
from app.models import User
from app.deco import login_required, get_log


bp = Blueprint('blog', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
@login_required
@get_log
def index(log=None):
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('index.html', user=user, log=log)


@bp.route('/', methods=['GET'])
def something():
    return ''
