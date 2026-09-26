
# AI Resume Analyzer & ATS Optimizer

An ATS (Applicant Tracking System) resume analyzer built with Python and Streamlit. Upload a resume, paste a target job description, and receive a structured analysis of resume relevance, skill gaps, formatting, and improvement opportunities.

## Live Demo

**[Open AI Resume Analyzer](https://ai-resume-analyzer-ic.streamlit.app/)**

## Features

- **ATS Match Score:** Estimate how closely a resume matches a target job description.
- **Keyword Analysis:** Identify matched skills and missing job-related keywords.
- **Resume Audit:** Review formatting, structure, and ATS compatibility.
- **Bullet Point Rewriter:** Get suggestions to improve resume bullet points.
- **Analysis Report:** Export resume analysis results.
- **Offline Mode:** Use the default ATS analysis without providing an API key.
- **Optional AI Integration:** Configure an AI provider through Advanced AI Settings, if supported by the app.
- **Multiple Formats:** PDF, DOCX, DOC, TXT, and Markdown, subject to the app's installed extraction dependencies.

## How to Use

1. Open the live demo.
2. Upload your resume or load the sample resume.
3. Paste the job description into the target job description box.
4. Click **Analyze Resume Now**.
5. Review the match score, keyword gaps, audit results, and improvement suggestions.
6. Download the analysis report if available.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/ishaanchowdhury1/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run resume_app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

## Project Structure

```text
AI-Resume-Analyzer/
├── resume_app.py       # Streamlit user interface
├── resume_analyzer.py  # Resume analysis engine
├── requirements.txt    # Python dependencies
├── test_app_modes.py   # Application mode tests
├── .devcontainer/      # Development container configuration
├── .gitignore
├── LICENSE
└── README.md
```

## Technology Stack

- Python
- Streamlit
- Resume text extraction and document processing
- Rule-based and keyword-based ATS analysis
- Optional AI integration, depending on configuration

## Important Notes

The ATS match score is an estimate based on the resume content and the supplied job description. It is not an actual employer ATS score or a guarantee of an interview or job offer.

Upload limits and supported document formats depend on the deployed Streamlit configuration and available dependencies. The offline analysis does not require a personal API key.

## Author

**Ishaan Chowdhury**

GitHub: [@ishaanchowdhury1](https://github.com/ishaanchowdhury1)

## License

This project is licensed under the MIT License.
