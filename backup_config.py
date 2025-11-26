#import libraly
import datetime;
from netmiko import ConnectHandler
import os
from dotenv import load_dotenv

#load env 
load_dotenv()

#Define device 
Cat8000v  = {
    'device_type': 'cisco_ios',
    'host':  os.getenv('CISCO_HOST'),
    'username': os.getenv('CISCO_USERNAME'),
    'password' : os.getenv('CISCO_PASSWORD'),
    'port' :  os.getenv('CISCO_PORT')
}

# establish connection with device 
connection = ConnectHandler(**Cat8000v)

#send cmd to router for show config
output =  connection.send_command('show running-config')

#use datetime to create time_stamp for our backpu config
backup_time  = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")

#create file.txt with  our time-stamp that we created
file_name = f"{backup_time}_config.txt"

#adjust path for save at backup directory
save_folder = "D:\\pythonWork\\NetworkAutomation\\backup"
full_path = os.path.join(save_folder, file_name)


#open file.txt for writing config output 
with open(full_path, "w") as f:
    f.write(output)

print(f"{backup_time} config.txt is saved successfully" )

#end connection session
connection.disconnect()



# with open(f"{backup_time} config.txt") as f:
#     print(f.read())