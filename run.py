from controller import fetch_generator_data
from utils import Voltage, Power, Engine, History
from db import create_db_tables, insert_record
import datetime
import time
from bot import send_notification

create_db_tables()
now = datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:S")
while True:
    registers = fetch_generator_data()
    if len(registers) == 0:
        for attempt in range(1,4):
            send_notification(f"Опитвам автоматично да възстановя връзката с контролера... Опит:{attempt}")
            with open("run_log.txt","a") as log:
                time.sleep(10)
                log.write(f"{now} | Retrying attempt {attempt}...")
                log.write("\n")
                registers = fetch_generator_data()
                if len(registers) != 0:
                    break
                    
    voltage = Voltage(tuple(registers[6:12]))

    power = Power(tuple([registers[12]/10,
                        registers[13]/10,
                        registers[14]/10,
                        registers[86],
                        registers[87],
                        registers[88],
                        registers[15]/100,
                        registers[19]/10,
                        registers[17]/10,
                        registers[18]/10]))
    
    engine = Engine(tuple([registers[39],
                          registers[37]/10,
                          registers[38]/10,
                          registers[35],
                          registers[33]]))
    
    history = History(tuple([registers[65],registers[71],registers[72],registers[73]]))
    
    insert_record(voltage)
    insert_record(power)
    insert_record(engine)
    insert_record(history)
    time.sleep(10)
