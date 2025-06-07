# 💼 Resume Matcher & ATS Compatibility Checker
## 🌐 Live Demo

👉 [Click here to try the live app](https://resume-tracker-847m.onrender.com/)


A **Streamlit-based web application** that helps job seekers:

- Match their **resume** to a **job posting**
- Calculate an **ATS (Applicant Tracking System) compatibility score**
- Generate a **professional job application email**

---

## 🚀 Features

- ✅ **Resume Upload**: Upload PDF resumes (up to 200MB)  
- 🌐 **Job Description Input**: Enter a job posting URL  
- 🧠 **Text Extraction**:
  - Resume: via **PyPDF2**
  - Job Posting: via **WebBaseLoader** (LangChain + BeautifulSoup4)
- 📊 **ATS Score Calculation**:
  - Uses **NLTK** & **scikit-learn** for NLP
  - Calculates **cosine similarity** between resume and job text (e.g., 36.28%)
    
- 🤖 **Langchain-Groq Integration**:
  - Interacts with **Grok API** via **langchain-groq**
  - Extracts structured **JSON** data
  - Generates **professional job application email**
    
- 📄 **Output Includes**:
  - Extracted Resume & Job Description JSONs
  - ATS compatibility score
  - AI-generated email text
 
  ![Screenshot 2025-06-07 205024](https://github.com/user-attachments/assets/0d9d29bd-d2a3-4525-bee9-0eec3b01ce6e)

    
- 🖼️ **UI Highlights**:
  - Drag-and-drop resume upload
  - Job URL input field
  - Process button with real-time display of results

---


