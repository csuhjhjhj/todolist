from flask import Blueprint, request, jsonify
import mysql.connector
from config import Config
from flask import abort
from datetime import datetime

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/todos', methods=['GET', 'POST'])
def handle_todos():
    db = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            data = request.json
            cursor.execute(
                "INSERT INTO todos (title, description, due_date, completed) VALUES (%s, %s, %s, %s)",
                (data['title'], data['description'], data['due_date'], data['completed'])
            )
            db.commit()
            new_id = cursor.lastrowid  # 获取新插入记录的ID
            cursor.execute("SELECT * FROM todos WHERE id = %s", (new_id,))
            new_todo = cursor.fetchone()  # 获取新添加的记录
            return jsonify(new_todo), 201  # 返回新记录的详细信息

        elif request.method == 'GET':
            cursor.execute("SELECT * FROM todos")
            todos = cursor.fetchall()
            return jsonify(todos)

    finally:
        cursor.close()
        db.close()


@api_blueprint.route('/todos/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_todo(id):
    db = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = db.cursor()

    try:
        if request.method == 'PUT':
            data = request.json
            print(f"Received data: {data}")  # 添加这行来查看接收到的数据
            # 确保所有字段都在 JSON 数据中
            if 'title' not in data or 'description' not in data or 'due_date' not in data or 'completed' not in data:
                return jsonify({"error": "Missing data in request"}), 400

            try:
                due_date = datetime.strptime(data['due_date'], '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d')
            except ValueError as ve:
                print(f"Date conversion error: {ve}")
                return jsonify({"error": "Invalid date format"}), 400

            cursor.execute(
                "UPDATE todos SET title = %s, description = %s, due_date = %s, completed = %s WHERE id = %s",
                (data['title'], data['description'], due_date, data['completed'], id)
            )
            db.commit()
            return jsonify({"message": "Todo updated"})

        elif request.method == 'DELETE':
            cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
            db.commit()
            return jsonify({"message": "Todo deleted"})

    except KeyError as ke:
        print(f"Missing key in data: {ke}")
        db.rollback()
        return jsonify({"error": str(ke)}), 400
    except Exception as e:
        print(f"General error: {e}")
        db.rollback()
        return jsonify({"error": "Server error"}), 500
    finally:
        cursor.close()
        db.close()