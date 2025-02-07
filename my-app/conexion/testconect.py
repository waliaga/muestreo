# Conectar a la base de datos
conn = connectionBD()

if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("Versión de PostgreSQL:", db_version)
    cursor.close()
    conn.close()