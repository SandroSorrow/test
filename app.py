from flask import Flask, render_template, redirect, url_for, flash

import sys
from project import form, functions
from project.form import *
from time import ctime
from config import Config
from xml.etree import ElementTree

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def start():
    return redirect(url_for("home"))


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/home_id<login>')
def home_log(login):
    return render_template("home.html", login=login)


@app.route('/registration', methods=["get", "post"])
def registration():
    reg_key = 'KoF-200928'
    file = 'project/knights.xml'
    form_reg = RegistrationForm()
    if form_reg.validate_on_submit():
        key = form_reg.key.data
        email = form_reg.e_mail.data
        password1 = form_reg.password1.data
        password2 = form_reg.password2.data
        if password1 == password2:
            password = password1
            if key == reg_key:
                rank = '1'
            else:
                rank = '0'
            login = functions.registration(email, password, rank, file)
            return redirect(url_for('new_account', login=login, rank=rank))
        else:
            return render_template("notifications.html",
                                   notification="Different passwords.",
                                   back='registration',)

    return render_template("forms.html",
                           form=form_reg,
                           title="Sign Up",
                           desc_h3="Sign Up",
                           desc_h3p=["Create new account",
                                     "For Knights of Favonius:",
                                     "Take registration key from Grandmaster or Acting Grand Master directly."],
                           botlinks={'log_in': ["If you already have account, please ", "log in."]},
                           )


@app.route('/account/new/id<login>', methods=["get", "post"])
def new_account(login):
    file = 'project/knights.xml'
    profile = {}
    form_new = NewAccForm()
    if form_new.validate_on_submit():
        name = form_new.name.data
        profile['name'] = name
        profile['surname'] = form_new.surname.data
        profile['sex'] = form_new.sex.data
        month = form_new.month.data
        day = form_new.day.data
        profile['birthday'] = month + ' ' + str(day) + 'th'
        profile['post'] = form_new.post.data
        profile['vision'] = form_new.vision.data
        profile['weapon'] = form_new.weapon.data
        profile['description'] = form_new.description.data
        profile['namepic'] = name + '.png'
        functions.new_account(login, profile, file)
        return render_template('notifications.html',
                               notification='You are successfully registratied!',
                               back='account', login=login,)

    return render_template('edit_account.html',
                           form=form_new,
                           title="Profile",
                           desc_h3="Profile",
                           desc_h3p=["Welcome to the Knights of Favonius Headquarters!",
                                     "Please, fill your profile."],
                           )


@app.route('/login', methods=["GET", "POST"])
def log_in():
    email = ""
    password = ""
    form_log = LogInForm()
    if form_log.validate_on_submit():
        email = form_log.e_mail.data
        password = form_log.password.data
        login = functions.login(email, password, file='project/knights.xml')
        if login == False:
            err = "Incorrect e-mail or password."
            return render_template("error.html", message=err, back='log_in')
        else:
            return redirect(url_for("account", login=login))

    return render_template("forms.html",
                           form=form_log,
                           email=email,
                           password=password,
                           title="Log In",
                           desc_h3="Please, log in.",
                           # desc_h3p=["Please, log in."],
                           botlinks={'registration':
                                     ["Or create new account: ", "Sign Up"]
                                     },
                           )


@app.route('/account/id<login>')
def account(login):
    file = 'project/knights.xml'
    profile = functions.account(login, file)
    rank = profile['rank']
    name = profile['name']
    sex = profile['sex']
    surname = profile['surname']
    birthday = profile['birthday']
    post = profile['post']
    vision = profile['vision']
    weapon = profile['weapon']
    description = profile['description']
    namepic = profile['namepic']
    visionpic = profile['visionpic']
    return render_template("account.html",
                           login=login,
                           rank=rank,
                           name=name,
                           sex=sex,
                           surname=surname,
                           birthday=birthday,
                           post=post,
                           vision=vision,
                           weapon=weapon,
                           about=description,
                           namepic=namepic,
                           visionpic=visionpic)


