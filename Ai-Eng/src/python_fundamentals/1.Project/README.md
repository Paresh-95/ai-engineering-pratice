# OpenRouter Chat

A streaming chat app that uses the dependencies from the main `Python Fundamentals` UV project. The API key stays on the Python server.

## Setup

1. From the workspace root, copy `Python Fundamentals/1.Project/.env.example` to `Python Fundamentals/1.Project/.env` and set `OPENROUTER_API_KEY`.

2. Start the web frontend:

   ```bash
   uv run --project "Python Fundamentals" python "Python Fundamentals/1.Project/web_app.py"
   ```

3. Open <http://127.0.0.1:8000>.

The original CLI script remains available with `uv run --project "Python Fundamentals" python "Python Fundamentals/1.Project/app.py"`.

Set `HOST` or `PORT` to change the local bind address or port.
