def connection():
    import requests
    import time
    activ = True
    while activ:
        try:
            r = requests.get('https://www.google.com')
            activ = not r.status_code == 200
        except Exception:
            time.sleep(2.0)
            print('Connection ERORR')


connection()
