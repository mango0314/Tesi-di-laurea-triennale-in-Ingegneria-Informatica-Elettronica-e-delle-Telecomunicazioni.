from datetime import datetime, date, time, timedelta
import os
import importlib
from flask import Flask, g
from flask_mysqldb import MySQL
from flask_wtf.csrf import generate_csrf
from flask_wtf import CSRFProtect
import config
import secrets

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = 'smash'

    mysql.init_app(app)

    app.config.setdefault('SECRET_KEY', os.environ.get('SECRET_KEY', secrets.token_urlsafe(32)))
    app.config.setdefault('MAX_CONTENT_LENGTH', 5 * 1024 * 1024) 
    upload_folder = os.path.join(app.instance_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder

    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


    csrf = CSRFProtect()
    csrf.init_app(app)
    

    # Registra automaticamente tutti i blueprint nella cartella controllers
    controllers_dir = os.path.join(os.path.dirname(__file__), 'controllers')
    for root, dirs, files in os.walk(controllers_dir):
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__'):
                # Costruisci il nome del modulo, es: app.controllers.privato.privato
                rel_path = os.path.relpath(os.path.join(root, filename), controllers_dir)
                module_name = "app.controllers." + rel_path.replace(os.sep, ".")[:-3]
                module = importlib.import_module(module_name)
                # Cerca una variabile che termina con _bp (es: index_bp)
                for attr in dir(module):
                    if attr.endswith('_bp'):
                        blueprint = getattr(module, attr)
                        app.register_blueprint(blueprint)

    @app.template_filter('date_it')
    def date_it(value):
        """Restituisce giorno mese_italiano anno, es. 22 luglio 2025"""
        if isinstance(value, (datetime,date)):
            # %d = giorno, %B = nome mese, %Y = anno
            return value.strftime('%d/%m/%Y')
        return value

    @app.template_filter('time_it')
    def time_it(value):
        """
        Gestisce:
          - datetime: estrae .time()
          - time: usa direttamente
          - timedelta: converte in ore e minuti
        """
        if isinstance(value, datetime):
            t = value.time()
            return t.strftime('%H:%M')
        if isinstance(value, time):
            return value.strftime('%H:%M')
        if isinstance(value, timedelta):
            total_secs = int(value.total_seconds())
            ore = total_secs // 3600
            minuti = (total_secs % 3600) // 60
            return f"{ore:02d}:{minuti:02d}"
        return value
    
    @app.before_request
    def set_csp_nonce():
        g.csp_nonce = secrets.token_urlsafe(16)

    @app.context_processor
    def inject_nonce():
        return {
                    'csp_nonce': getattr(g, 'csp_nonce', ''),
                    'csrf_token_value': generate_csrf()
                }
    @app.after_request
    def set_security_headers(response):
        nonce = getattr(g, 'csp_nonce', '')
        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
            "img-src 'self' https: data: blob:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    return app
