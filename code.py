import streamlit as st
from fpdf import FPDF
from io import BytesIO


def main():
    st.title("Resume Maker Application")
    
    # Form for user input
    st.header("Enter your details")
    
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile URL")
    
    # Dynamic Fields for Education
    st.header("Education")
    education_entries = []
    num_education = st.number_input("Number of Education Entries", min_value=1, max_value=10, step=1, value=1)
    for i in range(num_education):
        st.subheader(f"Entry {i+1}")
        institution = st.text_input(f"Institution Name {i+1}", key=f'institution_{i}')
        period_education = st.text_input(f"Period {i+1} (e.g., 2016-2020)", key=f'period_education_{i}')
        cgpa = st.text_input(f"CGPA {i+1}", key=f'cgpa_{i}')
        education_entries.append((institution, period_education, cgpa))
    
    # Dynamic Fields for Work Experience
    st.header("Work Experience")
    work_experience_entries = []
    num_experience = st.number_input("Number of Work Experience Entries", min_value=1, max_value=10, step=1, value=1)
    for i in range(num_experience):
        st.subheader(f"Entry {i+1}")
        company = st.text_input(f"Company Name {i+1}", key=f'company_{i}')
        period_work = st.text_input(f"Period {i+1} (e.g., Jan 2021 - Present)", key=f'period_work_{i}')
        role = st.text_input(f"Role {i+1}", key=f'role_{i}')
        work_description = st.text_area(f"Job Description {i+1}", key=f'work_description_{i}')
        work_experience_entries.append((company, period_work, role, work_description))
    
    # Dynamic Fields for Projects
    st.header("Projects")
    project_entries = []
    num_projects = st.number_input("Number of Project Entries", min_value=1, max_value=10, step=1, value=1)
    for i in range(num_projects):
        st.subheader(f"Entry {i+1}")
        project_title = st.text_input(f"Project Title {i+1}", key=f'project_title_{i}')
        project_description = st.text_area(f"Project Description {i+1}", key=f'project_description_{i}')
        project_entries.append((project_title, project_description))
    
    # Additional Information
    st.header("Additional Information")
    additional_info = st.text_area("Additional Information (certifications, languages, etc.)")
    
    # Generate Resume
    if st.button("Generate Resume"):
        pdf = generate_resume_pdf(name, email, phone, linkedin, education_entries, work_experience_entries, project_entries, additional_info)
        st.download_button(label="Download Resume as PDF", data=pdf, file_name=f"{name}_resume.pdf", mime="application/pdf")

def generate_resume_pdf(name, email, phone, linkedin, education_entries, work_experience_entries, project_entries, additional_info):
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font("Arial", 'B', 24)  # Increased font size for name
    pdf.cell(0, 15, txt=name, ln=True, align='C')  # Centered name
    
    # Add contact details, centered
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Email: {email}", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Phone: {phone}", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"LinkedIn: {linkedin}", ln=True, align='C')
    
    pdf.ln(10)  # Line break
    
    # Add Education section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Education", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for institution, period_education, cgpa in education_entries:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"{institution} ({period_education})", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"CGPA: {cgpa}")
    pdf.ln(5)
    
    # Add Work Experience section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Work Experience", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for company, period_work, role, work_description in work_experience_entries:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"{company} ({period_work})", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"Role: {role}\n{work_description}")
    pdf.ln(5)
    
    # Add Projects section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Projects", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for project_title, project_description in project_entries:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"{project_title}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"{project_description}")
    pdf.ln(5)
    
    # Add Additional Information section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Additional Information", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=additional_info)
    
    # Save PDF to a BytesIO object
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))  # Write the binary string to BytesIO
    pdf_output.seek(0)
    
    return pdf_output


if __name__ == "__main__":
    main()
