from flask import Flask, render_template, redirect, flash
from flask import make_response, jsonify
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_restful import Api

from config_key import secret_key  # файл в .gitignore
from data import db_session
from data.jobs import Jobs
from data.jobs_resource import JobsResource, JobsListResource
from data.users import User  # Import User model
from data.users_resource import UsersResource, UsersListResource
from forms.addjobform import AddJobForm
from forms.loginform import LoginForm
from forms.user import RegisterForm

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
    # app.register_blueprint(jobs_api.blueprint)

    # Регистрация ресурсов
    api.add_resource(JobsListResource, '/api/v2/jobs')  # Для списка задач
    api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')  # Для одной задачи
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')

    app.run()


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
