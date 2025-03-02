import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from streamlit_ace import st_ace
import re

st.title('CP Homework Solver')
st.write('Just enter your CP problem statement and get the code, complexity, and test cases.\nIf any error occurs, please refresh the page as AI can make mistakes too. and it might be slow  so please wait after code generation, complexity analysis, and test case generation.')

# API Key input
api_key = st.sidebar.text_input("Enter API Key", type="password")
api_key="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"
model_name = st.sidebar.selectbox("Select Open Source model", ["Deepseek-r1-distill-llama-70b"])
language = st.sidebar.selectbox("Select Programming Language", ["c", "python", "java", "cpp"], index=0)

def generator(model, Cprompt, problem_statement): 
    prompt = ChatPromptTemplate.from_messages([
        ("system", Cprompt),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | model
    response = chain.invoke({"messages": [HumanMessage(content=problem_statement)]})
    return response.content

def generate_code(model, problem_statement):
    Cprompt = f"You are a student who solves Coding problems in {language} language. You have to solve a problem with two modules brute force and optimized approach approach in single programme. with proper modules and main function.you have to give just code no explantion, no comments is needed and always return code wrapped in triple backticks like ```{language} your code ```"
    solution = generator(model, Cprompt, problem_statement)
    
    match = re.search(fr'```{language}(.*?)```', solution, re.DOTALL)
    cleaned_content = match.group(1).strip() if match else solution.strip()

    st.subheader("Code")
    st.code(cleaned_content, language=language)
    
    return cleaned_content

def analyze_complexity(model, cleaned_content):
    ComPrompt = f"You are a code analyzer who analyzes Coding problems codes in {language} language. You have to analyze the code and provide the time complexity of need modules by using some maths , text like for this part of loop N and overall n2 something like that."
    
    solution = generator(model, ComPrompt, cleaned_content)
    cleaned_result = re.sub(r'<think>.*?</think>', '', solution, flags=re.DOTALL)
    
    st.subheader("Time Complexity Analysis")
    st.markdown(cleaned_result, unsafe_allow_html=True)
    
    return cleaned_result

def generate_testcases(model, code_content):
    Tprompt = f"""You are a code analyzer who analyzes Coding problems in {language} language 
    and gives appropriate test cases in markdown table format.
    
    **Table format:**
    
    | Sample Input | Expected Output (BruteForce) |
    | INPUT1   | OUTPUT1 |
    | INPUT2   | OUTPUT2 |
    
    Ensure:
    - **No extra separators (`------------------------`)**
    - **Consistent formatting**
    - **Properly formatted Markdown tables**
    """

    solution = generator(model, Tprompt, code_content)
    cleaned_testcases = re.sub(r'<think>.*?</think>', '', solution, flags=re.DOTALL)
    
    st.subheader("Test Cases")
    st.markdown(cleaned_testcases, unsafe_allow_html=True)
    
    return cleaned_testcases

if api_key:
    model = ChatGroq(model=model_name, groq_api_key=api_key)
    
    st.sidebar.write("Select what function you want to use:")
    option = st.sidebar.radio(["Generate Code, complexity analysis, test cases from problem statement", "Analyze Complexity of code and give test cases"])
    
    if option == "Generate Code":
        problem_statement = st.text_area("Enter your CP problem here:")
        if st.button("Solve"):
            if problem_statement:
                code_result = generate_code(model, problem_statement)
                analyze_complexity(model, code_result)
                generate_testcases(model, code_result)
            else:
                st.warning("Please enter a problem statement.")
    
    elif option == "Analyze Complexity":
        st.write("Paste your code below:")
        cleaned_code = st_ace(language="python", theme="monokai", height=200)
        if st.button("Analyze"):
            if cleaned_code:
                analyze_complexity(model, cleaned_code)
                generate_testcases(model, cleaned_code)
            else:
                st.warning("Please enter code to analyze.")
else:
    st.warning("Enter a valid API Key to use the service.")