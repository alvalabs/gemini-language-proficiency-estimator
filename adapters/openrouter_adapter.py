import json
import requests
from typing import Dict, List, Optional

class OpenRouterAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek/deepseek-r1",
        max_tokens: Optional[int] = None,
    ) -> Dict:
        """
        Send a chat completion request to DeepSeek R1 via OpenRouter API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model identifier 
            max_tokens: Maximum tokens to generate
        
        Returns:
            API response as a dictionary
        """
        payload = {
            "model": model,
            "messages": messages
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=300
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")
            
        return response.json()['choices'][0]['message']['content']

