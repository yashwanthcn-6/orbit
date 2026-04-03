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



Y

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

-



## 👥 Contributors

Built for ORBIT Agentic Hyperthon 2026

---


---

## 🎓 Learning Resources

- Flask: https://flask.palletsprojects.com/
- OpenAI API: https://platform.openai.com/docs/
- Python: https://www.python.org/
- REST APIs: https://restfulapi.net/

---

**Happy Learning with StudySaarthi! 📚✨**
