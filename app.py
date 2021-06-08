#!/usr/bin/python3

#Import
#Main
from flask import Flask, render_template,request,redirect, flash
#Login
from flask_login import LoginManager,login_user,logout_user,current_user
from ressources.userdata import User
#PY
from ressources import prediction as pred
from ressources import tools as tools
from  ressources import SQL_APP as SQL_APP

#Definition APP
app = Flask(__name__,static_url_path='/static')

secret_key_file=open("/media/jhy/46AE-6494/Projet/id.txt","r")
secret_key=secret_key_file.readlines()
secret_key_file.close()
app.secret_key = secret_key[0]

#Definition Log
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.ID = user_id
    return user
    #return User.get_id(user_id)

#Stockage serveur
UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#stockage des images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Route definition
@app.route('/', methods=['GET', 'POST'])
def home(): 
    
    if request.method == "POST":
        imc_form = request.form
        taille = int(imc_form["taille"])
        poids = int(imc_form['poids'])
        imc = round((poids)/((taille/100)**2),2)

        if current_user.is_authenticated:
            user_id = current_user.ID
            SQL_APP.save_imc(user_id = str(user_id),imc = imc)
            return render_template('home logged.html',imc = imc) 
        else :
            return render_template('home.html', imc=imc)
    
    else :
        if current_user.is_authenticated:
            return render_template("home logged.html")
        else :    

            return render_template('home.html') 


@app.route('/connection', methods=['GET', 'POST'])
def loggin(): 
    if request.method == "POST":
        details = request.form
        adresse_mail = details['adresse_mail']
        password = details['mot_de_passe']

        if adresse_mail == "" or password == "" :
            error =  "Veuillez saisir un utilisateur ou mots de passe"
            return render_template('login.html',error=error)

        try :
            id_user,adresse_mail_base,password_base,pseudo = SQL_APP.connection_user(adresse_mail,password)
            user = User()
            user.ID = id_user
            login_user(user,force= False)
            return render_template('welcome.html',pseudo = pseudo)

        except :
            error =  "Utilisateur inconnu ou mot de passe incorecte"
            return render_template('login.html',error=error)

    else :
        return render_template('login.html')

@app.route('/deconnection', methods=['GET', 'POST'])
def logout():
    logout_user()

    return  redirect ("/")


@app.route('/prediction-picture', methods=['GET', 'POST'])
def prediction_photo(): 
    if request.method == "POST":
        image = request.files['image_users']
        filename = tools.saves_pictures(UPLOAD_FOLDER,image,app)
        resultat = pred.prediction(filename,model =1)
        resultat = tools.translate(resultat, dest = 'fr', short = True)

        apports_cols,apports_row = tools.request_food_local(recherche = resultat,flask = True)

        resultat = "Votre photo semble contenir  :" + resultat
        
        return render_template('from_picture.html', pred = resultat, apports_cols = apports_cols, apports_row = apports_row )
    else :
        return render_template('from_picture.html')

@app.route('/prediction-picture2', methods=['GET', 'POST'])
def prediction_photo2(): 
    if request.method == "POST":
        image = request.files['image_users']
        filename = tools.saves_pictures(UPLOAD_FOLDER,image,app)
        resultat = pred.prediction(filename,model =2)
        resultat = tools.translate(resultat, dest = 'fr', short = True)

        apports_cols,apports_row = tools.request_food_local(recherche = resultat,flask = True)

        resultat = "Votre photo semble contenir  :" + resultat
        
        return render_template('from_picture.html', pred = resultat, apports_cols = apports_cols, apports_row = apports_row )
    else :
        return render_template('from_picture.html')


@app.route('/inscription',methods=['GET', 'POST'])
def inscription(): 
    if request.method == "POST":
        details = request.form
        adresse_mail = details['adresse_mail']
        pseudo = details['pseudo']
        password = details['mot_de_passe']
        SQL_APP.creation_user(MAIL = adresse_mail, USERNAME = pseudo, PASSWORD = password, hash = True)

        return render_template('inscription_success.html')
    else :
        return render_template('inscription.html')


@app.route('/about')
def about(): 
    return render_template('about.html')

#Launch Flask
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    