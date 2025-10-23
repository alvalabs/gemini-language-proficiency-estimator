import openai
from typing import List, Dict 

class OpenAIAdapter:
    def __init__(self, api_key: str):
        """Initialize the OpenAI adapter with API key."""
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "o3-mini",
        reasoning_effort: str = "medium"
    ) -> str:
        """
        Generate a completion using OpenAI's API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: The model to use (default: o3-mini)
            reasoning_effort: The effort to use (default: medium)   
        
        Returns:
            The generated response text
        """
        try:
            completion = self.client.chat.completions.create(
                model=model,
                reasoning_effort=reasoning_effort,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating completion: {str(e)}")