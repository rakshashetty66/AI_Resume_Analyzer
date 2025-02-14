from flask import Flask, render_template, request
from model import process_resume, match_resume_with_job

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_description = request.form["job_description"]
        resume_file = request.files["resume"]

        # Extract text from resume
        resume_text = process_resume(resume_file)

        # Get match score & suggestions
        match_score, missing_skills = match_resume_with_job(resume_text, job_description)

        return render_template("result.html", score=match_score, missing=missing_skills)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