@app.route('/account/id<login>/edit', methods=["get", "post"])
def edit_account(login):
    file = 'project/knights.xml'
    form_new = NewAccForm()
    profile = functions.account(login, file)
    rank = profile['rank']
    if form_new.validate_on_submit():
        name = form_new.name.data
        profile['name'] = name
        profile['surname'] = form_new.surname.data
        profile['sex'] = form_new.sex.data
        month = form_new.month.data
        day = form_new.day.data
        profile['birthday'] = month + ' ' + str(day) + 'th'
        profile['post'] = form_new.post.data
        profile['vision'] = form_new.vision.data
        profile['weapon'] = form_new.weapon.data
        profile['description'] = form_new.description.data
        profile['namepic'] = name + '.png'
        functions.new_account(login, profile, file)
        return render_template("notifications.html",
                               notification='Profile updated.',
                               back='account', login=login, rank=rank)

    return render_template("edit_account.html",
                           form=form_new,
                           login=login,
                           rank=rank,
                           title="Notification",
                           notification="Page in progress",
                           back='home')


@app.route('/account/id<login>/message', methods=["GET", "POST"])
def message(login):
    heroes = {"jean@monstadt.tw": "Jean",
              "klee@monstadt.tw": "Klee",
              "keya@monstadt.tw": "Kaeya",
              "lisa@monstadt.tw": "Lisa",
              "amber@monstadt.tw": "Amber",
              "eula@monstadt.tw": "Eula",
              "diluc@monstadt.tw": "Diluc",
              "venti@monstadt.tw": "Venti",
              "barbara@monstadt.tw": "Barbara",
              "rosaria@monstadt.tw": "Rosaria",
              "diona-meow@monstadt.tw": "Diona",
              "bennet@monstadt.tw": "Bennet",
              "noelle@monstadt.tw": "Noelle",
              "nona_nagistus@monstadt.tw": "Mona",
              "sucrose@monstadt.tw": "Sucrose",
              "albedo@monstadt.tw": "Albedo",
              }
    form_message = MessageForm()
    if form_message.validate_on_submit():
        from_name = form_message.from_name.data
        from_email = form_message.from_email.data
        to_mail = form_message.to_mail.data
        message = form_message.message.data
        with open('logs/citizen_messages.txt', 'a', encoding='utf-8') as in_mess:
            if to_mail in heroes:
                address = heroes[to_mail] + ' <' + to_mail + '>'
            else:
                address = to_mail
            in_mess.write('\n' + str(ctime()) + '\n')
            in_mess.write('From: ' + str(from_name) + ' <' + from_email + '>\n')
            in_mess.write('To: ' + address + '\n')
            in_mess.write('Message:\n' + str(message) + '\n')
        print("New message received.")
        sys.stdout.write('New message received.')
        # flash("Ваше сообщение для " + knights[to_name] + " отправлено.")
        notification = 'Your message for {} sent.'.format(to_mail)
        return render_template("notifications.html", login=login,
                               title="Notification",
                               notification=notification,
                               back='message')

    return render_template("forms.html", login=login,
                           form=form_message,
                           title="Message",
                           desc_h3="Send message",
                           desc_h3p=["to any person in Teywat."],
                           )


