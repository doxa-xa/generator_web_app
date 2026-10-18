import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class Voltage: 
    def __init__(self,data):
        self.vol_h_l1 = int(data[0])
        self.vol_h_l2 = int(data[1])
        self.vol_h_l3 = int(data[2])
        self.vol_l_l1 = int(data[3])
        self.vol_l_l2 = int(data[4])
        self.vol_l_l3 = int(data[5])

    @property
    def insert_query(self):
        return f"""INSERT INTO voltage (vol_h_l1,vol_h_l2,vol_h_l3,vol_l_l1,vol_l_l2,vol_l_l3)
        VALUES ({self.vol_h_l1},{self.vol_h_l2},{self.vol_h_l3},{self.vol_l_l1},{self.vol_l_l2},{self.vol_l_l3})
        """

class Power:
    def __init__(self,data):
        self.curr_l1 = data[0]
        self.curr_l2 = data[1]
        self.curr_l3 = data[2]
        self.ph_angle1 = data[3]
        self.ph_angle2 = data[4]
        self.ph_angle3 = data[5]
        self.pf = data[6]
        self.ps = data[7]
        self.freq = data[8]
        self.power = data[9]

    @property
    def insert_query(self):
        return f"""INSERT INTO power (curr_l1,curr_l2,curr_l3,ph_angle1,ph_angle2,ph_angle3,pf,ps,freq,power)
        VALUES ({self.curr_l1},{self.curr_l2},{self.curr_l3},{self.ph_angle1},{self.ph_angle2},{self.ph_angle3},{self.pf},{self.ps},{self.freq},{self.power})"""
    

class Engine:
    def __init__(self,data):
        self.speed, self.battery, self.charge, self.oil_pressure, self.temp = data

    @property
    def insert_query(self):
        return f"""INSERT INTO engine (speed, battery, charge, oil_pressure, temp)
        VALUES ({self.speed},{self.battery},{self.charge},{self.oil_pressure},{self.temp})"""

class History:
    def __init__(self,data):
        self.num_starts, self.run_hrs, self.run_min, self.run_sec = data

    @property
    def insert_query(self):
        return f"""INSERT INTO history (num_starts, run_hrs,run_min,run_sec)
        VALUES ({self.num_starts},{self.run_hrs},{self.run_min},{self.run_sec})"""

def create_plot(time_axis, unit_axis,label,units):
    fig = Figure(figsize=(10,5),dpi= 100)
    ax = fig.subplots()

    x = time_axis
    y = unit_axis

    ax.plot(x,y,marker='o',markersize=3,color='purple',linestyle='-',linewidth=1)
    ax.set_title(f'History {label} [{units}]', fontsize=14, pad=15)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel(units, fontsize=12)
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    fig.autofmt_xdate(rotation=45)

    ax.grid(True, linestyle='--',alpha=0.5)

    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    
    plot_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return plot_url