import gradio as gr
from adapters.gemini_adapter import GeminiAdapter
from credentials import GEMINI_API_KEY

# Available languages for assessment
LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Dutch",
    "Russian",
    "Chinese (Mandarin)",
    "Japanese",
    "Korean",
    "Arabic",
    "Hindi",
    "Swedish",
    "Norwegian",
    "Danish",
    "Finnish",
    "Polish",
    "Turkish",
    "Vietnamese",
    "Thai",
    "Indonesian",
]

def get_system_prompt(language: str) -> str:
    """Generate system prompt for a specific target language."""
    return f"""You are an expert language assessment evaluator. Your task is to:

1. Listen to the audio response provided by the speaker speaking in {language}. 
2. Analyze the speaker's {language} language proficiency level based on:
   - Pronunciation and clarity
   - Grammar and sentence structure
   - Vocabulary usage and range
   - Fluency and coherence
   - Overall communication effectiveness

3. Output a lower and upper bound for the speaker's proficiency level (CEFR) based on the analysis.

4. Determine if the speaker's response actually answers the question that was asked

5. Provide your assessment in the following format:
   
   **Lower bound for proficiency level (CEFR):**[A1(beginner)/A2(elementary)/B1(intermediate)/B2(upper intermediate)/C1(advanced)/C2(mastery)]

   **Upper bound for proficiency level (CEFR):**[A1(beginner)/A2(elementary)/B1(intermediate)/B2(upper intermediate)/C1(advanced)/C2(mastery)]


   
   **Detailed Analysis:**
   - Pronunciation: [Your assessment]
   - Grammar: [Your assessment]
   - Vocabulary: [Your assessment]
   - Fluency: [Your assessment]
   - Content Relevance: [Your assessment]
   
Be specific, constructive, and objective in your assessment.
"""

def analyze_audio_response(question: str, audio_file, target_language: str) -> str:
    """
    Analyze an audio response for language proficiency and relevance.
    
    Args:
        question: The question that was asked
        audio_file: The audio file path from Gradio
        target_language: The language to assess proficiency in
        
    Returns:
        Analysis results as formatted text
    """
    if not question or not question.strip():
        return "⚠️ **Error:** Please provide a question."
    if audio_file is None:
        return "⚠️ **Error:** Please upload an audio file."
    
    try:
        # Generate system prompt with target language
        system_prompt = get_system_prompt(target_language)
        
        # Initialize Gemini adapter with system prompt
        gemini = GeminiAdapter(
            api_key=GEMINI_API_KEY,
            model_name="gemini-2.5-flash",
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for more consistent assessments
            max_tokens=2048
        )
        analysis_prompt = f"""
Please analyze the {target_language} audio response to the following question:

**Question:** {question}

**Target Language:** {target_language}

Listen to the audio carefully and provide a comprehensive assessment of the speaker's {target_language} language proficiency and whether they adequately answered the question.
"""
        
        # Generate analysis with audio
        result, metadata = gemini.generate_with_audio(
            prompt=analysis_prompt,
            audio_file_path=audio_file
        )
        
        return result
        
    except ValueError as e:
        return f"⚠️ **File Processing Error:**\n\n{str(e)}\n\nPlease ensure the audio file is in a supported format (MP3, WAV, M4A)."
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "authentication" in error_msg.lower():
            return f"⚠️ **Authentication Error:**\n\n{error_msg}\n\nPlease check that your GEMINI_API_KEY is set correctly in credentials.py"
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return f"⚠️ **Rate Limit Error:**\n\n{error_msg}\n\nYou may have exceeded your API quota. Please try again later."
        else:
            return f"⚠️ **Error occurred during analysis:**\n\n{error_msg}\n\nPlease check your API key and audio file format."

# Create Gradio interface
with gr.Blocks(title="Language Proficiency Estimator", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎙️ Language Proficiency Estimator
        
        Upload an audio response (MP3, WAV, or M4A) and receive an AI-powered assessment of language proficiency 
        and content relevance using Google's Gemini model.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Input")
            
            language_dropdown = gr.Dropdown(
                choices=LANGUAGES,
                value="English",
                label="Target Language",
                info="Select the language to assess proficiency in"
            )
            
            question_input = gr.Textbox(
                label="Question",
                placeholder="Enter the question that was asked...",
                lines=3,
                info="What question should the speaker be answering?"
            )
            
            audio_input = gr.Audio(
                label="Audio Response",
                type="filepath",
                sources=["upload", "microphone"]
            )
            
            analyze_btn = gr.Button("🔍 Analyze Response", variant="primary", size="lg")
            
            gr.Markdown(
                """
                ### ℹ️ Tips
                - Provide a clear question for context
                - Ensure audio quality is good
                - Supported formats: MP3, WAV, M4A
                """
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Analysis Results")
            output = gr.Markdown(
                label="Assessment",
                value="*Results will appear here after analysis...*"
            )
    
    # Examples section
    gr.Markdown("### 💡 Example Questions")
    gr.Examples(
        examples=[
            ["Tell me about your favorite hobby and why you enjoy it."],
            ["Describe your last vacation. Where did you go and what did you do?"],
            ["What are your career goals for the next five years?"],
            ["Explain how climate change affects our daily lives."],
        ],
        inputs=question_input,
        label="Click to use example questions"
    )
    
    # Connect the button to the function
    analyze_btn.click(
        fn=analyze_audio_response,
        inputs=[question_input, audio_input, language_dropdown],
        outputs=output
    )

def launch_app():
    """Launch the Gradio application."""
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    launch_app()
