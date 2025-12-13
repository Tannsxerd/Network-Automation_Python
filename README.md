# Network-Automation_Python
project นี้เกี่ยวกับการทำ **Automation Backup config** จาก **router cisco Catalyst8000** บน **cisco devnet sandbox ios xe** โดยใช้  **python libraly netmiko** และแจ้งเตือน **notifications** ไปยัง **discord** 

## 🐍 Python Concepts Applied
This project demonstrates the practical application of several core Python concepts:

### 1. External Libraries & API Interaction
- **Netmiko:** Used for handling low-level SSH connections to network devices, managing shells, and executing CLI commands programmatically.
- **Requests:** Used to interact with RESTful APIs (Discord Webhook) via HTTP POST requests to send real-time notifications.
- **Python-dotenv:** Implemented to manage environment variables, ensuring sensitive credentials are not hard-coded.

### 2. File Handling & OS Operations
- **Context Managers (`with open`):** Used for safely opening and writing configuration files, ensuring file resources are closed automatically after operations.
- **OS Module:** Utilized `os.path` and `os.makedirs` for cross-platform path management and automatic directory creation.

### 3. Error Handling & Robustness
- **Try-Except Blocks:** Implemented comprehensive error handling to catch connection timeouts or authentication failures, preventing script crashes and triggering alert notifications instead.

### 4. Data Structures & String Manipulation
- **Dictionaries:** Used to store and organize device parameters (host, username, password) efficiently.
- **f-strings:** Extensively used for dynamic string formatting (e.g., generating filenames with timestamps, formatting notification messages).

### 5. Modularization
- **Functions & Imports:** Separated the notification logic into a distinct module (`notifications.py`) and imported it into the main script to promote code reusability and clean architecture.
## Cisco Devnet sandbox ios xe
เป็น sandbox ที่มีการ pre-configured network  ไว้ให้ access เพื่อ ทดลองและพัฒนา project เล็กๆ โดย sand-box environment ที่ใช้ในโปรเจคนี้ผมเลือกเป็น Catalyst 8000 Always-On Sandbox โดยมีปัจจัยการพิจรณาดังนี้ 
<แปะรูปจาก cisco sandbox overview>

## python libraly netmiko
Network automation to screen-scraping devices is primarily concerned with gathering output from show commands and with making configuration changes. สรุปได้ว่า เราจะใช้ netmiko  ในการ ดึงข้อมูล output ออกมาจาก router ของเรา โดย ssh เข้าอุปกรณ์ แล้วใส่ลง variable เพื่อนำไปใช้ต่อไป 

### Example
**1)Define device**

    Cat8000v  = {
        'device_type': 'cisco_ios',
        'host':  'CISCO_HOST',
        'username':'CISCO_USERNAME',
        'password' : 'CISCO_PASSWORD',
        'port' :  'CISCO_PORT'
    }
   
**2)เชื่อมต่อDevice** 

    from netmiko import ConnectHandler
    #Unpacking the dictionary to connect to the device
    connection = ConnectHandler(**cat8000v)
    
**3)ส่ง command เข้า router แล้ว เก็บลง output variable**

    output = connection.send_command('show running-config')
    print(output)

## ระบบ backup

### 1)จัดการ ชื่อของไฟล์ที่จะ backup config เพิ่ม time-stamp โดยใช้ datetime

      #use datetime to create time_stamp for our backup config
        backup_time  = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
      #create file.txt with  our time-stamp that we created
        file_name = f"{backup_time}_config.txt"
        
### 2)จัดการBackup path  เพื่อ write ลง file
  โดยนำ output ที่ได้มา save ลง  backup path  โดยมี ส่วนนี้ในการจัดการ path เพื่อที่จะ **back_up** หากไม่มี **directory** ก็จะทำการสร้างขึ้นมาให้อัตโนมัติ
  
     #find current path 
	     current_dir = os.path.dirname(os.path.abspath(__file__))
     #join backup to current directory
	     save_folder = os.path.join(current_dir, "backup")
     #makedir if it does not exit and hadling error with exist_ok 
	     os.makedirs(save_folder, exist_ok=True)
	 #full path of directory to save txt file
	     full_path = os.path.join(save_folder, file_name)
### 3)เปิดไฟล์แล้ว write config ลง file ที่สร้างไว้

      #open file.txt for writing config output 
      with open(full_path, "w") as f:
         f.write(output)
## Discord Notifications
เมื่อ back up จะมีการส่ง notifications ไปยัง discord โดยใช้ web-hook 
ใช้ request เพื่อส่ง post ไปยัง endpoint web-hook 
มีการ handling error โดยใช้ try,except เมื่อ ส่ง data ไม่สำเร็จ
    
    def sendmessage(message):
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if not webhook_url:
            print("ไม่พบ DISCORD_WEBHOOK_URL ใน .env")
            return
        data = {'content': message}
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print("Discord Notification sent!")
            else:
                print(f"Discord status: {response.status_code}")
        except Exception as e:
            print(f"Failed to send Discord: {e}")
