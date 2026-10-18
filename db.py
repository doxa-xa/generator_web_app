import sqlite3
import datetime

def create_db_tables():
    with sqlite3.connect('generator.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS voltage (id INTEGER PRIMARY KEY,vol_h_l1,vol_h_l2,vol_h_l3,vol_l_l1,vol_l_l2,vol_l_l3, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS power (id INTEGER PRIMARY KEY,curr_l1,curr_l2,curr_l3,ph_angle1,ph_angle2,ph_angle3,pf,ps,freq,power,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS engine (id INTEGER PRIMARY KEY, speed, battery, charge, oil_pressure, temp, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, num_starts, run_hrs,run_min,run_sec)")
        conn.commit()

def insert_record(data):
    with sqlite3.connect('generator.db') as conn:
        cursor = conn.cursor()
        cursor.execute(data.insert_query)
        conn.commit()

def get_records(item:str,num_records:int):
    """
    data from the generator is inserted every 10 seconds
    period parameter: current record will be 1, last hour will be 360 
    """
    with sqlite3.connect('generator.db') as conn:
        cursor = conn.cursor()
        data = cursor.execute(f"SELECT * FROM {item} ORDER BY id DESC LIMIT {num_records}").fetchall()
    return data
    

class PowerORM:

    __id = []
    __curr1 = []
    __curr2 = []
    __curr3 = []
    __angle1 = []
    __angle2 = []
    __angle3 = []
    __pf = []
    __ps = []
    __freq = []
    __pow = []
    __tstp = []
    __headers = {'labels':['Output Power','Phase angle function'],
                'units':['kW','cos(φ)'],
                'title':'Power'}

    def __init__(self,data):
        self.data = data
        for pk, curr1,curr2,curr3,angle1,angle2,angle3,pf,ps,freq,pow,timestamp in data:
            self.__id.append(pk)
            self.__curr1.append(curr1)
            self.__curr2.append(curr2)
            self.__curr3.append(curr3)
            self.__angle1.append(angle1)
            self.__angle2.append(angle2)
            self.__angle3.append(angle3)
            self.__pf.append(pf)
            self.__ps.append(ps)
            self.__freq.append(freq)
            self.__pow.append(pow)
            self.__tstp.append(datetime.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"))

    @property
    def headers(self):
        return self.__headers

    @property
    def power(self) -> list:
        return self.__pow

    @property
    def timestp(self) -> list:
        return self.__tstp

    @property
    def phase_angle(self) -> list:
        return self.__pf

class EngineORM:
    __id = []
    __speed = []
    __bat = []
    __charge = []
    __oilp = []
    __temp = []
    __tmstp = []
    __headers = {
        'labels':['Temperature','Oil Pressure'],
        'units':['°C','kPa'],
        'title':'Engine'
    }


    def __init__(self,data):
        for pk,sp,bat,chrg,oilp,tmp,timestp in data:
            self.__id.append(pk)
            self.__speed.append(sp)
            self.__bat.append(bat)
            self.__charge.append(chrg)
            self.__oilp.append(oilp)
            self.__temp.append(tmp)
            self.__tmstp.append(datetime.datetime.strptime(timestp,"%Y-%m-%d %H:%M:%S"))

    @property
    def temperature(self):
        return self.__temp

    @property
    def oil_pressure(self):
        return self.__oilp

    @property
    def time_stamp(self):
        return self.__tmstp

    @property
    def headers(self):
        return self.__headers