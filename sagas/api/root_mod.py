from sanic.response import json
from sanic import Blueprint

bp = Blueprint('root_blueprint')

@bp.route('/')
async def bp_root(request):
    return json({'mod': 'info_stack'})

