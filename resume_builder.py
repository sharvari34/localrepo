import streamlit as st
from fpdf import FPDF
import base64

def create_pdf(name, contact, email, phone linkedin, github, portfolio, address, education, skills, projects, rel_exp):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)

    # Name
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt=name, ln=True, align='C')
    pdf.ln(10)

    # Contact Information
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt=f'Contact: {contact}', ln=True, align='L')

    pdf.cell(200, 10, txt=f'Email: {email}', ln=True, align='L')
    pdf.cell(200, 10, txt=f'LinkedIn: {linkedin}', ln=True, align='L')
    pdf.cell(200, 10, txt=f'GitHub: {github}', ln=True, align='L')
    pdf.cell(200, 10, txt=f'Portfolio: {portfolio}', ln=True, align='L')
    pdf.cell(200, 10, txt=f'Address: {address}', ln=True, align='L')
    pdf.ln(10)
    
   

    # Skills
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt='Skills', ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, skills)

    # Projects
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt='Projects', ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for project in projects:
        pdf.multi_cell(0, 10, f"Title: {project['title']}\nDescription: {project['description']}")
        pdf.ln(5)

    # Relevant Experience
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt='Relevant Experience', ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, rel_exp)


     # Education
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt='Education', ln=True, align='L')
    pdf.set_font('Arial', size=12)
    for edu in education:
        pdf.multi_cell(0, 10, f"Institution: {edu['institution']}\nPeriod: {edu['period']}\nCGPA: {edu['cgpa']}")
        pdf.ln(5)
    return pdf

def main():    
    st.title('Resume')

    # Sidebar
    with st.sidebar:
        st.subheader("Personal Info")
        name = st.text_input('Name')
        contact=st.text_input('Contact no.')
        
        email=st.text_input('Email')
        linkedin=st.text_input("LinkedIn URL")
        github=st.text_input("GitHub URL")
        porfolio=st.text_input("Portfolio URL")
        address = st.text_input('Address')

        st.subheader('Education')
        education = []
        num_education = st.number_input('Number of Education Entries', min_value=1, max_value=10, step=1)
        for i in range(int(num_education)):
            institution = st.text_input(f'Institution {i+1}', key=f'institution_{i}')
            period = st.text_input(f'Time Period {i+1}', key=f'period_{i}')
            cgpa = st.text_input(f'CGPA {i+1}', key=f'cgpa_{i}')
            education.append({'institution': institution, 'period': period, 'cgpa': cgpa})

        st.subheader('Skills (Enter each skill on a new line)')
        skills = st.text_area('Skills')

        st.subheader('Projects')
        projects = []
        num_projects = st.number_input('Number of Projects', min_value=1, max_value=10, step=1)
        for i in range(int(num_projects)):
            title = st.text_input(f'Project Title {i+1}', key=f'project_title_{i}')
            description = st.text_input(f'Project Description {i+1}', key=f'project_description_{i}')
            projects.append({'title': title, 'description': description})

        st.subheader('Relevant Experience')
        certifications = st.text_area('Relevant Experience')
 
    # Display
    st.write(f'## {name}')
    st.write(f'**Contact:**{contact}')

    st.write(f'**Email:** {email}')

    st.write(f'**LinkedIn:** {linkedin}')
    st.write(f'**GitHub:** {github}')
    st.write(f'**Portfolio:** {portfolio}')
    st.write(f'**Address:** {address}')
    st.write(f'### Education')
    for edu in education:
        st.write(f"Institution: {edu['institution']}")
        st.write(f"Period: {edu['period']}")
        st.write(f"CGPA: {edu['cgpa']}")
        st.write('')

    st.write('## Skills')
    for skill in skills.split('\n'):
        st.write(f'. {skill}')

    st.write('### Projects')
    for project in projects:
        st.write(f"**{project['title']}**")
        st.write(f"Description: {project['description']}")
        st.write('')

    st.write('### Relevant Experience')  
    st.write(rel_exp)  

    # PDF and Download Link
    if st.button('Download Resume as PDF'):
        pdf = create_pdf(name, contact, email, linkedin, github, portfolio, address, education, skills, projects, rel_exp)
        pdf_output = f"{name.replace(' ', '_')}_resume.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, 'rb') as pdf_file:
            pdf_bytes = pdf_file.read()
            b64_pdf = base64.b64encode(pdf_bytes).decode()

        # Download button
        href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{pdf_output}">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
   main()



