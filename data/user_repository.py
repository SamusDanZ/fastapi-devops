from domain.user import User


class UserRepository:

    def get_all(self, db) -> list[User]:
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, is_admin FROM usuarios_v2")
        filas = cursor.fetchall()
        usuarios: list[User] = list()
        for fila in filas:
            usuario = User(fila[0], fila[1], fila[2], bool(fila[3]))
            usuarios.append(usuario)
        cursor.close()
        return usuarios

    def get_by_username(self, db, username: str) -> User | None:
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, is_admin FROM usuarios_v2 WHERE username = %s", (username,))
        fila = cursor.fetchone()
        cursor.close()
        
        if fila:
            return User(fila[0], fila[1], fila[2], bool(fila[3]))
        return None

    def get_by_id(self, db, id: int) -> User | None:
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, is_admin FROM usuarios_v2 WHERE id = %s", (id,))
        fila = cursor.fetchone()
        cursor.close()
        
        if fila:
            return User(fila[0], fila[1], fila[2], bool(fila[3]))
        return None

    def insertar_usuario(self, db, usuario: User) -> None:
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios_v2 (username, password_hash, is_admin) VALUES (%s, %s, %s)", 
                      (usuario.username, usuario.password_hash, usuario.is_admin))
        db.commit()
        cursor.close()

    def actualizar_usuario(self, db, usuario: User) -> None:
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios_v2 SET username = %s, password_hash = %s, is_admin = %s WHERE id = %s", 
                      (usuario.username, usuario.password_hash, usuario.is_admin, usuario.id))
        db.commit()
        cursor.close()

    def borrar_usuario(self, db, id: int) -> None:
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios_v2 WHERE id = %s", (id,))
        db.commit()
        cursor.close()
