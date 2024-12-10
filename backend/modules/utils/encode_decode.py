import bcrypt 



def hash_password(password : str) -> str:
    """Hashes a password using bcrypt."""

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))  #rounds=12 is a good default. Adjust as needed for performance/security tradeoff.

    return hashed_password.decode('utf-8') # Decode back to string for storage



def check_password(password : str, hashed_password : str) -> bool:
    """Checks if a password matches a hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
