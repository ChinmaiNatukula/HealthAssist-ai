from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, bcrypt, jwt
from models import User, Report
from auth import auth_bp
from predict import predict_bp
from chatbot import chatbot_bp
from disease_info import disease_info_bp
from reports import reports_bp
from image_predict import image_predict_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(predict_bp, url_prefix='/api/predict')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chat')
    app.register_blueprint(disease_info_bp, url_prefix='/api/disease')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(image_predict_bp, url_prefix='/api/image-predict')

    # Create DB tables
    with app.app_context():
        db.create_all()

    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'service': 'HealthAssist AI Backend'}, 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
