from flask import Blueprint, request, jsonify
from enhanced_ai_agent import EnhancedAIAgent

chat_bp = Blueprint('chat', __name__)
ai_agent = EnhancedAIAgent()

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        history = data.get('history', [])
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get AI response
        response = ai_agent.chat_response(message, context={'history': history})
        
        # Prepare actions based on intent
        actions = []
        if response['intent'] == 'analyze':
            actions.append({
                'type': 'analyze',
                'data': {}
            })
        elif response['intent'] == 'template':
            actions.append({
                'type': 'template',
                'data': response.get('context', {}).get('template_data', {})
            })
        elif response['intent'] == 'insights':
            actions.append({
                'type': 'insight',
                'data': ai_agent.get_performance_metrics()
            })
        
        # Update learning
        ai_agent.update_learning(
            state={'message': message, 'history': history},
            action={'response': response['response'], 'actions': actions},
            reward=0  # Will be updated based on user interaction
        )
        
        return jsonify({
            'response': response['response'],
            'actions': actions
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/api/chat/feedback', methods=['POST'])
def chat_feedback():
    try:
        data = request.json
        message_id = data.get('message_id')
        feedback = data.get('feedback')
        
        if message_id is None or feedback is None:
            return jsonify({'error': 'Missing message_id or feedback'}), 400
        
        # Update AI learning with feedback
        ai_agent.update_learning(
            state={'message_id': message_id},
            action={'type': 'response'},
            reward=1 if feedback == 'positive' else -1
        )
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        print(f"Error in feedback endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500
