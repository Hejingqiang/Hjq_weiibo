from flask import Blueprint, render_template

wb_bp = Blueprint('weibo', import_name='weibo', url_prefix='/weibo')

@wb_bp.route('/mini/', methods=['get', 'post'])
def base():
    return render_template('mini.html')
