import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import re

def generator(model, prompt_template, user_input):
    """Generates content using AI model."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_template),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | model
    response = chain.invoke({"messages": [HumanMessage(content=user_input)]})
    return response.content

def generate_readme(model, project_details):
    """Generates a README.md file based on project details."""
    prompt_template = """You are an expert in writing professional GitHub README.md files.
    Based on the given project details, create a structured README.md with the following sections:
    
    - Project Title
    - Description
    - Features
    - Installation Instructions
    - Usage
    - Technologies Used
    - Contribution Guidelines
    - License
    
    Ensure:
    - Proper Markdown formatting
    - Clear and concise descriptions
    - Bullet points where necessary
    - Code blocks for commands (use triple backticks)
    """
    
    readme_content = generator(model, prompt_template, project_details)
    cleaned_testcases = re.sub(r'<think>.*?</think>', '', readme_content, flags=re.DOTALL)
    
    st.subheader("Generated README.md")
    st.code(cleaned_testcases, language="markdown")
    
    return readme_content

st.title("GitHub README.md Generator")
st.write("Fill in your project details and get a professional README.md file!")

# API Key input
api_key = st.sidebar.text_input("Enter API Key", type="password")
model_name = st.sidebar.selectbox("Select Open Source model", ["Deepseek-r1-distill-llama-70b"])

# User inputs
project_name = st.text_input("Project Name")
description = st.text_area("Project Description")
features = st.text_area("Key Features (bullet points, comma-separated)")
technologies = st.text_input("Technologies Used (comma-separated)")
installation = st.text_area("Installation Steps")
usage = st.text_area("Usage Instructions")
contributing = st.text_area("Contribution Guidelines")
license = st.text_input("License (e.g., MIT, GPL)")

if st.button("Generate README"):
    if api_key and project_name and description:
        model = ChatGroq(model=model_name, groq_api_key=api_key)
        
        # Combine details for AI prompt
        project_details = f"""
        Project Name: {project_name}
        Description: {description}
        Features: {features}
        Technologies: {technologies}
        Installation: {installation}
        Usage: {usage}
        Contribution: {contributing}
        License: {license}
        """
        
        readme_content = generate_readme(model, project_details)
        
        # Provide download link
        st.download_button(
            label="Download README.md",
            data=readme_content,
            file_name="README.md",
            mime="text/markdown"
        )
    else:
        st.warning("Please enter all required details and API Key.")
