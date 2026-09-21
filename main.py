from flask import Flask, url_for, render_template
from db import get_records
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    data = {'voltage':get_records('voltage',1),
            'power':get_records('power',1),
            'engine':get_records('engine',1),
            'history':get_records('history',1)}
    
    return render_template('index.html',data=data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)