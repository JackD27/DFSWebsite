from flask import Flask, send_file, render_template, request, redirect, url_for, flash
from prizepickstransfer import fileGrabber, overUnderCalc, allowed_file
from os.path import exists
import os 

app = Flask(__name__) 
app.secret_key = 'jacksdfs'
app.config['SECRET_KEY'] = 'jacksdfs'

@app.route('/')
def home(): 
    path = exists("files/OverUnderDiff.csv")
    if path:
        os.remove('files/OverUnderDiff.csv')
        return render_template('prizepicks.html')
    else:
        return render_template('prizepicks.html')

@app.route('/download')
def download():
    filePP = fileGrabber()
    filePP.to_csv('PrizePicksData.csv', index = False)
    path = "PrizePicksData.csv"
    return send_file(path, as_attachment=True)
    

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
    try:
        if request.method == 'POST':
            path = exists("files/OverUnderDiff.csv")
            file = request.files['file']
            if file and allowed_file(file.filename):
                newFile = overUnderCalc(file.filename)
            
                newFile.to_csv('files/OverUnderDiff.csv', index=False)
            
                return render_template('prizepicks2.html', tables=[newFile.to_html(classes='data', header="true")])
            else:
                flash("Please submit a CSV file that contains columns - [Name] and [fpts]", category='error')
                if path:
                    os.remove('files/OverUnderDiff.csv')
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('home'))
    
        return redirect(url_for('home'))
    except:
        flash("Rename CSV to ppData.csv in the meantime. :)", category='error')

'''
@app.route('/prizepicks')
def prizepicks():
    return render_template('prizepicks.html')
'''

if __name__ == '__main__':
    app.debug = True
    app.run()
    
    
