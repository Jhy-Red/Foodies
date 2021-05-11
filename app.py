#!/usr/bin/python3

#Import
from flask import Flask, render_template


#Definition APP
app = Flask(__name__,static_url_path='/static')

#Route definition
@app.route('/', methods=['GET', 'POST'])
def home(): 
    return render_template('home.html') 

@app.route('/prediction-picture', methods=['GET', 'POST'])
def prediction_photo(): 
    return render_template('prediction-photo.html') 

@app.route('/about')
def about(): 
    return render_template('about.html')



#Launch Flask
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    