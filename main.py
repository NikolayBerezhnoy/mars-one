from flask import Flask, render_template
from datetime import datetime
from data import db_session
from data.users import User
from data.jobs import Jobs
from loginform import LoginForm
from config_key import secret_key # файл в .gitignore

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key # можно указать любой

@app.route('/')
@app.route('/index')
@app.route('/<title>')
@app.route('/index/<title>')
def index(title='Домашняя страница'):
    return render_template('base.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    pass

@app.route('/training/<prof>')
def training(prof=''):
    spec = "Научные симуляторы"
    if "инженер" in prof.lower() or "строитель" in prof.lower():
        spec = "Инженерные тренажеры"

    return render_template('prof.html', prof=spec)

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
    dict1 = {"Фамилия":"Иванов",
              "Имя": "Иван",
                "Образование":"высшее",
                  "Профессия":"штурман",
                    "Пол":"male", "Мотивация":"Всегда мечтал застрять на Марсе",
                      "Готовы остаться":True}
    return render_template('auto_answer.html', dictt=dict1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

def main():
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

    # user1 = User()
    # user1.surname = "Ivan"
    # user1.name = "Ivanov"
    # user1.age = 23
    # user1.position = "captain"
    # user1.speciality = "research engineer"
    # user1.address = "module_2"
    # user1.email = "ivanov@mars.org"
    # db_sess.add(user1)

    # user2 = User()
    # user2.surname = "Petr"
    # user2.name = "Petrov"
    # user2.age = 35
    # user2.position = "captain"
    # user2.speciality = "research engineer"
    # user2.address = "module_2"
    # user2.email = "petrov@mars.org"
    # db_sess.add(user2)

    # user3 = User()
    # user3.surname = "Pavel"
    # user3.name = "Pavlov"
    # user3.age = 40
    # user3.position = "captain"
    # user3.speciality = "research engineer"
    # user3.address = "module_3"
    # user3.email = "pavlov@mars.org"
    # db_sess.add(user3)

    # job = Jobs()
    # job.team_leader = 1
    # job.job = "deployment of residential modules 1 and 2"
    # job.work_size = 15
    # job.collaborators = "2, 3"
    
    # db_sess.add(job)

    # db_sess.commit()
    # db_sess.close()

    app.run()

if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
