import re

def validate_email(email: str):
    email_regex = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if(re.fullmatch(email_regex, email)):
        return True
    else:
        return False

def validate_password(password: str):
    
    if len(password) < 8:
        return False
        
    if not any(char.isdigit() for char in password):
        return False
        
    if not any(char.isupper() for char in password):
        return False
        
    if not any(char.islower() for char in password):
        return False
        
    regexp = re.compile(r"""[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+""")
    if not regexp.search(password):
        return False
    
    return True