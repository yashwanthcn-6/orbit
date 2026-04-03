"""
StudySaarthi Autonomous Learning Agent
Core agent logic for perception, reasoning, planning, and action
"""

import json
import os
import re
from datetime import datetime

import openai
from openai.error import APIError, AuthenticationError, RateLimitError

from config import (
    MODEL_CONFIG,
    OPENAI_API_KEY,
    OPENAI_ENABLED,
    PROGRESS_FILE,
    TOPIC_CATEGORIES,
)

# Initialize OpenAI client for the pinned 0.x SDK
openai.api_key = OPENAI_API_KEY


def _normalize_words(topic):
    return [word for word in re.findall(r"[A-Za-z0-9']+", topic) if word]


def _display_topic(topic):
    words = _normalize_words(topic)
    if not words:
        return topic.strip().title() or "This Topic"
    return " ".join(word.capitalize() for word in words)


def _topic_variants(topic):
    clean_topic = _display_topic(topic)
    base_words = _normalize_words(topic.lower())
    last_word = base_words[-1] if base_words else "topic"
    return clean_topic, last_word


def _category_focus(category):
    if category == 'science_math':
        return (
            "core principles, cause-and-effect, and worked examples",
            "definition, process, formula or rule, and one practical use"
        )
    if category == 'history_gk':
        return (
            "timeline, major actors, turning points, and why it mattered",
            "background, key event, impact, and one memorable takeaway"
        )
    return (
        "big-picture meaning, useful examples, and real-life relevance",
        "idea, why it matters, example, and one easy way to remember it"
    )


