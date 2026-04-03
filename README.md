# StudySaarthi: Autonomous Learning Agent
## ORBIT Agentic Hyperthon Project

![StudySaarthi](https://img.shields.io/badge/Project-StudySaarthi-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3-white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Overview

**StudySaarthi** is a fully autonomous learning agent that demonstrates true autonomous reasoning and adaptive behavior - not just a chatbot. It perceives, reasons, plans, and acts independently to create customized learning experiences.

### Core Autonomous Features:
- **👁️ Perception**: Understands and validates user study topics
- **🧠 Reasoning**: Intelligently classifies topics into 3 categories
- **📐 Planning**: Designs adaptive learning workflows based on category
- **⚡ Action**: Generates customized explanations, notes, quizzes, and learning paths
- **🔄 Adaptive Behavior**: Different learning flows for different topic types

---

## 📁 Project Structure

```
studysaarthi-agent/
├── backend/
│   ├── app.py              # Flask application & API endpoints
│   ├── agent.py            # Core autonomous agent logic
│   ├── config.py           # Configuration & settings
│   └── utils.py            # Utility functions
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main UI template
│   └── static/
│       ├── css/
│       │   └── style.css   # Modern styling
│       └── js/
│           └── script.js   # Interactive frontend
├── data/                   # JSON storage for progress
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── SETUP.md               # Detailed setup instructions
├── ERROR_FIXES.md         # Common errors & solutions
└── PITCH.md               # Judge pitch document
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- OpenAI API Key (free or paid account)

### 1. Clone/Setup Project
```bash
# Navigate to project directory
cd studysaarthi-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# (Open .env in your text editor and paste your key)
```

### 4. Run the Application
```bash
# Start the Flask backend server
python backend/app.py
```

You should see:
```
==================================================
StudySaarthi - Autonomous Learning Agent
==================================================
Environment: development
Debug Mode: True

Starting Flask server...
Visit http://localhost:5000 in your browser
==================================================
```

### 5. Open in Browser
Visit: **http://localhost:5000**

---

## 📚 How It Works

### The Autonomous Agent Cycle

```
User Input (Topic)
       ↓
   [PERCEIVE] - Understand topic
       ↓
   [REASON] - Classify into category
       ↓
   [PLAN] - Design learning workflow
       ↓
   [ACT] - Generate content
       ↓
   [ADAPT] - Customize based on category
       ↓
User Gets: Explanation, Notes, Quiz, Next Topics
```

### Topic Categories & Workflows

#### 1. Science/Math Topics
- **Keywords**: physics, chemistry, biology, mathematics, calculus, algebra, geometry
- **Flow**: [explanation] → [examples] → [notes] → [quiz]
- **Style**: Technical with formulas and concepts
- **Questions**: 5 quiz questions

#### 2. History/Geography/GK Topics
- **Keywords**: history, geography, politics, culture, heritage, dynasty, war, revolution
- **Flow**: [timeline] → [explanation] → [key_points] → [quiz]
- **Style**: Narrative with historical context
- **Questions**: 4 quiz questions

#### 3. General Topics
- **Keywords**: technology, art, literature, music, sports, entertainment, health
- **Flow**: [overview] → [explanation] → [notes] → [quiz]
- **Style**: Conversational and practical
- **Questions**: 3 quiz questions

---

## 🔑 Getting Your OpenAI API Key

1. Go to: https://platform.openai.com/account/api-keys
2. Log in with your OpenAI account (create one if needed)
3. Click "Create new secret key"
4. Copy the key and paste it in your `.env` file

> **Note**: Free tier accounts get $5 credits. Each API call costs small amount.

---

## 📖 API Endpoints

### 1. Start Learning
**POST** `/api/learn`
```json
// Request
{
  "topic": "Photosynthesis",
  "user_id": "optional_user_id"
}

// Response
{
  "success": true,
  "topic": "photosynthesis",
  "category": "science_math",
  "explanation": "...",
  "notes": "...",
  "quiz": "...",
  "next_topics": "...",
  "user_id": "...",
  "timestamp": "2024-..."
}
```

### 2. Get User Progress
**GET** `/api/progress/{user_id}`
```json
// Response
{
  "success": true,
  "progress": [...],
  "count": 5
}
```

### 3. Get User Statistics
**GET** `/api/stats/{user_id}`
```json
// Response
{
  "success": true,
  "stats": {
    "total_sessions": 5,
    "category_breakdown": {
      "science_math": 2,
      "history_gk": 2,
      "general": 1
    },
    "topics_learned": ["photosynthesis", "..."],
    "total_topics": 5
  }
}
```

### 4. Health Check
**GET** `/api/health`
```json
// Response
{
  "status": "healthy",
  "app": "StudySaarthi",
  "environment": "development"
}
```

---

## 🎨 Frontend Features

### User Interface
- **Modern gradient design** with smooth animations
- **Responsive layout** - works on mobile, tablet, desktop
- **Real-time loading states** with spinner feedback
- **Session tracking** - automatic user ID generation
- **One-click copy** for notes and quiz
- **Suggested topics** - learn progressive topics

### Interactive Elements
- Input validation with helpful hints
- Error messages with clear guidance
- Progress tracking and statistics
- Learning history saved locally
- Keyboard shortcuts (Ctrl+Enter to submit, ESC to reset)

---

## 💾 Data Storage

Student progress is saved locally in JSON files:

### `data/progress.json`
Stores all learning sessions:
```json
[
  {
    "user_id": "user_12345",
    "topic": "photosynthesis",
    "category": "science_math",
    "timestamp": "2024-01-15T10:30:00",
    "session_data": {...}
  }
]
```

### `data/sessions.json`
Stores session metadata for analytics

---

## ⚙️ Configuration

Edit `backend/config.py` to customize:

```python
# Model settings
MODEL_CONFIG = {
    'model': 'gpt-3.5-turbo',
    'temperature': 0.7,
    'max_tokens': 1500,
    'top_p': 0.9
}

# Add custom categories
TOPIC_CATEGORIES = {
    'your_category': {
        'keywords': ['word1', 'word2'],
        'depth_level': 'detailed'
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

See **[ERROR_FIXES.md](ERROR_FIXES.md)** for:
- API key not found
- Connection refused errors
- Empty responses
- Timeout issues
- JSON parsing errors
- CORS errors
- Module not found errors

Quick fix for "Module not found":
```bash
# Make sure you're in the right directory
cd backend

# Run app from backend directory
python app.py
```

---

## 📊 Example Usage

### Example 1: Learn Photosynthesis
```
Input: "Photosynthesis"
Category: Science/Math (recognized from keywords)
Output:
  ✓ Technical explanation with formulas
  ✓ 3 detailed examples
  ✓ Study notes with mnemonics
  ✓ 5 quiz questions (easy → hard)
  ✓ Suggested: Cellular Respiration, ATP Production, Chloroplasts
```

### Example 2: Learn French Revolution
```
Input: "French Revolution"
Category: History/GK (recognized from keywords)
Output:
  ✓ Timeline-based explanation
  ✓ Historical context
  ✓ Key points and significance
  ✓ 4 multi-choice questions
  ✓ Suggested: American Revolution, Industrial Revolution, ...
```

### Example 3: Learn Machine Learning
```
Input: "Machine Learning"
Category: General (technology field)
Output:
  ✓ Conversational overview
  ✓ Practical applications
  ✓ Study notes
  ✓ 3 quiz questions
  ✓ Suggested: Deep Learning, Neural Networks, ...
```

---

## 🏆 Why This Is An Autonomous Agent

### NOT Just a Chatbot Because:

1. **True Reasoning**: Classifies topics using intelligent keyword matching
2. **Adaptive Planning**: Designs different workflows for different categories
3. **Autonomous Decision Making**: Agent decides learning path independently
4. **Goal-Oriented**: Structured cycle (Perceive → Reason → Plan → Act)
5. **Progressive Learning**: Suggests next topics based on current learning
6. **State Management**: Maintains learning progress and history
7. **Intelligent Routing**: Different content generation for each category

### Agent Architecture:
```
INPUT → PERCEPTION → REASONING → PLANNING → ACTION → OUTPUT
                                              ↓
                                         PROGRESS SAVED
                                              ↓
                                      Next Suggestion
```

See **[PITCH.md](PITCH.md)** for detailed judge explanation.

---

## 🔐 Security Notes

- API keys stored in `.env` (never committed to git)
- Input validation on all user fields
- XSS protection in template rendering
- HTTPS recommended for production
- Rate limiting recommended for production

---

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Spaced repetition algorithm
- [ ] Difficulty level adjustment
- [ ] Real-time progress analytics
- [ ] Audio/Video learning content
- [ ] Collaborative learning rooms
- [ ] Teacher dashboard
- [ ] Mobile app
- [ ] Offline mode with caching
- [ ] Integration with Notion/Obsidian

---

## 🚀 Deployment

### Using Gunicorn (Production)
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 backend.app:app
```

### Using Docker
See docker configuration in `Dockerfile` (optional)

### Heroku Deployment
1. Add `Procfile`: `web: gunicorn backend.app:app`
2. `git push heroku main`

---

## 📝 License

MIT License - Feel free to use and modify

---

## 👥 Contributors

Built for ORBIT Agentic Hyperthon 2024

---

## 📞 Support

For issues or questions:
1. Check [ERROR_FIXES.md](ERROR_FIXES.md)
2. Review Flask logs in terminal
3. Check browser console (F12)
4. Verify `.env` file has correct API key

---

## 🎓 Learning Resources

- Flask: https://flask.palletsprojects.com/
- OpenAI API: https://platform.openai.com/docs/
- Python: https://www.python.org/
- REST APIs: https://restfulapi.net/

---

**Happy Learning with StudySaarthi! 📚✨**
