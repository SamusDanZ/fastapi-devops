class ValoracionesRepository:
    def get_by_user(self, db, usuario_id: int) -> dict[int, dict[str, object]]:
        cursor = db.cursor()
        cursor.execute(
            "SELECT videojuego_id, puntuacion, comentario FROM usuarios_videojuegos WHERE usuario_id = %s",
            (usuario_id,),
        )
        filas = cursor.fetchall()
        cursor.close()

        puntuaciones: dict[int, dict[str, object]] = {}
        for fila in filas:
            puntuaciones[int(fila[0])] = {
                "puntuacion": int(fila[1]),
                "comentario": fila[2] if fila[2] else ""
            }
        return puntuaciones

    def get_by_user_with_details(self, db, usuario_id: int) -> list[dict[str, object]]:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT v.id, v.nombre, uv.puntuacion, uv.comentario
            FROM usuarios_videojuegos uv
            JOIN videojuegos_v2 v ON v.id = uv.videojuego_id
            WHERE uv.usuario_id = %s
            ORDER BY v.nombre
            """,
            (usuario_id,),
        )
        filas = cursor.fetchall()
        cursor.close()

        resultados: list[dict[str, object]] = []
        for fila in filas:
            resultados.append({
                "videojuego_id": int(fila[0]),
                "videojuego": fila[1],
                "puntuacion": int(fila[2]),
                "comentario": fila[3] if fila[3] else "",
            })
        return resultados

    def upsert_puntuacion(self, db, usuario_id: int, videojuego_id: int, puntuacion: int, comentario: str = "") -> None:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO usuarios_videojuegos (usuario_id, videojuego_id, puntuacion, comentario)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE puntuacion = VALUES(puntuacion), comentario = VALUES(comentario)
            """,
            (usuario_id, videojuego_id, puntuacion, comentario),
        )
        db.commit()
        cursor.close()

    def get_all_with_details(self, db) -> list[dict[str, object]]:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT u.username, v.id, v.nombre, uv.puntuacion, uv.comentario
            FROM usuarios_videojuegos uv
            JOIN usuarios_v2 u ON u.id = uv.usuario_id
            JOIN videojuegos_v2 v ON v.id = uv.videojuego_id
            ORDER BY v.nombre, u.username
            """
        )
        filas = cursor.fetchall()
        cursor.close()

        resultados: list[dict[str, object]] = []
        for fila in filas:
            resultados.append({
                "username": fila[0],
                "videojuego_id": int(fila[1]),
                "videojuego": fila[2],
                "puntuacion": int(fila[3]),
                "comentario": fila[4] if fila[4] else "",
            })
        return resultados

    def get_promedios_por_videojuego(self, db) -> dict[int, float]:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT videojuego_id, AVG(puntuacion) as promedio
            FROM usuarios_videojuegos
            GROUP BY videojuego_id
            """
        )
        filas = cursor.fetchall()
        cursor.close()

        promedios: dict[int, float] = {}
        for fila in filas:
            promedios[int(fila[0])] = round(float(fila[1]), 1)
        return promedios

    def get_by_videojuego(self, db, videojuego_id: int) -> list[dict[str, object]]:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT u.username, uv.puntuacion, uv.comentario
            FROM usuarios_videojuegos uv
            JOIN usuarios_v2 u ON u.id = uv.usuario_id
            WHERE uv.videojuego_id = %s
            ORDER BY uv.puntuacion DESC, u.username
            """,
            (videojuego_id,),
        )
        filas = cursor.fetchall()
        cursor.close()

        resultados: list[dict[str, object]] = []
        for fila in filas:
            resultados.append({
                "username": fila[0],
                "puntuacion": int(fila[1]),
                "comentario": fila[2] if fila[2] else "",
            })
        return resultados

    def get_promedio_videojuego(self, db, videojuego_id: int) -> float | None:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT AVG(puntuacion) as promedio
            FROM usuarios_videojuegos
            WHERE videojuego_id = %s
            """,
            (videojuego_id,),
        )
        fila = cursor.fetchone()
        cursor.close()

        if fila and fila[0]:
            return round(float(fila[0]), 1)
        return None
