"""
StudySaarthi Flask Application
Main entry point for the autonomous learning agent application
"""

from flask import Flask, render_template, request, jsonify
import uuid
from agent import StudySaarthiAgent
from utils import (
    load_user_progress,
    save_session,
    get_user_stats,
    format_response_for_frontend,
    validate_topic_input
)
from config import DEBUG, SECRET_KEY, FLASK_ENV

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Store user sessions (in production, use database)
user_sessions = {}


@app.route('/')
def home():
    """
    Render the main homepage
    """
    return render_template('index.html')


@app.route('/api/learn', methods=['POST'])
def learn():
    """
    API endpoint for the learning flow
    
    Receives a topic and runs the autonomous agent cycle:
    - Perception (understand topic)
    - Reasoning (classify topic)
    - Planning (design learning flow)
    - Action (generate content)
    
    Request JSON:
        {
            "topic": "photosynthesis",
            "user_id": "user123" (optional)
        }
    
    Response JSON:
        {
            "success": true,
            "topic": "photosynthesis",
            "category": "science_math",
            "explanation": "...",
            "notes": "...",
            "quiz": "...",
            "next_topics": "..."
        }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Extract topic
        topic = data.get('topic', '').strip()
        user_id = data.get('user_id', str(uuid.uuid4()))  # Generate user ID if not provided
        
        # Validate topic input
        is_valid, error_msg = validate_topic_input(topic)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Create and run agent
        agent = StudySaarthiAgent()
        result = agent.run_full_cycle(topic, user_id)
        
        # Save session
        save_session(user_id, result)
        
        # Format response for frontend
        response = format_response_for_frontend(result)
        
        # Add user_id to response for future use
        response['user_id'] = user_id
        
        return jsonify(response), 200
    
    except Exception as e:
        print(f"Error in /api/learn: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/progress/<user_id>', methods=['GET'])
def get_progress(user_id):
    """
    Get user's learning progress
    
    Parameters:
        user_id: Unique user identifier
    
    Response: Array of past learning sessions
    """
    try:
        progress = load_user_progress(user_id)
        return jsonify({
            'success': True,
            'progress': progress,
            'count': len(progress)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats/<user_id>', methods=['GET'])
def get_stats(user_id):
    """
    Get user's learning statistics
    
    Parameters:
        user_id: Unique user identifier
    
    Response: Dictionary with learning statistics
    """
    try:
        stats = get_user_stats(user_id)
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return jsonify({
        'status': 'healthy',
        'app': 'StudySaarthi',
        'environment': FLASK_ENV
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run Flask development server
    print("=" * 50)
    print("StudySaarthi - Autonomous Learning Agent")
    print("=" * 50)
    print(f"Environment: {FLASK_ENV}")
    print(f"Debug Mode: {DEBUG}")
    print("\nStarting Flask server...")
    print("Visit http://localhost:5000 in your browser")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=DEBUG,
        use_reloader=True
    )
