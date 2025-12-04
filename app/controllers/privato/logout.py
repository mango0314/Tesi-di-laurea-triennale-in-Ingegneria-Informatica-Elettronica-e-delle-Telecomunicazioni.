from flask import Blueprint, session, redirect, make_response

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def home():
    # Invalida la sessione
    session.clear()

    
    response = make_response(redirect('/'))
    

    return response


