# StudySaarthi Setup & Installation Guide

## System Requirements
- Python 3.8 or higher
- 500MB free disk space
- OpenAI API Key (free credits available)
- Any modern web browser

## Step-by-Step Installation

### Step 1: Create Python Virtual Environment

**Windows:**
```bash
# Open Command Prompt/PowerShell in project folder
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed Flask-2.3.3 openai-0.27.8 python-dotenv-1.0.0 ...
```

### Step 3: Get OpenAI API Key

1. Visit: https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the entire key (it starts with `sk-`)
4. Keep it secure! Don't share or commit to git

### Step 4: Configure Environment

1. Open `.env.example` in a text editor
2. Copy the entire content
3. Create a new file called `.env` in the project root
4. Paste the content and fill in:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   FLASK_ENV=development
   DEBUG=True
   SECRET_KEY=dev-secret-key
   ```

5. Save the `.env` file

### Step 5: Verify Installation

```bash
# Test Python installation
python --version

# Test pip packages
pip list | grep Flask
pip list | grep openai

# Check .env file exists
ls .env
```

### Step 6: Start the Application

```bash
# Make sure venv is activated
# (venv) should appear in your terminal

# Navigate to backend folder and run
cd backend
python app.py
```

Wait for message:
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

### Step 7: Open in Browser

1. Open your web browser (Chrome, Firefox, Safari, Edge)
2. Go to: **http://localhost:5000**
3. You should see the StudySaarthi interface
4. Try entering a topic like "Photosynthesis" or "French Revolution"

## Uninstall/Cleanup

To remove virtual environment:

**Windows:**
```bash
# Deactivate venv
deactivate

# Delete venv folder
rmdir /s venv
```

**macOS/Linux:**
```bash
# Deactivate venv
deactivate

# Delete venv folder
rm -rf venv
```

## Verify Everything Works

Run health check:
```bash
# In another terminal (with venv activated)
curl http://localhost:5000/api/health
```

Should return:
```json
{"status": "healthy", "app": "StudySaarthi", "environment": "development"}
```

## Next Steps

1. ✅ Application is running
2. Try a topic
3. View your progress
4. Check console for logs (helpful for debugging)

## Getting Help

1. **API Key Issues?** See ERROR_FIXES.md - API key section
2. **Connection Errors?** See ERROR_FIXES.md - Connection section
3. **Flask not starting?** Check if port 5000 is already in use

## Advanced: Run on Different Port

```bash
# Edit backend/config.py and change:
# FLASK_PORT = 5000  →  FLASK_PORT = 8000

# Or run with environment variable:
set FLASK_PORT=8000
python app.py
```

## Advanced: Production Setup

For public deployment:

1. Change `DEBUG=False` in `.env`
2. Change `SECRET_KEY` to random string
3. Use Gunicorn:
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:5000 backend.app:app
   ```

---

**Ready to learn? 🚀**
