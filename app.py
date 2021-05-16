#!/usr/bin/python3

#Import
from flask import Flask, render_template,request
from ressources import prediction as pred
from ressources import tools as tools
from  ressources import SQL_APP as SQL_APP

#Definition APP
app = Flask(__name__,static_url_path='/static')

#Stockage serveur
UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#stockage des images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#Route definition
@app.route('/', methods=['GET', 'POST'])
def home(): 
    return render_template('home.html') 

@app.route('/prediction-picture', methods=['GET', 'POST'])
def prediction_photo(): 
    if request.method == "POST":
        image = request.files['image_users']
        filename = tools.saves_pictures(UPLOAD_FOLDER,image,app)
        resultat = pred.prediction(filename,model =1)
        resultat = tools.translate(resultat, dest = 'fr', short = True)

        apports_cols,apports_row = tools.request_food_local(recherche = resultat,flask = True)
        
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
    