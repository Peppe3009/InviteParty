from flask import Flask, render_template, request, redirect, session, jsonify, current_app
from flask_mail import Message, Mail
from datetime import datetime
import locale
from flask_pymongo import PyMongo
from static.python.functions import *

app = Flask(__name__)
app.config.update(mail_settings)
app.secret_key = KEY
app.config["MONGO_URI"] = "mongodb://localhost:27017/Progetto"
mail = Mail(app)
mongo = PyMongo(app)




@app.route('/', methods=['GET', 'POST'])
def login_view():
    status = 0
    if request.method == 'GET':
        session.pop('nome', None)
        session.pop('cognome', None)
        session.pop('locale', None)
        session.pop('level', None)
        session.pop('email', None)
        session.pop('codice', None)

    if request.method == 'POST':
        email = request.form['email']
        password = codifica(request.form['password'])
        codice = request.form['codice']
        # ricerca in database

        result = mongo.db.users.find_one({"Email": email, "Password": password, "Codice": codice})
        if result is not None:
            session['nome'] = result['Nome']
            session['cognome'] = result['Cognome']
            session['email'] = result['Email']
            session['codice'] = result['Codice']
            session['password'] = result['Password']
            session['level'] = result['Account']

            if result['Account'] == 'Admin':
                return redirect('/AdminProfile')
            elif result['Account'] == 'PR':
                return redirect('/PRProfile')
            else:
                return redirect('/UserProfile')
        else:
            status = 400

    return render_template('LoginPages/LoginPage.html', status=status)


@app.route('/signup', methods=['GET', 'POST'])
def signup_view():
    if request.method == 'POST':

        nome = request.form['nome'].capitalize()
        cognome = request.form['cognome'].capitalize()
        password = codifica(request.form['password'])
        email = request.form['email']
        level = request.form['levelUser']
        locale = request.form['locale']
        codice = stringa_random()
        
        msg = Message(subject='Username per registrazione',
                      recipients=[email],
                      body="Codice univoco di " + nome + " " + cognome + " : " + codice,
                      sender='tecwebprogetto@gmail.com')
        mail.send(msg)

        #  inserimento in database

        mongo.db.users.insert({"Nome": nome,
                               "Cognome": cognome,
                               "Password": password,
                               "Email": email,
                               "Codice": codice,
                               "Account": level,
                               "Locale": locale})
        return redirect('/')

    return render_template('SignUpPages/SignUpPage.html')


@app.route('/PRProfile', methods=['GET', 'POST'])
def pr_profile_view():
    nome = ''
    cognome = ''
    email = ''
    level = ''
    temp = []
    if request.method == 'GET':
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        nome = session['nome']
        cognome = session['cognome']
        email = session['email']
        level = session['level']
        cursor = mongo.db.events.find({"PR": nome + ' ' + cognome}, {"_id:": False})
        for i in cursor:
            giornoEvento = i['giornoEvento']
            giornoEvento = giornoEvento.replace(',', '')
            giornoEvento = datetime.strptime(giornoEvento, '%d %B %Y')
            if giornoEvento > datetime.today():
                temp.append(i['nomeEvento'])
    return render_template('PrPages/PrProfile.html', level=level, nome=nome, cognome=cognome, email=email,
                           eventi=temp)


@app.route('/becomePr', methods=['POST', 'GET'])
def become_pr_view():


    temp = []
    if request.method == 'GET':
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        cursor = mongo.db.events.find({"PR": ""}, {"_id": False})
        for item in cursor:
            giornoEvento = item['giornoEvento']
            giornoEvento = giornoEvento.replace(',', '')
            giornoEvento = datetime.strptime(giornoEvento, '%d %B %Y')
            if giornoEvento > datetime.today():
                temp.append(item)
    return render_template('PrPages/becomePr.html', eventi=temp)


@app.route('/updatePr', methods=['GET', 'POST'])
def update_pr():
    if request.method == 'GET':
        nomeEvento = request.args.get('nomeEvento')
        giornoEvento = request.args.get('giornoEvento')
        mongo.db.events.update_one({"nomeEvento": nomeEvento, "giornoEvento": giornoEvento, "PR": ""},
                                   {"$set": {"PR": session['nome'] + " " + session['cognome']}})
        return jsonify({"status": 200})
    return jsonify({"status": 404})


