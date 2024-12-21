from modules.database.user_operations import insert_user

from modules.database.user_operations import is_username_taken , is_email_taken , is_phone_number_taken 

class register:
    def register(self, user_name : str, user_email : str, user_password : str, user_phone : str) -> dict:
        """Registers a new user, handling potential errors."""
        
        errors : dict 
        errors = {}  

        if is_username_taken(username=user_name):
            errors["validationName"] = "Username already taken"
        if is_email_taken(email=user_email):
            errors["validationEmail"] = "Email address already registered"
        if is_phone_number_taken(phone_number=user_phone):
            errors["validationphoneNumber"] = "Phone number already in use"

        if errors:  
            return errors  


        try:
            insert_user(user_name, user_email, user_password, user_phone)
            return {"success": True}  
        
        except Exception as e:
            return {"success": False, "error": str(e)} 

