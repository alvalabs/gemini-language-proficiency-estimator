from typing import List, Optional, Tuple
import google.generativeai as genai
import json
import time
import mimetypes

class GeminiAdapter:
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,  # Increased from default
        json_schema: Optional[dict] = None,
    ):
        """Initialize the Gemini adapter.
        
        Args:
            api_key: Google API key for authentication
            model_name: Name of the Gemini model to use
            temperature: Controls randomness in responses (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
        """
        # Initialize Gemini client
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        self.generation_config = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_tokens
        }
        if json_schema:
            self.generation_config["response_mime_type"] = "application/json"
            self.generation_config["response_schema"] = json_schema

        self.model = genai.GenerativeModel(self.model_name, system_instruction=self.system_prompt)

    def generate(self, prompt: str) -> Tuple[str, dict]:
        """Generate a response from the Gemini model.
        Args:
            prompt: Input text prompt
            
        Returns:
            Generated text response
        """
        
        response = self.model.generate_content(
            contents=prompt,
            generation_config=self.generation_config,
        )
        return response.text, response.usage_metadata

    def generate_with_audio(self, prompt: str, audio_file_path: str) -> Tuple[str, dict]:
        """Generate a response from the Gemini model with audio input.
        Args:
            prompt: Input text prompt
            audio_file_path: Path to the audio file (MP3, WAV, or M4A)
            
        Returns:
            Tuple of (generated text response, usage metadata)
        """
        try:
            print(f"Reading audio file: {audio_file_path}")
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(audio_file_path)
            if not mime_type:
                if audio_file_path.lower().endswith('.mp3'):
                    mime_type = 'audio/mpeg'
                elif audio_file_path.lower().endswith('.wav'):
                    mime_type = 'audio/wav'
                elif audio_file_path.lower().endswith('.m4a'):
                    mime_type = 'audio/mp4'
                else:
                    mime_type = 'audio/mpeg'  # default
            
            print(f"MIME type: {mime_type}")
            
            # Read the audio file as bytes
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            print(f"File size: {len(audio_data)} bytes")
            
            # Combine system prompt with user prompt if system prompt exists
            full_prompt = prompt
            if self.system_prompt:
                full_prompt = f"{self.system_prompt}\n\n{prompt}"
            
            # Create generation config with higher token limit
            audio_gen_config = {
                "temperature": self.temperature if self.temperature is not None else 0.3,
                "max_output_tokens": 4096,  # Increased token limit
                "top_p": 0.95,  # Controls diversity of output
                "top_k": 40,    # Number of highest probability tokens to consider
            }
            
            # For audio, create a model without system_instruction to avoid conflicts
            audio_model = genai.GenerativeModel(
                self.model_name,
                generation_config=audio_gen_config,
            )
            
            print(f"Generating content with model: {self.model_name}")
            
            # Generate content with inline audio data
            response = audio_model.generate_content(
                [
                    full_prompt,
                    {
                        "mime_type": mime_type,
                        "data": audio_data
                    }
                ]
            )
            
            # Get the full response text
            if hasattr(response, 'text'):
                result_text = response.text
            else:
                # Fallback to getting text from parts if .text doesn't work
                result_text = ""
                if hasattr(response, 'candidates') and response.candidates:
                    for candidate in response.candidates:
                        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                            for part in candidate.content.parts:
                                if hasattr(part, 'text'):
                                    result_text += part.text + "\n"
            
            print("Content generated successfully")
            print(f"Response length: {len(result_text)} characters")
            
            return result_text.strip(), getattr(response, 'usage_metadata', {})
            
        except Exception as e:
            print(f"Error in generate_with_audio: {type(e).__name__}: {str(e)}")
            raise