@app.route('/prenotationsList', methods=['GET', 'POST'])
def prenotations_list_view():
    eventi = []
    if request.method == 'GET':
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        cursor = mongo.db.events.find({"PR": session['nome'] + " " + session['cognome']}, {"_id": False})

        for i in cursor:
            giornoEvento = i['giornoEvento']
            giornoEvento = giornoEvento.replace(',', '')
            giornoEvento = datetime.strptime(giornoEvento, '%d %B %Y')
            if giornoEvento > datetime.today():
                eventi.append(i['nomeEvento'])
        return render_template('PrPages/prenotationsList.html', risultato=eventi)
    return render_template('PrPages/prenotationsList.html', risultato=eventi)


@app.route('/getPrenotations', methods=['GET', 'POST'])
def get_prenotations():
    all_prenotations = []
    if request.method == 'GET':
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        nomeEvento = request.args.get('nomeEvento')
        cursor = mongo.db.prenotazioni.find({"nomeEvento": nomeEvento}, {"_id": False})
        for prenotazione in cursor:
            giornoEvento = prenotazione['giornoEvento']
            giornoEvento = giornoEvento.replace(',', '')
            giornoEvento = datetime.strptime(giornoEvento, '%d %B %Y')
            if giornoEvento > datetime.today():
                all_prenotations.append(prenotazione)
        return jsonify(all_prenotations)


@app.route('/AdminProfile', methods=['GET', 'POST'])
def admin_profile_view():
    nome = ''
    cognome = ''
    email = ''
    level = ''
    temp = []
    if request.method == 'GET':
        nome = session['nome']
        cognome = session['cognome']
        email = session['email']
        codice = session['codice']
        level = session['level']
        result = mongo.db.users.find({"Email": email, "Codice": codice})

        for i in result:
            temp.append(i['Locale'])

    return render_template('AdminPages/adminProfile.html', level=level, nome=nome, cognome=cognome, email=email,
                           locali=temp)


@app.route('/addEvent', methods=['GET', 'POST'])
def add_event_view():
    status = 0
    temp = []
    if request.method == 'GET':
        email = session['email']
        codice = session['codice']
        result = mongo.db.users.find({"Email": email, "Codice": codice})
        for i in result:
            temp.append(i['Locale'])
    if request.method == 'POST':
        nomeEvento = request.form['nomeEvento']
        giornoEvento = request.form['giornoEvento']
        oraEvento = request.form['inizioEvento']
        tipoEvento = request.form['tipoEvento']
        numeroInvitati = request.form['numeroInvitati']
        nomeLocale = request.form['nomeLocale']
        mongo.db.events.insert({
            "nomeEvento": nomeEvento,
            "giornoEvento": giornoEvento,
            "oraEvento": oraEvento,
            "tipoEvento": tipoEvento,
            "numeroInvitati": numeroInvitati,
            "nomeLocale": nomeLocale,
            "PR": ""
        })
        status = 200
    return render_template('AdminPages/addEvent.html', risultato=temp, status=status)


@app.route('/addLocale', methods=['GET', 'POST'])
def add_locale():
    status = 0
    if request.method == 'POST':
        newLocale = request.form['newlocale']
        mongo.db.users.insert({"Nome": session['nome'],
                               "Cognome": session['cognome'],
                               "Password": session['password'],
                               "Email": session['email'],
                               "Codice": session['codice'],
                               "Account": session['level'],
                               "Locale": newLocale})

        status = 200
    return render_template('AdminPages/addLocale.html', status=status)


@app.route('/handleEvent', methods=['GET', 'POST'])
def handle_event():
    temp = []
    if request.method == 'GET':
        email = session['email']
        codice = session['codice']
        result = mongo.db.users.find({"Email": email, "Codice": codice})
        for i in result:
            temp.append(i['Locale'])
    return render_template('AdminPages/handleEvent.html', risultato=temp)


@app.route('/getEvent', methods=['GET', 'POST'])
def get_event():
    temp = []
    if request.method == 'GET':
        nomeLocale = request.args.get('nomeLocale')
        result = mongo.db.events.find({"nomeLocale": nomeLocale}, {"_id": False})
        for value in result:
            temp.append(value)
        return jsonify(temp)


