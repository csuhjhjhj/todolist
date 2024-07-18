from flask import Flask
from api import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 更改端口为 5001
