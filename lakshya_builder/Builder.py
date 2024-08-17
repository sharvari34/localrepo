import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import os

# Function to generate advanced PDF design
class PDF(FPDF):
    def header(self):
        # Header with a background box and the title
        self.set_fill_color(0, 102, 204)
        self.rect(0, 0, 210, 40, 'F')
        self.set_font('Arial', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 40, 'Resume', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        # Add a simple footer with the page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_section_title(self, title):
        # Advanced section title formatting
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=True, align='L')
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
    
    def add_personal_info(self, label, content):
        # Personal Information formatting
        self.set_font('Arial', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.cell(30, 10, label, ln=False, align='L')

        self.set_font('Arial', '', 12)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, content, ln=True, align='L')

    def add_content_box(self, label, content):
        # Create a content box for skills, experience, etc.
        self.set_fill_color(240, 240, 240)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, label, ln=True, align='L', fill=True)
        self.multi_cell(0, 10, content, align='L')
        self.ln(5)

def generate_pdf(name, email, phone, linkedin, skills, education, experience, projects, additional_info, image_path=None):
    pdf = PDF()
    pdf.add_page()

    # Add Profile Picture if available
    if image_path:
        pdf.image(image_path, x=150, y=50, w=40, h=40)

    # Personal Information
    pdf.add_section_title("Personal Information")
    pdf.add_personal_info("Name:", name)
    pdf.add_personal_info("Email:", email)
    pdf.add_personal_info("Phone:", phone)
    pdf.add_personal_info("LinkedIn:", linkedin)
    pdf.ln(5)

    # Skills Section
    pdf.add_section_title("Skills")
    skills_list = skills.split("\n")
    for skill in skills_list:
        pdf.cell(0, 10, f"- {skill}", ln=True)
    pdf.ln(5)

    # Education Section
    pdf.add_section_title("Education")
    pdf.add_content_box("", education)

    # Work Experience Section
    pdf.add_section_title("Work Experience")
    pdf.add_content_box("", experience)

    # Projects Section
    pdf.add_section_title("Projects")
    pdf.add_content_box("", projects)

    # Additional Information Section
    pdf.add_section_title("Additional Information")
    pdf.add_content_box("", additional_info)

    # Save PDF to a BytesIO object
    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)

    return pdf_output

# Streamlit UI
st.title("Advanced Resume Maker")

st.subheader("Please fill in your details to generate a professional resume.")

# Layout with columns
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile URL")

with col2:
    profile_pic = st.file_uploader("Upload Profile Picture (optional)", type=["png", "jpg", "jpeg"])
    profile_summary = st.text_area("Profile Summary", help="Brief overview of your professional background and goals.")

# Expander sections for collapsible details
with st.expander("Skills"):
    skills = st.text_area("List of Skills (one per line)", help="e.g., Python\nData Analysis\nLeadership")

with st.expander("Education"):
    education_institution = st.text_input("Institution")
    education_period = st.text_input("Period (e.g., 2017-2021)")
    education_cgpa = st.text_input("CGPA")
    education = f"{education_institution}\nPeriod: {education_period}\nCGPA: {education_cgpa}"

with st.expander("Work Experience"):
    company_name = st.text_input("Company")
    work_period = st.text_input("Period (e.g., June 2019 - August 2020)")
    role = st.text_input("Role")
    work_description = st.text_area("Description")
    experience = f"{role} at {company_name}\nPeriod: {work_period}\n{work_description}"

with st.expander("Projects"):
    project_title = st.text_input("Project Title")
    project_description = st.text_area("Project Description")
    projects = f"{project_title}\n{project_description}"

with st.expander("Additional Information"):
    additional_info = st.text_area("Additional Information (e.g., Certifications, Languages, etc.)")

# Submit button
if st.button("Generate PDF"):
    if name and email and phone and linkedin and profile_summary and skills and education and experience and projects and additional_info:
        # Save the profile picture to a file if provided
        image_path = None
        if profile_pic:
            image = Image.open(profile_pic)
            image_path = "profile_pic.jpg"
            image.save(image_path)

        # Generate the PDF
        pdf = generate_pdf(name, email, phone, linkedin, skills, education, experience, projects, additional_info, image_path)

        # Remove the profile picture file if it was saved
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        st.success("Resume generated successfully!")
        st.download_button(
            label="Download Resume",
            data=pdf,
            file_name=f"{name.replace(' ', '_')}_resume.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Please fill in all the fields before generating the PDF.")
