# app/controllers/commenti_api.py

from flask import Blueprint, request, jsonify, current_app
from app.models.commento.CommentoDAO import CommentoDAO

commenti_api_bp = Blueprint('commenti_api', __name__)

@commenti_api_bp.route('/api/commenti/<int:scontro_id>', methods=['GET'])
def list_commenti(scontro_id):
    current_app.logger.debug(f"[debug] /api/commenti called scontro_id={scontro_id} args={dict(request.args)}")

    """
    Restituisce commenti paginati per uno scontro.
    Query params:
      - page (int, default=1)
      - per_page (int, default=10, max=50)
    Response JSON:
      { ok: True, page, per_page, total, items: [{id, nome, created_at, contenuto}, ...] }
    Nota: created_at viene formattato come "HH:MM - GG/MM/AAAA"
    """
    try:
        # parametri di paginazione
        page = max(1, int(request.args.get('page', 1)))
        per_page = min(50, max(1, int(request.args.get('per_page', 10))))

        # usa il metodo paginato del DAO (lo hai aggiunto)
        items, total = CommentoDAO.get_by_scontro_paginated(scontro_id, page=page, per_page=per_page)

        # serializza gli oggetti Commento in dict
        serialized = []
        for c in items:
            # created_at: se presente, formatta come "HH:MM - GG/MM/AAAA"
            created_at_raw = getattr(c, 'created_at', None)
            if created_at_raw:
                try:
                    created_at_str = created_at_raw.strftime('%H:%M - %d/%m/%Y')
                except Exception:
                    created_at_str = str(created_at_raw)
            else:
                created_at_str = ''

            serialized.append({
                'id': getattr(c, 'id', None),
                'nome': getattr(c, 'nome', '') or '',
                'created_at': created_at_str,
                'contenuto': getattr(c, 'contenuto', '') or ''
            })

        return jsonify({
            'ok': True,
            'page': page,
            'per_page': per_page,
            'total': int(total or 0),
            'items': serialized
        })
    except Exception as e:
        current_app.logger.exception("Errore in /api/commenti/<scontro_id>")
        return jsonify({'ok': False, 'error': 'server error'}), 500
