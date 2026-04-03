# Common Errors & Fixes for StudySaarthi

## 🔴 Error: "ModuleNotFoundError: No module named 'flask'"

### Cause
Dependencies not installed or venv not activated

### Fix
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Check if it's activated**: You should see `(venv)` at the start of terminal

---

## 🔴 Error: "OPENAI_API_KEY not found in environment"

### Cause
API key not set in `.env` file

### Fix
1. Copy `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` file with text editor
3. Find line: `OPENAI_API_KEY=your_openai_api_key_here`
4. Replace with actual key from https://platform.openai.com/account/api-keys
5. **Important**: Keep `sk-` at the beginning, don't remove it

Example:
```
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

---

## 🔴 Error: "Connection refused" / "Cannot connect to http://localhost:5000"

### Cause
Flask server not running or wrong port

### Fix
1. **Check if Flask is running**:
   - Should see "Running on http://localhost:5000"
   - Should not see errors in terminal

2. **Port already in use**:
   ```bash
   # Windows - Find what's using port 5000
   netstat -ano | findstr :5000
   
   # Kill the process
   taskkill /PID <PID> /F
   ```

3. **Restart Flask**:
   - Stop current session (Ctrl+C)
   - Wait 2 seconds
   - Run again: `python backend/app.py`

---

## 🔴 Error: "Failed to fetch" / API returns 404

### Cause
API endpoint path is wrong or Flask not responding

### Fix
1. Verify Flask is running and showing no errors
2. Check browser console (press F12) for exact error
3. Try health check:
   ```bash
   curl http://localhost:5000/api/health
   ```
4. Should see: `{"status": "healthy", ...}`

---

## 🔴 Error: "Invalid API Key"

### Cause
Wrong or expired API key format

### Fix
1. Get new key: https://platform.openai.com/account/api-keys
2. Make sure key starts with `sk-`
3. Update `.env` file
4. Restart Flask (`Ctrl+C`, then run again)

---

## 🔴 Error: "Topic input validation failed"

### Cause
Topic doesn't meet requirements

### Fix
Requirements:
- Minimum 2 characters
- Maximum 100 characters
- No special characters `< > { } ; --`

**Working examples**:
✅ "Photosynthesis"
✅ "French Revolution"
✅ "Machine Learning"

**Not working**:
❌ "a" (too short)
❌ "hello<script>" (invalid chars)
❌ "this is a very long topic" (too long)

---

## 🔴 Error: Empty response from AI

### Cause
- API quota exceeded
- Network timeout
- Invalid request

### Fix
1. **Check quotas**: https://platform.openai.com/account/billing/overview
2. **Try shorter topic**: "biology" instead of "advanced molecular biology"
3. **Restart Flask and try again**
4. **Check browser console** for exact error message

---

## 🔴 Error: "FileNotFoundError: [Errno 2] No such file or directory: '../data/progress.json'"

### Cause
Data directory doesn't exist or code running from wrong location

### Fix
```bash
# Make sure you're running from backend directory
cd backend

# Or create data directory manually
mkdir ../data

# Then run
python app.py
```

---

## 🔴 Error: "CORS Error" / "Access to XMLHttpRequest blocked"

### Cause
Browser security policy (usually in production)

### Fix
For development, it's normal browser behavior. To test:
1. Make sure you're accessing http://localhost:5000 (not 127.0.0.1)
2. Check "Access-Control-Allow-Origin" headers in Flask

If deploying to production, add CORS support:
```bash
pip install flask-cors
```

---

## 🔴 Error: "Timeout waiting for response"

### Cause
AI is taking too long to generate response (1-2 seconds normal, 10+ is slow)

### Fix
1. **Check API status**: https://status.openai.com/
2. **Try different topic** - some topics generate faster
3. **Increase timeout in script.js**:
   ```javascript
   // Change timeout value (in milliseconds)
   timeout: 30000  // 30 seconds instead of default
   ```

---

## 🔴 Error: "Port 5000 already in use"

### Cause
Another application using the same port

### Fix
**Option 1: Kill existing process**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**Option 2: Use different port**
Edit `backend/app.py`:
```python
# Change from:
app.run(port=5000)
# To:
app.run(port=8000)
```

---

## 🔴 Error: "SyntaxError: invalid syntax"

### Cause
Python code error (usually typo)

### Fix
1. **Check Python version**: `python --version` (needs 3.8+)
2. **Check for file encoding**: Make sure files are UTF-8
3. **Verify parentheses/brackets** are balanced
4. **Look at line number** in error message

---

## 🔴 Error: "json.JSONDecodeError"

### Cause
Response parsing failed (try-except issue)

### Fix
1. Check if response is actually JSON:
   ```bash
   curl -X POST http://localhost:5000/api/learn \
     -H "Content-Type: application/json" \
     -d '{"topic":"test"}'
   ```

2. Should return JSON with `success: true`

---

## 🔴 Error: "File not found" for static files (CSS/JS)

### Cause
Flask can't find CSS or JS files

### Fix
Check folder structure:
```
frontend/
├── static/
│   ├── css/
│   │   └── style.css       ← Check exists
│   └── js/
│       └── script.js       ← Check exists
└── templates/
    └── index.html
```

Run from correct directory:
```bash
cd backend
python app.py
```

---

## ✅ Testing Checklist

- [ ] Virtual environment activated: `(venv)` shows in terminal
- [ ] `.env` file exists and has `OPENAI_API_KEY`
- [ ] Flask running: "Running on http://localhost:5000"
- [ ] Browser opens http://localhost:5000 (no errors)
- [ ] Can type in topic input field
- [ ] "Start Learning" button doesn't immediately error
- [ ] After 2-5 seconds, see explanation, notes, quiz
- [ ] Can copy notes and quiz
- [ ] Can see progress when clicking "View Progress"

---

## 📞 Debug Mode

Enable detailed logging:

In `backend/app.py`, change:
```python
app.run(debug=True)  # Already on by default
```

Look for logs like:
```
[PERCEIVE] Understood topic: photosynthesis
[REASON] Classified topic into: science_math
[PLAN] Designed learning flow: [...]
[ACT] Generated all learning content
```

---

## 🚨 Still Stuck?

1. **Check browser console**: Press F12 → Console tab → Look for red errors
2. **Check Flask terminal**: Look for red error messages
3. **Verify .env**: Make sure OPENAI_API_KEY line has no quotes
4. **Try fresh start**:
   ```bash
   # Stop Flask (Ctrl+C)
   # Restart venv
   deactivate
   venv\Scripts\activate  # or source venv/bin/activate
   # Restart Flask
   cd backend && python app.py
   ```

---

**Still having issues? Make sure to check all three places for errors:**
1. **Browser console** (F12)
2. **Flask terminal** (where python is running)
3. **.env file** (check OpenAI key is valid)

Good luck! 🚀
