from flask import Flask
from flask_wtf.csrf import CSRFProtect

import config
from apps.front import bp as front_bp
from exts import db

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 初始化测试环境配置
    app.register_blueprint(front_bp)
    db.init_app(app)
    csrf.init_app(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
