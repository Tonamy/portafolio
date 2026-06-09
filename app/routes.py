from flask import Blueprint, request, jsonify, render_template

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return render_template('chat.html')

@main_blueprint.route('/chat', methods=['POST'])
def chat_handler():
    from app.bot.engine import process_message
    request_data = request.get_json() or {}
    user_message = request_data.get('message', '').strip()
    step = request_data.get('step', 1)
    data = request_data.get('data', {})
    reply, next_step, updated_data = process_message(user_message, step, data)
    return jsonify({'reply': reply, 'next_step': next_step, 'data': updated_data})
