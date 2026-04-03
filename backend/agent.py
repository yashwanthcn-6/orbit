"""
StudySaarthi Autonomous Learning Agent
Core agent logic for perception, reasoning, planning, and action
"""

import json
import os
from datetime import datetime
import openai
from openai import OpenAI
from config import (
    OPENAI_API_KEY,
    TOPIC_CATEGORIES,
    MODEL_CONFIG,
    PROGRESS_FILE
)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def _fallback_response(section, topic, category):
    """Fallback content when OpenAI quota is exhausted or API call fails."""
    fallback_templates = {
        'explanation': f"Temporary fallback: A quick learner-friendly summary for '{topic}' in {category}.",
        'notes': f"Temporary fallback notes for {topic}: key points and simple bullet list (API quota might be exhausted).",
        'quiz': f"Fallback quiz: 3 simple conceptual questions for {topic}.",
        'next_topic': f"Fallback next topics: 1) related topic A, 2) related topic B, 3) related topic C."
    }
    return fallback_templates.get(section, f"Fallback content for {section}.")


class StudySaarthiAgent:
    """
    Autonomous Learning Agent that:
    - Perceives: Understands user's study topic
    - Reasons: Classifies the topic into categories
    - Plans: Designs a learning workflow
    - Acts: Generates explanations, notes, quiz, and next steps
    - Adapts: Customizes response based on topic category
    """

    def __init__(self):
        self.topic = None
        self.category = None
        self.user_id = None
        self.learning_flow = {}

    def perceive(self, user_input):
        """
        PERCEPTION STEP: Understand and validate user's topic
        Input: Raw user input (study topic)
        Output: Cleaned topic string
        """
        # Clean and normalize user input
        self.topic = user_input.strip().lower()
        print(f"[PERCEIVE] Understood topic: {self.topic}")
        return self.topic

    def reason(self):
        """
        REASONING STEP: Classify the topic into one of three categories
        Input: Topic string
        Output: Category classification (science_math, history_gk, or general)
        """
        # Convert topic to lowercase for keyword matching
        topic_lower = self.topic.lower()

        # Score each category based on keyword matches
        scores = {
            'science_math': 0,
            'history_gk': 0,
            'general': 0
        }

        # Match keywords to categories
        for category, config in TOPIC_CATEGORIES.items():
            for keyword in config['keywords']:
                if keyword in topic_lower:
                    scores[category] += 1

        # Determine category
        if scores['science_math'] > 0 and scores['science_math'] >= max(scores['history_gk'], scores['general']):
            self.category = 'science_math'
        elif scores['history_gk'] > 0 and scores['history_gk'] >= max(scores['science_math'], scores['general']):
            self.category = 'history_gk'
        else:
            self.category = 'general'

        print(f"[REASON] Classified topic into: {self.category}")
        return self.category

    def plan(self):
        """
        PLANNING STEP: Design a customized learning workflow
        Input: Topic category
        Output: Learning flow structure tailored to category
        """
        # Customize the learning plan based on category
        if self.category == 'science_math':
            self.learning_flow = {
                'order': ['explanation', 'examples', 'notes', 'quiz'],
                'explanation_style': 'technical',
                'examples_count': 3,
                'quiz_questions': 5,
                'focus': 'concepts and formulas'
            }
        elif self.category == 'history_gk':
            self.learning_flow = {
                'order': ['timeline', 'explanation', 'key_points', 'quiz'],
                'explanation_style': 'narrative',
                'examples_count': 2,
                'quiz_questions': 4,
                'focus': 'historical context and significance'
            }
        else:  # general
            self.learning_flow = {
                'order': ['overview', 'explanation', 'notes', 'quiz'],
                'explanation_style': 'conversational',
                'examples_count': 2,
                'quiz_questions': 3,
                'focus': 'practical understanding'
            }

        print(f"[PLAN] Designed learning flow: {self.learning_flow['order']}")
        return self.learning_flow

    def act(self):
        """
        ACTION STEP: Generate learning content using OpenAI API
        Input: Topic, category, and learning flow
        Output: Dictionary with explanation, notes, quiz, and next topic suggestion
        """
        try:
            result = {
                'topic': self.topic,
                'category': self.category,
                'explanation': self._generate_explanation(),
                'notes': self._generate_notes(),
                'quiz': self._generate_quiz(),
                'next_topic': self._suggest_next_topic(),
                'timestamp': datetime.now().isoformat()
            }
            
            print("[ACT] Generated all learning content")
            return result

        except Exception as e:
            print(f"[ACT] Error generating content: {str(e)}")
            return {
                'error': f"Failed to generate content: {str(e)}",
                'topic': self.topic
            }

    def _generate_explanation(self):
        """Generate detailed explanation of the topic using OpenAI"""
        prompt = f"""
        Explain the topic "{self.topic}" in a clear, beginner-friendly way.
        Category: {self.category}
        
        Make it engaging and easy to understand. Use simple language.
        Keep it concise but comprehensive (2-3 paragraphs).
        """

        try:
            response = client.chat.completions.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert educator creating learning content for students."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=MODEL_CONFIG['max_tokens']
            )
            return response.choices[0].message.content.strip()

        except (openai.RateLimitError, openai.APIError, openai.AuthenticationError) as e:
            print(f"[ACT-FALLBACK] Explanation generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('explanation', self.topic, self.category)
        except Exception as e:
            print(f"[ACT-ERROR] Explanation generation general error: {str(e)}")
            return _fallback_response('explanation', self.topic, self.category)


    def _generate_notes(self):
        """Generate structured study notes using OpenAI"""
        prompt = f"""
        Create concise study notes for "{self.topic}" using the following format:
        
        1. Key Concepts (3-4 bullet points)
        2. Important Points (3-4 bullet points)
        3. Examples or Applications (2-3 items)
        4. Remember (1-2 memory tips or mnemonics)
        
        Make it scannable and easy to memorize.
        """

        try:
            response = client.chat.completions.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert at creating study notes and guides."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=MODEL_CONFIG['max_tokens']
            )
            return response.choices[0].message.content.strip()

        except (openai.RateLimitError, openai.APIError, openai.AuthenticationError) as e:
            print(f"[ACT-FALLBACK] Notes generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('notes', self.topic, self.category)
        except Exception as e:
            print(f"[ACT-ERROR] Notes generation general error: {str(e)}")
            return _fallback_response('notes', self.topic, self.category)


    def _generate_quiz(self):
        """Generate interactive quiz questions using OpenAI"""
        num_questions = self.learning_flow.get('quiz_questions', 3)
        
        prompt = f"""
        Create {num_questions} quiz questions for the topic "{self.topic}".
        For each question, provide:
        - The question
        - 4 answer options (A, B, C, D)
        - The correct answer (single letter)
        - Brief explanation
        
        Format each question clearly and number them 1-{num_questions}.
        Make questions progressive (easy to hard).
        """

        try:
            response = client.chat.completions.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator with clear formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=MODEL_CONFIG['max_tokens']
            )
            return response.choices[0].message.content.strip()

        except (openai.RateLimitError, openai.APIError, openai.AuthenticationError) as e:
            print(f"[ACT-FALLBACK] Quiz generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('quiz', self.topic, self.category)
        except Exception as e:
            print(f"[ACT-ERROR] Quiz generation general error: {str(e)}")
            return _fallback_response('quiz', self.topic, self.category)


    def _suggest_next_topic(self):
        """Suggest related next topics for continuation of learning"""
        prompt = f"""
        Based on the topic "{self.topic}", suggest 3 related topics that a student should learn next.
        
        List them as:
        - Topic name (brief description)
        
        Make them progressive (easy to advanced).
        """

        try:
            response = client.chat.completions.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert at designing learning paths."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()

        except (openai.RateLimitError, openai.APIError, openai.AuthenticationError) as e:
            print(f"[ACT-FALLBACK] Next topic generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('next_topic', self.topic, self.category)
        except Exception as e:
            print(f"[ACT-ERROR] Next topic generation general error: {str(e)}")
            return _fallback_response('next_topic', self.topic, self.category)


    def save_progress(self, user_id):
        """Save user's learning progress to JSON file"""
        self.user_id = user_id
        
        progress_data = {
            'user_id': user_id,
            'topic': self.topic,
            'category': self.category,
            'timestamp': datetime.now().isoformat(),
            'session_data': self.learning_flow
        }

        try:
            # Read existing progress
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, 'r') as f:
                    all_progress = json.load(f)
            else:
                all_progress = []

            # Add new progress
            all_progress.append(progress_data)

            # Save back to file
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(all_progress, f, indent=2)

            print(f"[SAVE] Progress saved for user {user_id}")
            return True

        except Exception as e:
            print(f"[SAVE] Error saving progress: {str(e)}")
            return False

    def run_full_cycle(self, user_input, user_id=None):
        """
        Run the complete perception-reasoning-planning-action cycle
        Input: User's study topic and optional user ID
        Output: Complete learning content package
        """
        # Perception
        self.perceive(user_input)

        # Reasoning
        self.reason()

        # Planning
        self.plan()

        # Action
        result = self.act()

        # Save progress if user ID provided
        if user_id:
            self.save_progress(user_id)

        return result
