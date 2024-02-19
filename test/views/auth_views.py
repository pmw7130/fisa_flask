from flask import Blueprint, request, redirect, render_template, flash, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from test.forms import UserCreateForm, UserLoginForm
from test.models import User
from test import db
import functools

auth = Blueprint('auth', __name__, url_prefix="/auth")
# __init__ 의 create_app 안에 등록


# 회원 가입 - signup
@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    #1. 폼을 가져온다
    form = UserCreateForm()

    ## update와 유사한 로직으로 작동합니다 
    #2-1. 폼의 유효성을 확인한다 & db에 해당하는 사용자이름이 있는지도 확인
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            #2-1-1. db의 user 테이블에 값을 넣는다  
            user = User(username=form.username.data, \
                        password=generate_password_hash(form.password1.data), \
                        email=form.email.data)                                                 
            db.session.add(user)
            db.session.commit()
            return redirect( url_for( 'main.index' ) )
        #2-1-2. 이미 존재하는 사용자입니다
        else:
            flash('이미 가입한 아이디입니다')
    #2-2. 다시 auth/signup.html로 이동시킵니다.
    return render_template('auth/signup.html', form=form)

# 로그인 - login
# signup 함수와 비슷하게 동작
@auth.route("/login", methods=['GET', 'POST'])
def login():
# post로 값이 들어오면 비밀번호 일치여부에 따라 로그인
    form = UserLoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        # print("-------------", user.password, form.password.data)
        if not user:
            flash("존재하지 않는 사용자입니다")
        elif not check_password_hash(user.password, form.password.data):
            flash("비밀번호가 틀렸습니다")
        # 비밀번호가 일치하는 경우 
        else:
    # 세션에 user_id라는 객체 생성
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')  # board/list 
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        # 에러메시지를 flash 한테 넘깁니다
        # 문제가 있으면 그 문제를 form_errors.html로 보내버리는 역할 
        flash("error")
    return render_template('auth/login.html', form=form)


# auth로 시작하는 블루프린트가 주소창에 가기 전에 무조건 실행되는 애너테이션
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
         # 없으면 로그아웃 상태라는 것을 파악한다
        g.user = None
    else:
        # @auth 를 통해서 라우팅을 하면 로그인이 되어있으면 로그인 사람의 모든 회원정보를 테이블에 가져오고
        g.user = User.query.get(user_id)
        # print(g.user, g.user.username, g.user.password)



# 로그아웃 - logout 
@auth.route("/logout")
def logout():
    session.clear()
    return redirect( url_for('main.index') )

# 우리가 직접 어노테이션을 만들어서
# 접근이 불가한 페이지에 접근하면 로그인을 유도하도록 만든다
def login_required(view):  # login_required(create) localhost:5000/board/create
    @functools.wraps(view)
    def warpped_views(*args, **kwargs):   # create/list, ?page=1
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return warpped_views