from db import DB
from add_achieve import AddAchieveForm
from flask import Flask, redirect, render_template, session, url_for
from login_form import LoginForm
from user_model import UsersModel
from achieve_model import AchieveModel
from reg_form import RegisterForm
from change_model import ChangeForm
from regteacher_form import RegisterTeacherForm
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
AchieveModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()
admin_model = UsersModel(db.get_connection())
existss = admin_model.exists('Svetlana', '0000')
if not (existss[0]):
    pass
    admin_model.insert('Ямбарышева Светлана Юрьевна', '-', 'Svetlana', '0000', '-',
                       'teacher', 'sy.jpg')

existss = admin_model.exists('Elena', '0000')
if not (existss[0]):
    pass
    admin_model.insert('Корзунина Елена Владимировна', '-', 'Elena', '0000', '-',
                        'teacher', 'ev.jpg')
    

# http://127.0.0.1:8080/login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    already = False
    if 'username' in session:
        return redirect("/logout")
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        already = False
        if (exists[0]):
            alredy = True
            session['username'] = user_name
            session['user_id'] = exists[1]
            if UsersModel(db.get_connection()).get(session['user_id'])[6] == 'teacher':
                return redirect("/index_teacher")
            return redirect("/index")
    return render_template('login.html', title='Авторизация',
                           form=form, already=already)

@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')

# http://127.0.0.1:8080/reg
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    already = False
    true_password = False
    teacher_exist = True
    file_ok = True
    if form.validate_on_submit():
        name = form.name.data
        group = form.group.data
        user_name = form.username.data
        password = form.password.data
        password_agree = form.password_agree.data
        if password != password_agree:
            true_password = True
        teacher = form.teacher.data
        teacher_exist = False
        all_user = UsersModel(db.get_connection()).get_all()
        for user in all_user:
            if user[1] == teacher and user[6] == 'teacher':
                teacher_exist = True
                break
        filename = secure_filename(form.file.data.filename)
        file_ok = False
        if '.' in filename and (filename.split('.')[1] in ['jpg', 'JPG', 'bmp',
                                                           'png', 'PNG']):
            file_ok = True
        if file_ok:
            form.file.data.save('static/img/' + filename)
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        already = False
        if not (exists[0]) and not true_password and teacher_exist and file_ok:
            already = False
            user_model.insert(name, group, user_name, password, teacher,
                              'pupil', filename)
            exists = user_model.exists(user_name, password)
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect("/index")
        elif not (exists[0]) and (true_password or 
                                  not teacher_exist or not file_ok):
            already = False
        else:
            already = True
    return render_template('reg.html', title='Регистрация', form=form,
                           already=already, true_password=true_password,
                           teacher_exist=teacher_exist, file_ok=file_ok)

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    achievements = AchieveModel(db.get_connection()).get_all(session['user_id'])
    achievements.sort(key=lambda x: (x[4], x[1]))
    u_role = False
    name = UsersModel(db.get_connection()).get(session['user_id'])[1]
    group = UsersModel(db.get_connection()).get(session['user_id'])[2]
    user_name = UsersModel(db.get_connection()).get(session['user_id'])[3]
    password = UsersModel(db.get_connection()).get(session['user_id'])[4]
    teacher = UsersModel(db.get_connection()).get(session['user_id'])[5]    
    role = UsersModel(db.get_connection()).get(session['user_id'])[6]
    if role == 'teacher':
        return redirect("/index_teacher")
    return render_template('index.html', username=session['username'],
                           achievements=achievements, name=name, group=group,
                           teacher=teacher,
                           link=url_for('static', filename='img/'+UsersModel(db.get_connection()).get(session['user_id'])[7]))

@app.route('/index_teacher')
def index_teacher():
    if 'username' not in session:
        return redirect('/login')
    role = UsersModel(db.get_connection()).get(session['user_id'])[6]
    if role != 'teacher':
        return redirect('/index')    
    achievements = AchieveModel(db.get_connection()).get_all(session['user_id'])
    achievements.sort(key=lambda x: (x[4], x[1]))
    u_role = False
    name = UsersModel(db.get_connection()).get(session['user_id'])[1]
    user_name = UsersModel(db.get_connection()).get(session['user_id'])[3]
    password = UsersModel(db.get_connection()).get(session['user_id'])[4]  
    role = UsersModel(db.get_connection()).get(session['user_id'])[6]
    all_user = UsersModel(db.get_connection()).get_all()
    users = []
    for user in all_user:
        if user[3] != UsersModel(db.get_connection()).get(session['user_id'])[3]:
            if user[5] == UsersModel(db.get_connection()).get(session['user_id'])[1]:
                users.append((user[0], user[1]))  
    return render_template('index_teacher.html', users=users, name=name,
                           link=url_for('static',
                                        filename='img/'+UsersModel(db.get_connection()).get(session['user_id'])[7]))

