from flask import Blueprint, render_template

cmt_bp = Blueprint('comment', import_name='comment', url_prefix='/cmt')

@cmt_bp.route('/mini/', methods=['get', 'post'])
def base():
    return render_template('mini.html')
