"""
Utility functions for StudySaarthi application
"""

import json
import os
from datetime import datetime
from config import PROGRESS_FILE, SESSIONS_FILE


def load_user_progress(user_id):
    """
    Load user's learning progress from JSON storage
    
    Args:
        user_id: Unique user identifier
        
    Returns:
        List of user's past learning sessions
    """
    if not os.path.exists(PROGRESS_FILE):
        return []

    try:
        with open(PROGRESS_FILE, 'r') as f:
            all_progress = json.load(f)
        
        # Filter progress for specific user
        user_progress = [p for p in all_progress if p.get('user_id') == user_id]
        return user_progress
    
    except Exception as e:
        print(f"Error loading progress: {str(e)}")
        return []


def save_session(user_id, session_data):
    """
    Save a learning session to JSON storage
    
    Args:
        user_id: Unique user identifier
        session_data: Dictionary containing session information
    """
    session = {
        'user_id': user_id,
        'timestamp': datetime.now().isoformat(),
        'data': session_data
    }

    try:
        # Read existing sessions
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, 'r') as f:
                all_sessions = json.load(f)
        else:
            all_sessions = []

        # Append new session
        all_sessions.append(session)

        # Save back to file
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(all_sessions, f, indent=2)

        return True
    
    except Exception as e:
        print(f"Error saving session: {str(e)}")
        return False


def get_user_stats(user_id):
    """
    Get learning statistics for a user
    
    Args:
        user_id: Unique user identifier
        
    Returns:
        Dictionary with user statistics
    """
    progress = load_user_progress(user_id)
    
    # Count topics by category
    category_count = {
        'science_math': 0,
        'history_gk': 0,
        'general': 0
    }
    
    topics_learned = []
    
    for session in progress:
        category = session.get('category')
        if category in category_count:
            category_count[category] += 1
        
        topic = session.get('topic')
        if topic and topic not in topics_learned:
            topics_learned.append(topic)
    
    stats = {
        'total_sessions': len(progress),
        'category_breakdown': category_count,
        'topics_learned': topics_learned,
        'total_topics': len(topics_learned)
    }
    
    return stats


def format_response_for_frontend(agent_result):
    """
    Format agent output for frontend consumption
    
    Args:
        agent_result: Dictionary from agent.run_full_cycle()
        
    Returns:
        Formatted dictionary ready for JSON response
    """
    if 'error' in agent_result:
        return {
            'success': False,
            'error': agent_result['error']
        }
    
    return {
        'success': True,
        'topic': agent_result.get('topic'),
        'category': agent_result.get('category'),
        'explanation': agent_result.get('explanation'),
        'notes': agent_result.get('notes'),
        'quiz': agent_result.get('quiz'),
        'next_topics': agent_result.get('next_topic'),
        'timestamp': agent_result.get('timestamp'),
        'mode': agent_result.get('mode', 'openai')
    }


def validate_topic_input(topic):
    """
    Validate user's topic input
    
    Args:
        topic: User input string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not topic or not isinstance(topic, str):
        return False, "Topic cannot be empty"
    
    if len(topic.strip()) < 2:
        return False, "Topic must be at least 2 characters long"
    
    if len(topic.strip()) > 100:
        return False, "Topic must be less than 100 characters"
    
    # Check for any malicious patterns
    dangerous_chars = ['<', '>', '{', '}', ';', '--']
    if any(char in topic for char in dangerous_chars):
        return False, "Invalid characters in topic"
    
    return True, ""
