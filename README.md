# 🎙️ Gemini Language Proficiency Estimator

An AI-powered language proficiency assessment tool that analyzes audio responses using Google's Gemini model. This application evaluates speaker proficiency levels and determines whether responses adequately answer the given questions.

## Evaluation ideas

We could run self-assessment of L2 english/swedish speakers using [CEFR matrix](https://rm.coe.int/CoERMPublicCommonSearchServices/DisplayDCTMContent?documentId=090000168045bb52). Then compare results of self-asssessment to model predictions. 


## Quick Start

### Prerequisites
- Python 3.13+
- Google API Key for Gemini ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/alvalabs/gemini-language-proficiency-estimator.git
cd gemini-language-proficiency-estimator
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Configure your API key:

**Option 1: Environment Variable (Recommended)**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

**Option 2: Edit credentials.py**
```python
GOOGLE_API_KEY = "your-api-key-here"
```

### Running the Application

Start the Gradio web interface:
```bash
python main.py
```

Or directly run the app:
```bash
python app.py
```

The application will be available at: **http://localhost:7860**

### Common Issues

**ModuleNotFoundError: No module named 'gradio'**
- Run `uv sync` to install all dependencies

**Import Error: cannot import name 'GOOGLE_API_KEY'**
- Make sure you've set up `credentials.py` with `GEMINI_API_KEY` (not `GOOGLE_API_KEY`)
- Use the `credentials_template.py` as a reference

**API Errors**
- Verify your API key is valid at https://makersuite.google.com/app/apikey
- Check that you haven't exceeded your API quota
- Ensure the audio file is in a supported format (MP3 or WAV)

**Audio Processing Fails**
- Try a smaller audio file (under 10MB recommended)
- Ensure the audio quality is clear
- Convert the file to MP3 or WAV format if it's in another format
