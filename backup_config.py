#import libraly
import datetime;
from netmiko import ConnectHandler
import os
from dotenv import load_dotenv
from notifications import sendmessage
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
try:
    # establish connection with device 
    connection = ConnectHandler(**Cat8000v)

    #send cmd to router for show config
    output =  connection.send_command('show running-config')

    #use datetime to create time_stamp for our backup config
    backup_time  = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")

    #create file.txt with  our time-stamp that we created
    file_name = f"{backup_time}_config.txt"

    #find current path 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #join backup to current directory
    save_folder = os.path.join(current_dir, "backup")
    #makedir if it does not exit and hadling error with exist_ok 
    os.makedirs(save_folder, exist_ok=True)
    #full path of directory to save txt file
    full_path = os.path.join(save_folder, file_name)

    #open file.txt for writing config output 
    with open(full_path, "w") as f:
        f.write(output)

    #for discord notifications 
    msg_success = f"✅ Backup Completed! File: {file_name}"
    sendmessage(msg_success)

    #end connection session
    connection.disconnect()
except Exception as e:
    print(f"Error occurred: {e}")
    msg_error = f"Backup Failed!\nError: {str(e)}"
    sendmessage(msg_error)


