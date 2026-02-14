import bcrypt

class User:
    def __init__(self, id: int, username: str, password_hash: str = None, is_admin: bool = False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
    
    def set_password(self, password: str):
        """Encripta la contraseña"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verifica la contraseña"""
        password_bytes = password.encode('utf-8')
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)
