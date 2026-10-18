from flask import Flask, url_for, render_template
from db import get_records, PowerORM, EngineORM
from utils import create_plot

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    data = {'voltage':get_records('voltage',1),
            'power':get_records('power',1),
            'engine':get_records('engine',1),
            'history':get_records('history',1)}
    return render_template('index.html',data=data)


@app.route('/powerhistory',methods=['GET'])
def power_history():
    
    pw = get_records('power',720)
    power = PowerORM(pw)
    plot_url = create_plot(power.timestp,power.power,power.headers['labels'][0],power.headers['units'][0])
    plot_url1 = create_plot(power.timestp,power.phase_angle,power.headers['labels'][1],power.headers['units'][1])
    return render_template('plots.html',data=power.headers,plot_url=[plot_url,plot_url1])

@app.route('/enginehistory',methods=['GET'])
def engine_history():
    eng = get_records('engine',720)
    engine = EngineORM(eng)
    plot_url1 = create_plot(engine.time_stamp,engine.temperature,engine.headers['labels'][0],engine.headers['units'][0])
    plot_url2 = create_plot(engine.time_stamp,engine.oil_pressure,engine.headers['labels'][1],engine.headers['units'][1])
    return render_template('plots.html',data=engine.headers,plot_url=[plot_url1,plot_url2])

@app.route('/debug')
def debug():
    pw = get_records('power',720)
    power = PowerORM(pw)
    return render_template('debug.html',power=power.power)

if __name__ == '__main__':
    

    app.run(debug=True,host='0.0.0.0',port=5000)