def _fallback_response(section, topic, category):
    """Generate meaningful local study content when OpenAI is unavailable."""
    clean_topic, last_word = _topic_variants(topic)
    focus, notes_focus = _category_focus(category)

    if section == 'explanation':
        return (
            f"{clean_topic} is easiest to learn when you begin with the main idea and then connect it to a simple example. "
            f"For this topic, focus on {focus}. Ask what {clean_topic} means, where it appears, and why a student should care about it.\n\n"
            f"After that, describe the topic in your own words and connect it to one familiar situation. If you can explain the definition, "
            f"identify the most important parts, and give one example, you already understand the foundation well."
        )

    if section == 'notes':
        return (
            "1. Key Concepts\n"
            f"- {clean_topic} is the main topic being studied.\n"
            f"- Review it through {notes_focus}.\n"
            "- Learn the big idea before memorizing smaller details.\n"
            "- Connect the topic to one concrete example.\n\n"
            "2. Important Points\n"
            f"- Ask: what is {clean_topic}, how does it work, and why does it matter?\n"
            "- Compare it with a related idea to avoid confusion.\n"
            f"- Revise the important terms linked to {clean_topic}.\n"
            "- Practice recalling the topic without looking at notes.\n\n"
            "3. Examples or Applications\n"
            f"- Explain {clean_topic} to a classmate in simple language.\n"
            "- Write a 3-line summary in your own words.\n"
            f"- Solve or discuss one example involving {last_word}.\n\n"
            "4. Remember\n"
            "- Study the meaning first, then the details.\n"
            "- Use one keyword, one example, and one quick recap."
        )

    if section == 'quiz':
        return (
            f"1. What is the best first step in understanding {clean_topic}?\n"
            "A. Memorizing every detail\n"
            "B. Identifying the core idea\n"
            "C. Ignoring examples\n"
            "D. Skipping definitions\n"
            "Answer: B\n"
            "Explanation: Starting with the central idea makes the rest of the topic easier to organize.\n\n"
            f"2. Why are examples helpful when studying {clean_topic}?\n"
            "A. They replace definitions completely\n"
            "B. They make revision unnecessary\n"
            "C. They connect ideas to practical understanding\n"
            "D. They only help advanced learners\n"
            "Answer: C\n"
            "Explanation: Examples turn abstract information into something easier to remember and apply.\n\n"
            f"3. Which revision method is most effective for {clean_topic}?\n"
            "A. Passive rereading only\n"
            "B. Active recall in your own words\n"
            "C. Studying once and stopping\n"
            "D. Memorizing without structure\n"
            "Answer: B\n"
            "Explanation: Active recall shows whether you really understand the topic."
        )

    if section == 'next_topic':
        return (
            f"- Basics of {clean_topic} (build the core definition and vocabulary)\n"
            f"- Applications of {clean_topic} (see how the idea is used in examples or real situations)\n"
            f"- Advanced concepts related to {clean_topic} (move from foundation to deeper understanding)"
        )

    return f"Local study content for {clean_topic}."


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
        self.mode = 'openai'

    def perceive(self, user_input):
        """
        PERCEPTION STEP: Understand and validate user's topic
        Input: Raw user input (study topic)
        Output: Cleaned topic string
        """
        self.topic = user_input.strip().lower()
        print(f"[PERCEIVE] Understood topic: {self.topic}")
        return self.topic

    def reason(self):
        """
        REASONING STEP: Classify the topic into one of three categories
        Input: Topic string
        Output: Category classification (science_math, history_gk, or general)
        """
        topic_lower = self.topic.lower()
        scores = {
            'science_math': 0,
            'history_gk': 0,
            'general': 0
        }

        for category, config in TOPIC_CATEGORIES.items():
            for keyword in config['keywords']:
                if keyword in topic_lower:
                    scores[category] += 1

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
        else:
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
                'mode': self.mode,
                'timestamp': datetime.now().isoformat()
            }

            print(f"[ACT] Generated all learning content in {self.mode} mode")
            return result

        except Exception as e:
            print(f"[ACT] Error generating content: {str(e)}")
            return {
                'error': f"Failed to generate content: {str(e)}",
                'topic': self.topic
            }

    def _should_use_local_mode(self):
        return self.mode == 'local' or not OPENAI_ENABLED or not OPENAI_API_KEY

    def _generate_explanation(self):
        """Generate detailed explanation of the topic using OpenAI or local mode."""
        if self._should_use_local_mode():
            self.mode = 'local'
            return _fallback_response('explanation', self.topic, self.category)

        prompt = f"""
        Explain the topic "{self.topic}" in a clear, beginner-friendly way.
        Category: {self.category}

        Make it engaging and easy to understand. Use simple language.
        Keep it concise but comprehensive (2-3 paragraphs).
        """

        try:
            response = openai.ChatCompletion.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert educator creating learning content for students."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=MODEL_CONFIG['max_tokens']
            )
            return response["choices"][0]["message"]["content"].strip()

        except (RateLimitError, APIError, AuthenticationError) as e:
            self.mode = 'local'
            print(f"[ACT-FALLBACK] Explanation generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('explanation', self.topic, self.category)
        except Exception as e:
            self.mode = 'local'
            print(f"[ACT-ERROR] Explanation generation general error: {str(e)}")
            return _fallback_response('explanation', self.topic, self.category)

    def _generate_notes(self):
        """Generate structured study notes using OpenAI or local mode."""
        if self._should_use_local_mode():
            self.mode = 'local'
            return _fallback_response('notes', self.topic, self.category)

        prompt = f"""
        Create concise study notes for "{self.topic}" using the following format:

        1. Key Concepts (3-4 bullet points)
        2. Important Points (3-4 bullet points)
        3. Examples or Applications (2-3 items)
        4. Remember (1-2 memory tips or mnemonics)

        Make it scannable and easy to memorize.
        """

        try:
            response = openai.ChatCompletion.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert at creating study notes and guides."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=MODEL_CONFIG['max_tokens']
            )
            return response["choices"][0]["message"]["content"].strip()

        except (RateLimitError, APIError, AuthenticationError) as e:
            self.mode = 'local'
            print(f"[ACT-FALLBACK] Notes generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('notes', self.topic, self.category)
        except Exception as e:
            self.mode = 'local'
            print(f"[ACT-ERROR] Notes generation general error: {str(e)}")
            return _fallback_response('notes', self.topic, self.category)

    def _generate_quiz(self):
        """Generate interactive quiz questions using OpenAI or local mode."""
        if self._should_use_local_mode():
            self.mode = 'local'
            return _fallback_response('quiz', self.topic, self.category)

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
            response = openai.ChatCompletion.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator with clear formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=MODEL_CONFIG['max_tokens']
            )
            return response["choices"][0]["message"]["content"].strip()

        except (RateLimitError, APIError, AuthenticationError) as e:
            self.mode = 'local'
            print(f"[ACT-FALLBACK] Quiz generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('quiz', self.topic, self.category)
        except Exception as e:
            self.mode = 'local'
            print(f"[ACT-ERROR] Quiz generation general error: {str(e)}")
            return _fallback_response('quiz', self.topic, self.category)

    def _suggest_next_topic(self):
        """Suggest related next topics for continuation of learning."""
        if self._should_use_local_mode():
            self.mode = 'local'
            return _fallback_response('next_topic', self.topic, self.category)

        prompt = f"""
        Based on the topic "{self.topic}", suggest 3 related topics that a student should learn next.

        List them as:
        - Topic name (brief description)

        Make them progressive (easy to advanced).
        """

        try:
            response = openai.ChatCompletion.create(
                model=MODEL_CONFIG['model'],
                messages=[
                    {"role": "system", "content": "You are an expert at designing learning paths."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_CONFIG['temperature'],
                max_tokens=500
            )
            return response["choices"][0]["message"]["content"].strip()

        except (RateLimitError, APIError, AuthenticationError) as e:
            self.mode = 'local'
            print(f"[ACT-FALLBACK] Next topic generation failed ({type(e).__name__}): {str(e)}")
            return _fallback_response('next_topic', self.topic, self.category)
        except Exception as e:
            self.mode = 'local'
            print(f"[ACT-ERROR] Next topic generation general error: {str(e)}")
            return _fallback_response('next_topic', self.topic, self.category)

    def save_progress(self, user_id):
        """Save user's learning progress to JSON file."""
        self.user_id = user_id

        progress_data = {
            'user_id': user_id,
            'topic': self.topic,
            'category': self.category,
            'timestamp': datetime.now().isoformat(),
            'session_data': self.learning_flow
        }

        try:
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, 'r') as f:
                    all_progress = json.load(f)
            else:
                all_progress = []

            all_progress.append(progress_data)

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
        self.perceive(user_input)
        self.reason()
        self.plan()
        result = self.act()

        if user_id:
            self.save_progress(user_id)

        return result