@app.route("/showStatistic", methods=['GET', 'POST'])
def show_statistic_view():
    temp = []
    if request.method == 'GET':
        email = session['email']
        codice = session['codice']
        result = mongo.db.users.find({"Email": email, "Codice": codice})
        for i in result:
            temp.append(i['Locale'])
    return render_template("AdminPages/showStatistic.html", risultato=temp)


@app.route("/getData", methods=['GET', 'POST'])
def get_data():
    eventi = []
    prenotazioni = []
    if request.method == 'GET':
        nomeLocale = request.args.get('nomeLocale')
        result = mongo.db.events.find({'nomeLocale': nomeLocale}, {"giornoEvento": 1, "nomeEvento": 1, "_id": False})
        for i in result:
            eventi.append(i)
        for evento in eventi:
            newresult = mongo.db.prenotazioni.find(
                {"nomeEvento": evento['nomeEvento'], "giornoEvento": evento['giornoEvento']}, {"_id": False})
            prenotazioni.append(newresult.count())

        return jsonify(eventi, prenotazioni)


@app.route('/UserProfile', methods=['GET', 'POST'])
def user_profile_view():
    nome = ''
    cognome = ''
    email = ''
    level = ''
    if request.method == 'GET':
        nome = session['nome']
        cognome = session['cognome']
        email = session['email']
        level = session['level']

    return render_template('UserPages/UserProfile.html', nome=nome, cognome=cognome, email=email, level=level)


@app.route('/showEvent', methods=['GET', 'POST'])
def show_events():
    all_events = []
    not_booked = []
    if request.method == 'GET':

        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        results = mongo.db.events.find()
        for result in results:
            giornoEvento = result['giornoEvento']
            giornoEvento = giornoEvento.replace(',', '')
            giornoEvento = datetime.strptime(giornoEvento, '%d %B %Y')
            if giornoEvento > datetime.today():
                all_events.append(result)

        for event in all_events:
            # cursor = tutte le prenotazioni di uno specifico evento
            cursor = mongo.db.prenotazioni.find({"nomeEvento": event['nomeEvento']}, {"_id": False})
            if cursor.count() == 0:
                not_booked.append(event)
            elif cursor.count() < int(event['numeroInvitati']):
                cont = 0
                for item in cursor:
                    # se non c'è prenotazione per il mio user, faccio vedere l'evento
                    if (item['nomeInvitato'] != session['nome']) or (item['cognomeInvitato'] != session['cognome']):
                        # tengo traccia di quante prenotazioni non sono a mio nome
                        cont += 1
                if cont == cursor.count():
                    # se è uguale al numero di elementi vuol dire che la mia prenotazione non c'è
                    # mostro l'evento
                    not_booked.append(event)
    return render_template("UserPages/showEvent.html", not_booked=not_booked)


@app.route('/add_prenotation', methods=['POST', 'GET'])
def add_prenotation():
    if request.method == 'GET':
        nomeEvento = request.args.get('nomeEvento')
        nomeLocale = request.args.get('nomeLocale')
        giornoEvento = request.args.get('giornoEvento')
        oraEvento = request.args.get('oraEvento')
        mongo.db.prenotazioni.insert({
            "nomeEvento": nomeEvento,
            "nomeLocale": nomeLocale,
            "giornoEvento": giornoEvento,
            "oraEvento": oraEvento,
            "nomeInvitato": session['nome'],
            "cognomeInvitato": session['cognome'],
        })
        return jsonify({"status": 200})
    return jsonify({"status": 404})


@app.route('/allPrenotations', methods=['GET', 'POST'])
def all_prenotations_view():
    all_prenotations = []
    if request.method == 'GET':
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        cursor = mongo.db.prenotazioni.find({'nomeInvitato': session['nome'], 'cognomeInvitato': session['cognome']},
                                            {'_id': False})
        for item in cursor:
            giornoEvento = item['giornoEvento']
            giornoEvento = giornoEvento.replace(',', '')
            giornoEvento = datetime.strptime(giornoEvento, '%d %B %Y')
            if datetime.today() < giornoEvento:
                all_prenotations.append(item)
    return render_template('UserPages/allPrenotations.html', prenotazioni=all_prenotations)

@app.route('/sw.js', methods=['GET'])
def sw():
    return app.send_static_file('sw.js')
if __name__ == '__main__':
    app.run(debug=True)
