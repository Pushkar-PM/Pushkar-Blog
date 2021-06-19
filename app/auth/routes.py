from app import db
from flask import render_template,flash,redirect,url_for,request,g
from app.auth.forms import LoginForm,RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm
from app.auth.email import send_email,send_password_reset_email
from guess_language import guess_language
from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse
from datetime import datetime
from flask_babel import get_locale,_
from app.models import User,Post
from app.auth import bp


@bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid login"))
            return redirect(url_for('auth.login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html',title=_("login"),form=form)
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_("Congratulations you have successfully registered"))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',title=_('Register'),form=form)

@bp.route('/reset_password_request',methods=['POST','GET'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_("Check email for instructions"))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',form=form,title=_('Reset'))

@bp.route('/reset_password/<token>',methods=['POST','GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user=User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Password has been reset'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)
