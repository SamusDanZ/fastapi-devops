from domain.model.Alumno import Videojuegos


class VideojuegosRepository:

    def get_all(self, db) -> list[Videojuegos]:
        cursor = db.cursor()

        cursor.execute("SELECT id, nombre FROM videojuegos_v2")

        filas = cursor.fetchall()
        videojuegos: list[Videojuegos] = list()
        for fila in filas:
            videojuego = Videojuegos(fila[0], fila[1])
            videojuegos.append(videojuego)
        cursor.close()

        return videojuegos

    def existe_nombre(self, db, nombre: str) -> bool:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM videojuegos_v2 WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0] > 0

    def insertar_videojuego(self, db, videojuego: Videojuegos) -> bool:
        if self.existe_nombre(db, videojuego.nombre):
            return False
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO videojuegos_v2 (nombre) VALUES (%s)", (videojuego.nombre,))
        db.commit()
        cursor.close()
        return True

    def actualizar_videojuego(self, db, videojuego: Videojuegos) -> None:
        cursor = db.cursor()

        cursor.execute("UPDATE videojuegos_v2 SET nombre = %s WHERE id = %s", (videojuego.nombre, videojuego.id))

        db.commit()
        cursor.close()

    def get_by_id(self, db, id: int) -> Videojuegos | None:
        cursor = db.cursor()

        cursor.execute("SELECT id, nombre FROM videojuegos_v2 WHERE id = %s", (id,))
        fila = cursor.fetchone()
        cursor.close()

        if fila:
            return Videojuegos(fila[0], fila[1])
        return None

    def borrar_videojuego(self, db, id: int) -> None:
        cursor = db.cursor()

        cursor.execute("DELETE FROM videojuegos_v2 WHERE id = %s", (id,))

        db.commit()
        cursor.close()
