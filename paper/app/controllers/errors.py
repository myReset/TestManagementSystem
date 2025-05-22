from flask import render_template, request, jsonify


def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(400)
    def bad_request(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'Bad Request', 'message': str(e)})
            response.status_code = 400
            return response
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'Forbidden', 'message': str(e)})
            response.status_code = 403
            return response
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'Not Found', 'message': str(e)})
            response.status_code = 404
            return response
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'Internal Server Error', 'message': str(e)})
            response.status_code = 500
            return response
        return render_template('errors/500.html'), 500 