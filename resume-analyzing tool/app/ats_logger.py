import os
import csv

ATS_LOG_FILE = os.path.join("ats_records", "ats_log.csv")

# Ensure folder and CSV exist
os.makedirs("ats_records", exist_ok=True)
if not os.path.exists(ATS_LOG_FILE):
    with open(ATS_LOG_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Resume Name", "ATS Score", "Remarks"])

def log_ats_score(resume_name, ats_score):
    """
    Log resume name, ATS score, and remarks (Good/Bad) to CSV.
    """
    remarks = "Good" if ats_score >= 70 else "Bad"
    
    with open(ATS_LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([resume_name, ats_score, remarks])
