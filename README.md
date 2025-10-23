# 🎙️ Gemini Language Proficiency Estimator

An AI-powered language proficiency assessment tool that analyzes audio responses using Google's Gemini model. This application evaluates speaker proficiency levels and determines whether responses adequately answer the given questions.

## Features

- **Audio Analysis**: Upload MP3 or WAV files or record directly through the web interface
- **Proficiency Assessment**: AI-powered evaluation of:
  - Pronunciation and clarity
  - Grammar and sentence structure
  - Vocabulary usage and range
  - Fluency and coherence
  - Overall communication effectiveness
- **Content Relevance**: Determines if the response answers the question
- **Modern UI**: Clean, intuitive Gradio interface with real-time feedback
- **Gemini Integration**: Powered by Google's latest Gemini 2.0 Flash model

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

## Usage

1. **Enter a Question**: Type the question that the speaker should be answering
2. **Upload Audio**: Upload an MP3/WAV file or record directly using your microphone
3. **Analyze**: Click "Analyze Response" to get instant feedback
4. **Review Results**: Get detailed proficiency assessment including:
   - Overall proficiency level (Beginner to Proficient)
   - Whether the question was answered
   - Detailed analysis of pronunciation, grammar, vocabulary, and fluency
   - Personalized recommendations for improvement

## Project Structure

```
├── app.py                    # Gradio UI application
├── main.py                   # Application entry point
├── credentials.py            # API key configuration
├── adapters/
│   ├── gemini_adapter.py    # Gemini model integration with audio support
│   ├── openai_adapter.py    # OpenAI integration
│   └── ...
├── utils/
│   └── cloud_storage.py     # Google Cloud Storage utilities
└── pyproject.toml           # Project dependencies
```

## Technical Details

- **Framework**: Gradio 4.0+
- **AI Model**: Google Gemini 2.0 Flash Exp (with audio support)
- **Audio Formats**: MP3, WAV
- **Dependencies**: See `pyproject.toml`

## Troubleshooting

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

## Additional Adapters

This project also includes ready-to-use adapters for:
- OpenAI models
- OpenRouter models
- Google BigQuery
- Firestore
- Google Cloud Storage

## Security Note

⚠️ **Never commit your API key to version control!** The `credentials.py` file is gitignored by default.
