import mysql.connector
from mysql.connector import errorcode

def init_db(app):
    try:
        db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            due_date DATE,
            completed BOOLEAN NOT NULL DEFAULT FALSE
        );
        """)
        db.commit()
    except mysql.connector.Error as err:
        print("Error occurred:", err)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
