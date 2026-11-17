import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COURSES = [
    {
        "id": 1,
        "code": "CS101",
        "name": "Introduction to Programming",
        "description": "Learn programming fundamentals, problem-solving, and Python basics."
    },
    {
        "id": 2,
        "code": "MATH201",
        "name": "Applied Mathematics",
        "description": "Explore algebra, statistics, and mathematical tools for practical problems."
    },
    {
        "id": 3,
        "code": "ENG110",
        "name": "Academic Communication",
        "description": "Develop clear academic writing, presentation, and communication skills."
    },
    {
        "id": 4,
        "code": "SCI120",
        "name": "Foundations of Environmental Science",
        "description": "Study ecosystems, sustainability, and human impacts on the environment."
    },
    {
        "id": 5,
        "code": "BUS205",
        "name": "Principles of Management",
        "description": "Understand planning, organizing, leadership, and organizational decision-making."
    },
    {
        "id": 6,
        "code": "IT210",
        "name": "Web Development Fundamentals",
        "description": "Build a foundation in web technologies, HTTP, HTML, CSS, and APIs."
    }
]


@app.get("/")
def homepage():
    """Simple HTML landing page describing the API."""
    endpoint_rows = [
        ("GET", "/api/health", "Check API service status"),
        ("GET", "/api/courses", "Retrieve all available courses"),
        ("GET", "/api/courses/1", "Retrieve course with ID 1"),
        ("GET", "/api/courses/9999", "Example not-found response")
    ]
    endpoints_html = "".join(
        f"<li><code>{method} {path}</code> — {description}</li>"
        for method, path, description in endpoint_rows
    )
    example = jsonify(COURSES[0]).get_data(as_text=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Student Course API</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 850px; margin: 48px auto;
           padding: 0 20px; color: #182230; line-height: 1.6; }}
    .status {{ display: inline-block; padding: 4px 10px; border-radius: 20px;
               background: #dcfce7; color: #166534; font-weight: 700; }}
    code, pre {{ background: #f1f5f9; border-radius: 5px; }}
    code {{ padding: 2px 5px; }} pre {{ padding: 16px; overflow-x: auto; }}
    li {{ margin: 10px 0; }}
  </style>
</head>
<body>
  <h1>Student Course API</h1>
  <p>A lightweight REST API built with Python and Flask. It provides fictional
     course information in JSON and does not use a database or real student data.</p>
  <p>API status: <span class="status">Operational</span></p>
  <h2>Available endpoints</h2>
  <ul>{endpoints_html}</ul>
  <h2>Example JSON response — GET /api/courses/1</h2>
  <pre>{example}</pre>
  <p>For machine-readable status, visit <a href="/api/health">/api/health</a>.</p>
</body>
</html>"""


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Student Course API"}), 200


@app.get("/api/courses")
def get_courses():
    return jsonify({"courses": COURSES, "count": len(COURSES)}), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    course = next((item for item in COURSES if item["id"] == course_id), None)
    if course is None:
        return jsonify({
            "error": "Course not found",
            "message": f"No course exists with ID {course_id}."
        }), 404
    return jsonify(course), 200


@app.errorhandler(404)
def handle_not_found(error):
    # Keep unknown routes in JSON format as well.
    return jsonify({"error": "Not found", "message": "The requested resource was not found."}), 404


@app.errorhandler(500)
def handle_server_error(error):
    app.logger.exception("Unexpected server error")
    return jsonify({"error": "Internal server error", "message": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
