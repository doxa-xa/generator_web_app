class Voltage: 
    def __init__(self,data):
        self.vol_h_l1 = data[0]
        self.vol_h_l2 = data[1]
        self.vol_h_l3 = data[2]
        self.vol_l_l1 = data[3]
        self.vol_l_l2 = data[4]
        self.vol_l_l3 = data[5]

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
