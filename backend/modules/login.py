from modules.database import login as log

class login:
    
    def __init__(self):
        pass

    def login(self , email : str , password : str) -> str | None:
        return log(email=email , password = password)