@app.route('/index/<int:user_id>')
def users(user_id):
    if 'username' not in session:
        return redirect('/login')
    role = UsersModel(db.get_connection()).get(session['user_id'])[6]
    if role != 'teacher':
        return redirect('/index')
    user = UsersModel(db.get_connection()).get(user_id)
    achievements = AchieveModel(db.get_connection()).get_all(user[0])
    achievements.sort(key=lambda x: (x[4], x[1]))  
    name = user[1]
    group = user[2]
    teacher = user[5]      
    return render_template('users.html', achievements=achievements, name=name,
                           group=group, teacher=teacher,
                           link=url_for('static',
                                        filename='img/'+UsersModel(db.get_connection()).get(user_id)[7]))


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddAchieveForm()
    file_ok = True
    if form.validate_on_submit():
        title = form.title.data
        if title == 'Другое':
            title = form.adittion.data
        content = form.content.data
        filename = secure_filename(form.file.data.filename)
        file_ok = False
        if '.' in filename and (filename.split('.')[1] in ['jpg',
                                                           'JPG', 'bmp',
                                                           'png', 'PNG']):
            file_ok = True
        if not file_ok:
            return render_template('add_achieve.html', title='Добавление новости',
                                       form=form, username=session['username'],
                                       file_ok=file_ok)            
        form.file.data.save('static/img/' + filename)
        nm = AchieveModel(db.get_connection())
        nm.insert(title, content, session['user_id'], filename)
        return redirect("/index")
    return render_template('add_achieve.html', title='Добавление новости',
                           form=form, username=session['username'],
                           file_ok=file_ok)


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = AchieveModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")

@app.route('/delete_pupil/<int:pupil_id>', methods=['GET'])
def delete_pupil(pupil_id):
    if 'username' not in session:
        return redirect('/login')
    role = UsersModel(db.get_connection()).get(session['user_id'])[6]
    if role != 'teacher':
        return redirect('/index')    
    nm = UsersModel(db.get_connection())
    nm.delete(pupil_id)
    return redirect("/index")

@app.route('/image/<int:im>', methods=['GET'])
def image(im):
    if 'username' not in session:
        return redirect('/login')   
    return render_template('image.html',
                           link=url_for('static',
                                        filename='img/'+AchieveModel(db.get_connection()).get(im)[5]))

@app.route('/image_teacher/<int:im>', methods=['GET'])
def image_teacher(im):
    if 'username' not in session:
        return redirect('/login')     
    role = UsersModel(db.get_connection()).get(session['user_id'])[6]
    if role != 'teacher':
        return redirect('/index')
    user_id = AchieveModel(db.get_connection()).get(im)[3]
    return render_template('image_teacher.html',
                           link=url_for('static',
                                        filename='img/'+AchieveModel(db.get_connection()).get(im)[5]), user_id=user_id)

# http://127.0.0.1:8080/reg
@app.route('/reg_teacher', methods=['GET', 'POST'])
def reg_teacher():
    form = RegisterTeacherForm()
    already = False
    true_password = False
    teacher_exist = False
    file_ok = True
    if form.validate_on_submit():
        name = form.name.data
        user_name = form.username.data
        password = form.password.data
        password_agree = form.password_agree.data
        if password != password_agree:
            true_password = True
        teacher_exist = False
        all_user = UsersModel(db.get_connection()).get_all()
        for user in all_user:
            if user[1] == name and user[6] == 'teacher':
                teacher_exist = True
                break
        filename = secure_filename(form.file.data.filename)
        file_ok = False
        if '.' in filename and (filename.split('.')[1] in ['jpg',
                                                           'JPG', 'bmp',
                                                           'png', 'PNG']):
            file_ok = True
        if file_ok:
            form.file.data.save('static/img/' + filename)
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        already = False
        if not (exists[0]) and not true_password and not teacher_exist and file_ok:
            already = False
            user_model.insert(name, '-', user_name, password, '-',
                              'teacher', filename)
            exists = user_model.exists(user_name, password)
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect("/index")
        elif not (exists[0]) and (true_password or teacher_exist or not file_ok):
            already = False
        else:
            already = True
    return render_template('reg_teacher.html', title='Регистрация', form=form,
                           already=already, true_password=true_password,
                           teacher_exist=teacher_exist, file_ok=file_ok)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')