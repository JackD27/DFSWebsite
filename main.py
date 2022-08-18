from flask import Flask, send_file, render_template, request, redirect, url_for, flash
from prizepickstransfer import fileGrabber, overUnderCalc, allowed_file
from os.path import exists
import os 
import pandas as pd

app = Flask(__name__) 
'''
app.secret_key = 'jacksdfs'
app.config['SECRET_KEY'] = 'jacksdfs'
'''
UPLOAD_FOLDER = 'static/files/'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def home(): 
    path = exists("files/OverUnderDiff.csv")
    if path:
        os.remove('files/OverUnderDiff.csv')
        return render_template('prizepicks.html')
    else:
        return render_template('prizepicks.html')

@app.route('/download', methods = ['GET', 'POST'])
def download():
    if request.method == 'POST':
        sport = request.form.get("pp-sport")
        if len(sport) < 1:
            sport = None
        else:
            sport = sport.upper()
        filePP = fileGrabber(sport)
        filePP.to_csv('PrizePicksData.csv', index = False)
        path = "PrizePicksData.csv"
        return send_file(path, as_attachment=True)
    return send_file(path, as_attachment=True)

@app.route('/test')
def test():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = str(os.listdir(cwd))
    str1 = 'Current dir:' +cwd+' Files:' +files
    return str1
    

@app.route('/downloadOU')
def downloadOU():
    path = exists("files/OverUnderDiff.csv")
    if path:
        return send_file('files/OverUnderDiff.csv', as_attachment=True)
    else:
        flash("CSV file doesn't exist. Upload your own file first.", category='error')
        return redirect(url_for('home'))

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        path = exists("files/OverUnderDiff.csv")
        file = request.files['file']
        if file and allowed_file(file.filename):
            try:   
                yes = pd.read_csv(file)
                yes = overUnderCalc(yes)
                yes.to_csv('files/OverUnderDiff.csv', index=False)
                return render_template('prizepicks2.html', tables=[yes.to_html(classes='data', header="true")])
            except Exception as e:
                print(e)
                flash("Please submit a CSV file that contains columns - [Name] and [fpts]", category='error')
                
                return redirect(url_for('home'))
        else:
            flash("Please submit a CSV file that contains columns - [Name] and [fpts]", category='error')
            if path:
                os.remove('files/OverUnderDiff.csv')
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))
    return 'Ok'
'''
@app.route('/prizepicks')
def prizepicks():
    return render_template('prizepicks.html')
'''

if __name__ == '__main__':
    app.debug = True
    app.run()
    
    
