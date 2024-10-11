from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config.from_object('config.Config')
    
    # Importa e registra as rotas
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
