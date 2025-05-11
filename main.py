from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session, jobs_api
from data.jobs import Jobs
from data.users import User  # Import User model
from forms.loginform import LoginForm
from config_key import secret_key  # файл в .gitignore
from forms.user import RegisterForm
from forms.addjobform import AddJobForm
from flask_login import LoginManager
from flask_login import login_user
from flask import make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data.jobs_resources import JobsResource, JobsListResource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = secret_key  # можно указать любой

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/mars_explorer.db")
db_sess = db_session.create_session()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route('/')
@app.route('/index')
@app.route('/<title>')
@app.route('/index/<title>')
def index(title='Домашняя страница', user_name='Mars One'):
    global db_sess
    a = []
    for job in db_sess.query(Jobs).all():
        a.append(job)
    return render_template('works_log.html', title=title, lst=a)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global db_sess
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
            surname=form.surname.data,
            email=form.email.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return index('Welcome', user.name)
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/training/<prof>')
def training(prof=''):
    spec = "Научные симуляторы"
    if "инженер" in prof.lower() or "строитель" in prof.lower():
        spec = "Инженерные тренажеры"
    return render_template('prof.html', prof=spec)

@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        db_sess.close()
        flash('Работа успешно добавлена!', 'success')
        return redirect('/')
    return render_template('addjob.html', title='Добавление работы', form=form)

@app.route('/list_prof/<numeration>')
def list_prof(numeration=''):
    lst = ['Инженер-исследователь',
           'Инженер-строитель',
           'Пилот',
           'Метеоролог',
           'Инженер по жизнеобеспечению',
           'Инженер по радиационной защите',
           'Врач',
           'Экзобиолог']
    return render_template('list.html', list=lst, format=numeration)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    dict1 = {"Фамилия": "Иванов",
             "Имя": "Иван",
             "Образование": "высшее",
             "Профессия": "штурман",
             "Пол": "male",
             "Мотивация": "Всегда мечтал застрять на Марсе",
             "Готовы остаться": True}
    return render_template('auto_answer.html', dictt=dict1)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect('/success')
#     return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


def main():
    #app.register_blueprint(jobs_api.blueprint)

    # Регистрация ресурсов
    api.add_resource(JobsListResource, '/api/v2/jobs')  # Для списка задач
    api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')  # Для одной задачи


    # db_session.global_init("db/mars_explorer.db")
    # db_sess = db_session.create_session()
    # user = User()
    # user.surname = "Scott"
    # user.name = "Ridley"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = "research engineer"
    # user.address = "module_1"
    # user.email = "scott_chief@mars.org"
    # db_sess.add(user)
    #
    # user1 = User()
    # user1.surname = "Ivan"
    # user1.name = "Ivanov"
    # user1.age = 23
    # user1.position = "captain"
    # user1.speciality = "research engineer"
    # user1.address = "module_2"
    # user1.email = "ivanov@mars.org"
    # db_sess.add(user1)
    #
    # user2 = User()
    # user2.surname = "Petr"
    # user2.name = "Petrov"
    # user2.age = 35
    # user2.position = "captain"
    # user2.speciality = "research engineer"
    # user2.address = "module_2"
    # user2.email = "petrov@mars.org"
    # db_sess.add(user2)
    #
    # user3 = User()
    # user3.surname = "Pavel"
    # user3.name = "Pavlov"
    # user3.age = 40
    # user3.position = "captain"
    # user3.speciality = "research engineer"
    # user3.address = "module_3"
    # user3.email = "pavlov@mars.org"
    # db_sess.add(user3)
    #
    # job = Jobs()
    # job.team_leader = 2
    # job.job = "Exploration of mineral resources"
    # job.work_size = 12
    # job.collaborators = "1, 3"
    #
    # db_sess.add(job)
    #
    # db_sess.commit()
    # db_sess.close()

    app.run()


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')