@app.route('/account/id<login>/incident', methods=["GET", "POST"])
def incident(login):
    incident_id = {0: "Commission",
                   1: "Wild animals",
                   2: "Bandits",
                   3: "Abyss mages",
                   4: "The Fatui",
                   5: "Anomaly",
                   }
    form_incident = IncidentForm()
    file = 'project/incidents.xml'
    if form_incident.validate_on_submit():
        from_name = form_incident.from_name.data
        place = form_incident.place.data
        id_ = form_incident.incident_type.data
        incident_description = form_incident.incident_description.data
        num_id = functions.task(id_, place, from_name, incident_description, file=file)
        date_ = ' '.join(functions.my_time())
        print('\n>>> New Incident! <<<\tID:', num_id, place, id_, incident_id[id_], '\n')
        with open('logs/incidents.txt', 'a', encoding='utf-8') as inc:
            inc.write('\n' + 'ID: ' + num_id + ' - ' + str(id_) + '-' + incident_id[id_] + ' ' + date_ + '\n')
            inc.write(from_name + '\n' + place + '\n' + incident_description + '\n')
        notification = 'Incident ID: ' + num_id + '.'
        return render_template("notifications.html",
                               title="Notification",
                               notification=notification,
                               back='home')

    return render_template("forms.html",
                           login=login,
                           form=form_incident,
                           title="New incident",
                           desc_h3="New incident",
                           desc_h3p=["If you have problems or witnessed an incident, please fill out the form below.",
                                     "The Knights will receive your message and deal with it."],
                           )


@app.route('/account/id<login>/incident/check', methods=["GET", "POST"])
def check_incident(login):
    id_ = ''
    form_check = CheckForm()
    if form_check.validate_on_submit():
        id_ = form_check.incident_id.data
        return redirect(url_for("check", id_=id_, login=login,))

    return render_template("forms.html",
                           login=login,
                           id=id_,
                           form=form_check,
                           title="Check incident",
                           desc_h3="Check incident status",
                           desc_h3p=["Here you can check the status of your request.",
                                     "Enter incident ID below."],
                           )


@app.route('/account/id<login>/incident/check/incident_<id_>')
def check(login, id_):
    response = functions.check(id_, file='project/incidents.xml')
    print('ID', id_, response)
    notification = 'Commission {} status: {}'.format(id_, response)
    return render_template("notifications.html",
                           login=login,
                           title="Status",
                           notification=notification,
                           back='check_incident')


@app.route('/account/id<login>/missions', methods=['get', 'post'])
def missions(login):
    form_mission = MissionsForm()
    if form_mission.validate_on_submit():
        status = form_mission.status.data
        return redirect(url_for('mission_list', login=login, status=status))

    return render_template("forms.html",
                           login=login,
                           form=form_mission,
                           title="Missions",
                           desc_h3="Missions",
                           desc_h3p=["Chose mission status to search.",
                                     ],
                           )


@app.route('/account/id<login>/missions/status_<status>', methods=['get', 'post'])
def mission_list(login, status):
    file = 'project/incidents.xml'
    mission = functions.missions(status, file)
    if mission:
        print('Mission list received.')
        # for i in mission:
        #     print('{' + i + ': ', mission[i], '}', sep='')
    else:
        print('No response.')
    status_string = {'0': "Not complete",
                     '1': "Complete",
                     '2': "Need support",
                     '3': "All",
                     }
    return render_template('missions.html', login=login,
                           status=status,
                           mission=mission,
                           title="Missions",
                           backlink='missions',
                           desc_h3="{} missions".format(status_string[status]),
                           desc_h3p=[""],
                           notification='',
                           back='missions')


@app.route('/account/id<login>/missions/stat_<status>/report<inc_id>', methods=['get', 'post'])
def reports(login, status, inc_id):
    file = 'project/incidents.xml'
    k_file = 'project/knights.xml'
    form_rep = ReportForm()
    if form_rep.validate_on_submit():
        new_status = form_rep.status.data
        upd_report = form_rep.report.data
        functions.report(inc_id, new_status, login, upd_report, file, k_file)
        return render_template('notifications.html', login=login, status=status,
                               notification='Report sent.',
                               back='mission_list',)

    return render_template("forms.html", login=login, status=status,
                           form=form_rep,
                           title="Report",
                           desc_h3="Mission {} report form.".format(inc_id),
                           desc_h3p=["",
                                     ],
                           )


@app.route('/<name>')
def template(name):
    if name == 'notify':
        return render_template("notifications.html",
                               title="Notification",
                               notification="Test notification page",
                               back='home')
    elif name == 'error':
        return render_template("error.html",
                               message="Test error page",
                               back='home')
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run()
