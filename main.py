from flask import Flask, send_file, render_template, request, redirect, url_for
from prizepickstransfer import fileGrabber, overUnderCalc, allowed_file
from os.path import exists
import os 

app = Flask(__name__) 
'''
app.secret_key = 'jacksdfs'
app.config['SECRET_KEY'] = 'jacksdfs'
'''
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

def editCSVfile(file):
    data = overUnderCalc('static/files/'+file)
    return data

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
        return redirect(url_for('home'))
        '''
        flash("CSV file doesn't exist. Upload your own file first.", category='error')
        '''

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        path = exists("files/OverUnderDiff.csv")
        file = request.files['file']
        if file and allowed_file(file.filename):
            app.logger.error(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            try:   
                yes = editCSVfile(file.filename)
                yes.to_csv('files/OverUnderDiff.csv', index=False)
                os.remove('static/files/'+file.filename)
                return render_template('prizepicks2.html', tables=[yes.to_html(classes='data', header="true")])
            except Exception as e:
                print(e)
                '''
                flash("Please submit a CSV file that contains columns - [Name] and [fpts]", category='error')
                '''
                dir = 'static/files'
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))
                return redirect(url_for('home'))
        else:
            '''
            flash("Please submit a CSV file that contains columns - [Name] and [fpts]", category='error')
            '''
            if path:
                os.remove('files/OverUnderDiff.csv')
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))
            
'''
@app.route('/prizepicks')
def prizepicks():
    return render_template('prizepicks.html')
'''

if __name__ == '__main__':
    app.debug = True
    app.run()
    
    
