from datetime import datetime

def create_user(name, email, password_hash):
    return {
        "name": name,
        "email": email,
        "password": password_hash,
        "created_at": datetime.utcnow()
    }
