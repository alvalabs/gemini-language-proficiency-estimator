from typing import List, Optional, Tuple
import google.generativeai as genai
import json

class GeminiAdapter:
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.0-flash-001",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
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
