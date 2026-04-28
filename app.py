import os
import csv
from datetime import datetime

JOB_DIR = "input_jobs"
RESUME_DIR = "input_resumes"
KB_DIR = "input_kb"
OUTPUT_DIR = "outputs"
TRACKER_DIR = "tracker"

KEYWORDS = [
    "python", "machine learning", "data preprocessing", "github", "git",
    "api", "sql", "communication", "problem solving", "oop",
    "database", "jupyter", "pandas", "numpy", "deep learning",
    "html", "css", "flask", "streamlit"
]

def ensure_folders():
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR]:
        os.makedirs(folder, exist_ok=True)

def read_files(folder):
    text = ""
    count = 0
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                text += f.read()
                count += 1
    return text, count

def extract_keywords(text):
    text = text.lower()
    return [k for k in KEYWORDS if k in text]

def compare(job, resume):
    matched = [s for s in job if s in resume]
    missing = [s for s in job if s not in resume]
    score = round((len(matched)/len(job))*100, 2) if job else 0
    return matched, missing, score

def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def job_analysis(skills):
    return "Job Skills:\n" + "\n".join(f"- {s}" for s in skills)

def skill_gap(matched, missing, score):
    text = f"Match Score: {score}%\n\nMatched:\n"
    text += "\n".join(matched)
    text += "\n\nMissing:\n"
    text += "\n".join(missing)
    return text

def resume_suggestions(job_skills, missing):
    text = "Resume Suggestions:\n"
    for skill in job_skills:
        text += f"- Add {skill} in your resume\n"
    if missing:
        text += "\nImprove these:\n"
        text += "\n".join(missing)
    return text

def interview_questions(job_skills, kb):
    text = "Interview Questions:\n"
    for s in job_skills:
        text += f"- Explain {s}\n"
    text += "\nHR Questions:\n- Tell me about yourself\n- Why should we hire you?\n"
    return text

def create_tracker():
    path = os.path.join(TRACKER_DIR, "applications.csv")
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id","company","role","status"])
            writer.writerow(["APP-001","ABC","AI Intern","Not Applied"])
    return path

def reminders():
    return "Reminder: Apply and prepare!"

def run():
    ensure_folders()

    job, jc = read_files(JOB_DIR)
    resume, rc = read_files(RESUME_DIR)
    kb, kc = read_files(KB_DIR)

    if jc == 0 or rc == 0 or kc == 0:
        print("Add files in all folders")
        return

    job_skills = extract_keywords(job)
    resume_skills = extract_keywords(resume)

    matched, missing, score = compare(job_skills, resume_skills)

    save(os.path.join(OUTPUT_DIR,"job_analysis.txt"), job_analysis(job_skills))
    save(os.path.join(OUTPUT_DIR,"skill_gap.txt"), skill_gap(matched, missing, score))
    save(os.path.join(OUTPUT_DIR,"resume.txt"), resume_suggestions(job_skills, missing))
    save(os.path.join(OUTPUT_DIR,"questions.txt"), interview_questions(job_skills, kb))

    create_tracker()
    save(os.path.join(TRACKER_DIR,"reminders.txt"), reminders())

    print("✅ Full Agent Completed!")

if __name__ == "__main__":
    run()