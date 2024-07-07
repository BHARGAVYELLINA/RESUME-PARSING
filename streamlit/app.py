import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from text_extraction.resume_parsing import parse_resume

files = st.file_uploader("Upload a file", accept_multiple_files=True)

submit = st.button("Submit")

bar = st.progress(0)

def flatten_resume(resume):
    return {
        "Name": resume.get("name", ""),
        "Phone": ", ".join(resume.get("contact_details", {}).get("phone", [])),
        "Email": ", ".join(resume.get("contact_details", {}).get("email", [])),
        "Skills": ", ".join(resume.get("skills", [])),
        "Education": "; ".join(["{} ({})".format(edu[0], edu[1]) for edu in resume.get("education", [])]),
        "Experience": "; ".join(resume.get("experience", []))
    }

if submit:
    parsed_resumes = []

    for i, file in enumerate(files):
        text = parse_resume(file)
        flattened_resume = flatten_resume(text)
        parsed_resumes.append(flattened_resume)
        bar.progress((i + 1) / len(files))

    columns = ["Name", "Phone", "Email", "Skills", "Education", "Experience"]
    new_dataframe = pd.DataFrame(parsed_resumes, columns=columns)

    st.dataframe(new_dataframe)
    st.text("")

    from io import BytesIO

    towrite = BytesIO()
    new_dataframe.to_excel(towrite, index=False, header=True)
    towrite.seek(0)
    st.download_button(
        label="Download Excel",
        data=towrite,
        file_name="resume_details.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )