# Student-Course-API

A simple REST API built with Python and Flask. It serves six fictional courses as JSON, includes a health check, and provides a small HTML homepage. No database or real student information is used.

## API endpoints

| Method | Endpoint | Success / purpose |
|---|---|---|
| GET | `/api/health` | `200` — API service status |
| GET | `/api/courses` | `200` — list of all courses |
| GET | `/api/courses/1` | `200` — details for course ID 1 |
| GET | `/api/courses/9999` | `404` — useful course-not-found error |

The homepage is available at `/`.

## Requirements

- Python 3.9 or newer
- pip

## Run locally

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server:

   ```bash
   python app.py
   ```

5. Open <http://127.0.0.1:5000/> in your browser.

The app reads the `PORT` environment variable and defaults to `5000` locally.

## Run tests

With the virtual environment activated:

```bash
python -m unittest -v
```

The tests use Flask's test client and do not require the server to be running.

## Example requests

```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/courses
curl http://127.0.0.1:5000/api/courses/1
curl -i http://127.0.0.1:5000/api/courses/9999
```

Example health response:

```json
{
  "service": "Student Course API",
  "status": "ok"
}
```

## Deploy to Render

1. Create a GitHub repository named `Student-Course-API`.
2. Add the files in this project to the repository and push your commit.
3. Sign in to [Render](https://render.com/).
4. Select **New +** → **Web Service**, then connect the GitHub repository.
5. Render can use the included `render.yaml` Blueprint configuration. If configuring manually, use:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
6. Deploy. When the service is live, open the Render URL to view the homepage and append `/api/health` to verify the JSON health response.

The included `render.yaml` defines the same build and start commands. Render supplies the `PORT` environment variable; Gunicorn binds to it through the `Procfile`/Render configuration. No secret environment variables or database are needed.

## CORS and error handling

CORS is enabled for the API using Flask-CORS. Course lookup returns JSON with HTTP `404` when an ID does not exist. Unmatched routes and unexpected server errors also return JSON error responses.
