from flask import Flask, send_file, render_template
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

if __name__ == '__main__':
    app.run(debug=True)
