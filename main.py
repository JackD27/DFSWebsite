from flask import Flask, send_file, render_template, request
from prizepickstransfer import fileGrabber

app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/download')
def download():
    file = fileGrabber()
    file.to_csv('PrizePicksData.csv', index = False)
    path = "PrizePicksData.csv"
    return send_file(path, as_attachment=True)

@app.route('/prizepicks')
def prizepicks():
    return render_template('prizepicks.html')

if __name__ == '__main__':
    app.run(debug=True)
