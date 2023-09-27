from flask import session, redirect, url_for
import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session.keys():
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def logged_in(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" in session.keys():
            return redirect(url_for('blog.index'))
        return view(**kwargs)
    return wrapped_view


def get_log(f):
    @functools.wraps(f)
    def wrapped_func(*args, **kwargs):
        with open('record.log', 'r') as log_file:
            logs = log_file.readlines()
        kwargs['log'] = logs[-1]
        return f(*args, **kwargs)
    return wrapped_func
