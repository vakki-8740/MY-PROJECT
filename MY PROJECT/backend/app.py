from flask import Flask, send_from_directory
from config import Config
from routes import api
from models import init_db
import os

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(Config)
    
    # FLOW: routes -> models -> database.db -> utils -> discord
    init_db()
    app.register_blueprint(api, url_prefix='/api')

    # Serve Frontend Files
    @app.route('/user/')
    def serve_user(): return send_from_directory(os.path.join(app.root_path, '../frontend/user'), 'index.html')
    @app.route('/admin/')
    def serve_admin(): return send_from_directory(os.path.join(app.root_path, '../frontend/admin'), 'index.html')

    return app

# backend/app.py ke end mein ye add karein

if __name__ == '__main__':
    create_app().run(debug=True, port=5000)
else:
    # Production mode for Render
    app = create_app()
