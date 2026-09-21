import sqlite3

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
        data = cursor.execute(f"SELECT * FROM {item} ORDER BY id DESC LIMIT {num_records}").fetchone()
    return data
    

