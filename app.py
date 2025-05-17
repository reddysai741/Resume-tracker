import streamlit as st
import PyPDF2
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Set page title
st.set_page_config(page_title="Imarticus Learning Login")
background_url = "https://images.unsplash.com/photo-1678227547309-f25998d4fc86?q=80&w=1976&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

# Inject custom CSS for background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main > div {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1.5rem;
        border-radius: 50px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS for styling and positioning
st.markdown(
    """
    <style>
    .header-container {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 2px solid #e6e6e6;
        margin-bottom: 20px;
    }
    .header-container img {
        width: 150px;
        height: auto;
        margin-right: 10px;
    }
    .header-container .title {
        font-size: 24px;
        font-weight: bold;
        color: #262730;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header section: Logo and title side by side
st.markdown(
    """
    <div class="header-container">
        <img src="https://media.istockphoto.com/id/1391720775/photo/woman-using-computer-on-table-with-new-email-message-on-laptop-communication-connection.jpg?s=1024x1024&w=is&k=20&c=hFbvH-9cIoiQbAVp_bz5hwUKSFFH8c4_3m6deRsDDks="alt="Imarticus Logo">
        <div class="title">Smart Resume Matcher with AI-Powered HR Messaging</div>
    </div>
    """,
    unsafe_allow_html=True
)

llm = ChatGroq(
    temperature=0,
    groq_api_key='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',
    model_name="meta-llama/llama-4-scout-17b-16e-instruct"
)

# Initialize variables for later use
json_resume = None
page_data = None

# Vertical page division using columns
col1, col2 = st.columns(2)

# Left column: Resized Illustration
with col1:
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader("Choose your resume", type=["pdf"])

    if resume_file is not None:
        try:
            pdfReader = PyPDF2.PdfReader(resume_file)
            resume_text = ""
            for page in pdfReader.pages:
                content = page.extract_text()
                if content:
                    resume_text += content

            if not resume_text.strip():
                st.warning("No readable text found in the resume.")
            else:
                st.success("✅ Resume content extracted successfully!")
                st.text_area("Extracted Resume Text", resume_text, height=250)

                prompt_extract = PromptTemplate.from_template(
                    """
                    ### SCRAPED TEXT FROM WEBSITE:
                    {pagecontent}
                    ### INSTRUCTION:
                    i will give my resume from that extract the name,experience but in this dont take description ,techincal skills in jason format , No preamble
                    Only return the valid JSON.
                    ### VALID JSON (NO PREAMBLE):
                    """
                )

                chain_extract = prompt_extract | llm
                resume = chain_extract.invoke(input={'pagecontent': resume_text})

                st.write("🧠 LLM Raw Output:")
                st.code(resume.content)

                try:
                    json_parser = JsonOutputParser()
                    json_resume = json_parser.parse(resume.content)

                except Exception as e:
                    st.error(f"⚠️ Failed to parse JSON with LangChain parser: {e}")

        except Exception as e:
            st.error(f"❌ Error reading resume: {e}")

# Right column: Additional content
with col2:
    st.subheader("🔗 Job Description Link")
    job_link = st.text_input("Paste the job description URL")

    if job_link:
        try:
            st.info("⏳ Loading job data from URL...")
            loader = WebBaseLoader(job_link)
            page_data = loader.load().pop().page_content

            st.success("✅ Job description scraped successfully.")
            st.text_area("Scraped Job Description", page_data[:3000], height=250)

            prompt_extract = PromptTemplate.from_template(
                """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_data}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your job is to extract the job postings and return them in JSON format containing the
                following keys: `role`, `experience`, `skills` and `description`.
                Only return the valid JSON.
                ### VALID JSON (NO PREAMBLE):
                """
            )

            chain_extract = prompt_extract | llm
            job = chain_extract.invoke(input={'page_data': page_data})
            st.write("🧠 LLM Raw Job Output:")
            st.code(job.content)

            json_parser = JsonOutputParser()
            json_job = json_parser.parse(job.content)

        except Exception as e:
            st.error(f"❌ Error processing job description: {e}")

if json_resume and page_data:
    try:
        email_prompt = PromptTemplate.from_template("""
        You are a professional email writer.

        Based on the following resume details and job description, write a formal job application email to apply for the job. Keep it polite, confident, and concise.

        ### RESUME DETAILS (JSON):
        {resume_json}

        ### JOB DESCRIPTION:
        {job_text}

        Write a complete email with a subject line, greeting, body, and a closing with the candidate’s name.
        """)

        email_chain = email_prompt | llm
        email_response = email_chain.invoke({
            "resume_json": json_resume,
            "job_text": page_data
        })

        st.subheader("📧 AI-Generated Email to HR")
        st.text_area("Generated Email", value=email_response.content, height=300)

    except Exception as e:
        st.error(f"Error generating email: {e}")
