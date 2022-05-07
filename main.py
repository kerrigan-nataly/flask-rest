from flask import Flask, make_response, jsonify, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session, news_api, jobs_api, users_api
from data.users import User
from data.category import Category
from data.news import News
from data.jobs import Jobs
from forms.user import LoginForm, RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()

    users = db_sess.query(User)

    return render_template('index.html', users=users, current_user=current_user)


@app.route('/user_show')
@login_required
def current_user_show():
    db_sess = db_session.create_session()
    user = current_user

    return render_template('nostalgy.html', user=user, current_user=current_user)


@app.route('/user_show/<int:user_id>')
def user_show(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    return render_template('nostalgy.html', user=user, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            city_from=form.city_from.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Server internal error'}), 500)


def prep_db(session):
    cap = User()
    cap.surname = "Scott"
    cap.name = "Ridley"
    cap.age = 21
    cap.position = "captain"
    cap.speciality = "research engineer"
    cap.address = "module_1"
    cap.email = "cap@mars.org"
    cap.city_from = "Саут-Шилдс"
    cap.set_password('test')

    nav = User()
    nav.surname = "Watny"
    nav.name = "Mark"
    nav.age = 25
    nav.position = "rover navigator"
    nav.speciality = "navigator"
    nav.address = "module_2"
    nav.city_from = "Москва"
    nav.email = "mark_wanty@mars.org"

    astro1 = User()
    astro1.surname = "Weir"
    astro1.name = "Andy"
    astro1.age = 49
    astro1.position = "scientist"
    astro1.speciality = "climatologist"
    astro1.address = "module_2"
    astro1.city_from = "Веллингтон"
    astro1.email = "andy_weir@mars.org"

    astro2 = User()
    astro2.surname = "Sanders"
    astro2.name = "Teddy"
    astro2.age = 41
    astro2.position = "NASA director"
    astro2.speciality = "tourist"
    astro2.address = "module_2"
    astro2.city_from = "Сент-Пол"
    astro2.email = "teddy_sanders@mars.org"

    astro3 = User()
    astro3.surname = "Sigourney"
    astro3.name = "Weaver"
    astro3.age = 30
    astro3.position = "Secondary pilot"
    astro3.speciality = "warrant officer"
    astro3.address = "module_2"
    astro3.city_from = "Манхэттен"
    astro3.email = "weaver_sigourney@mars.org"

    astro4 = User()
    astro4.surname = "House"
    astro4.name = "Gregory"
    astro4.age = 49
    astro4.position = "chief medical officer"
    astro4.speciality = "therapist"
    astro4.address = "module_3"
    astro4.city_from = "Принстон"
    astro4.email = "house_gregory@mars.org"

    cat1 = Category()
    cat1.name = 'Hazard 1'

    cat2 = Category()
    cat2.name = 'Hazard 2'

    cat3 = Category()
    cat3.name = 'Hazard 3'

    session.add(cap)
    session.add(nav)
    session.add(astro1)
    session.add(astro2)
    session.add(astro3)
    session.add(astro4)
    session.add(cat1)
    session.add(cat2)
    session.add(cat3)
    session.commit()

    news1 = News()
    news1.title = "Новость 1"
    news1.content = "Содержание новости 1"
    news1.categories.append(cat1)
    news1.user_id = 1

    news2 = News()
    news2.title = "Новость 2"
    news2.content = "Содержание новости 2"
    news2.categories.append(cat2)
    news2.user_id = 1

    news3 = News()
    news3.title = "Новость 3"
    news3.content = "Содержание новости 3"
    news3.categories.append(cat3)
    news3.user_id = 2

    job1 = Jobs()
    job1.job = "New job 1"
    job1.work_size = 2
    job1.team_leader = 1
    job1.is_finished = True

    job2 = Jobs()
    job2.job = "New job 2"
    job2.work_size = 5
    job2.team_leader = 2
    job2.is_finished = False

    session.add(news1)
    session.add(news2)
    session.add(news3)

    session.add(job1)
    session.add(job2)

    session.commit()


def main():
    db_session.global_init("db/mars_one.db")
    app.register_blueprint(news_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    session = db_session.create_session()
    users = session.query(User).all()
    if not users:
        prep_db(session)
    app.run()


if __name__ == '__main__':
    main()
