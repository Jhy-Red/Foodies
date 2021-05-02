#!/usr/bin/python3

#Import
from flask import Flask, render_template


#Definition APP
app = Flask(__name__,static_url_path='/static')



#Route definition
@app.route('/', methods=['GET', 'POST'])
def home(): 
    return render_template('home.html')



#Launch Flask
if __name__ == "__main__":
    app.run(debug=True)
    