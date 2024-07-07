import re
import spacy
from docx import Document
from pdfminer.high_level import extract_text

nlp = spacy.load('en_core_web_sm')

def clean_text(text):
    cleaned_text = re.sub("\n+", " ", text)
    cleaned_text = re.sub("\s+", " ", cleaned_text)
    cleaned_text = re.sub(r"[^a-zA-Z0-9@\s/.\-]", "", cleaned_text)
    return cleaned_text.strip()

def extract_contact_details(text):
    phone = re.findall(r'\b\d{10}\b', text)
    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return {"phone": phone, "email": email}

def extract_skills(text):
    doc = nlp(text)
    skills = []
    technical_skills_list = [
        'C', 'C++', 'JAVA', 'PYTHON', 'SQL', 'HTML/CSS', 'NODE JS', 'HASKELL', 'SCALA',
        'VS Code', 'Eclipse', 'Anaconda', 'Jupyter Notebook', 'Google Colab',
        'Cisco Packet Tracer', 'Arduino IDE', 'AutoCad'
    ]
    
    for token in doc:
        if token.text.upper() in technical_skills_list:
            skills.append(token.text.upper())

    return list(set(skills))

def extract_education(text):
    education = []
    pattern = r'(\b[Bb]achelor\'?s?\b|\b[Mm]aster\'?s?\b|\b[Mm]\.?[Ss]c\b|\b[Bb]\.?[Ss]c\b|\bPh\.?[Dd]\b|\b[Dd]iploma\b|\b[Dd]egree\b|\b[Bb]\.?[Tt]ech\b).*?(\b[University|College|School]+\b)[\s,]*(.*?)(\b[\d]{4}\b).*?(\b[\d]{4}\b)'
    for match in re.finditer(pattern, text):
        degree = match.group(1)
        duration = match.group(4) + ' - ' + match.group(5)
        education.append((degree, duration))
    return education

def extract_experience(text):
    experience = re.findall(r'\b\d+\s+(years|months)\b.*?\b(experience|worked)\b', text, re.IGNORECASE)
    return experience

def extract_name(text):
    name_match = re.match(r'^([A-Za-z]+)\s([A-Za-z]+)', text)
    if name_match:
        return f"{name_match.group(1)} {name_match.group(2)}"
    return None


def parse_resume(file_path):
    if file_path.name.endswith('.pdf'):
        text = extract_text(file_path)
    else:
        raise ValueError("Unsupported file format")

    cleaned_text = clean_text(text)
    contact_details = extract_contact_details(cleaned_text)
    skills = extract_skills(cleaned_text)
    education = extract_education(cleaned_text)
    experience = extract_experience(cleaned_text)
    name = extract_name(cleaned_text)

    return {
        "name": name,
        "contact_details": contact_details,
        "skills": skills,
        "education": education,
        "experience": experience
    }