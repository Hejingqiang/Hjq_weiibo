from flask import Blueprint, render_template

user_bp = Blueprint('user',import_name='user',url_prefix='/user')

@user_bp.route('/base/',methods=['get','post'])
def base():
    return render_template('base.html')


