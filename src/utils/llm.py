"""
LLM interface for Amber.txt

Handles communication with language models through OpenRouter.
"""
import json
import requests
from typing import Dict, List, Any, Optional
import logging

from .config import get_openrouter_api_key, get_default_model


class LLMInterface:
    """
    Interface for communicating with language models through OpenRouter.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 default_model: Optional[str] = None,
                 max_tokens: int = 1024,
                 temperature: float = 0.7):
        """
        Initialize the LLM interface.
        
        Args:
            api_key: OpenRouter API key (will use environment variable if None)
            default_model: Default model to use (will use environment variable if None)
            max_tokens: Maximum tokens to generate
            temperature: Temperature parameter for generation
        """
        self.api_key = api_key or get_openrouter_api_key()
        self.default_model = default_model or get_default_model()
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # API endpoint for OpenRouter
        self.api_endpoint = "https://openrouter.ai/api/v1/chat/completions"
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("LLMInterface")
    
    def generate_response(self, 
                          messages: List[Dict[str, str]], 
                          model: Optional[str] = None,
                          system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a response from the language model.
        
        Args:
            messages: List of message objects in the format
                      [{"role": "user", "content": "Hello"}, ...]
            model: Model to use (defaults to self.default_model)
            system_prompt: Optional system prompt to prepend
            
        Returns:
            Response from the language model
        """
        model = model or self.default_model
        
        # Prepare messages, including system prompt if provided
        prepared_messages = []
        
        if system_prompt:
            prepared_messages.append({
                "role": "system",
                "content": system_prompt
            })
            
        prepared_messages.extend(messages)
        
        # Prepare the request payload
        payload = {
            "model": model,
            "messages": prepared_messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Make the API request
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload, 
            timeout=60)
            
            # Check for errors
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            
            # Log usage information
            self._log_usage(result)
            
            return {
                "content": result["choices"][0]["message"]["content"],
                "model": result["model"],
                "usage": result.get("usage", {}),
                "raw_response": result
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return {
                "content": "I'm having trouble connecting to my language model. Please try again later.",
                "error": str(e)
            }
        except (KeyError, IndexError) as e:
            self.logger.error(f"Error parsing API response: {e}")
            return {
                "content": "I received an unexpected response format. Please try again.",
                "error": str(e)
            }
    
    def _log_usage(self, response: Dict[str, Any]) -> None:
        """
        Log usage statistics from API response.
        
        Args:
            response: API response object
        """
        if "usage" in response:
            usage = response["usage"]
            self.logger.info(
                f"LLM Usage - Prompt: {usage.get('prompt_tokens', 0)}, "
                f"Completion: {usage.get('completion_tokens', 0)}, "
                f"Total: {usage.get('total_tokens', 0)}"
            )
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of available models from OpenRouter.
        
        Returns:
            List of model information objects
        """
        # API endpoint for listing models
        models_endpoint = "https://openrouter.ai/api/v1/models"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Make the API request
            response = requests.get(
                models_endpoint,
                headers=headers, 
            timeout=60)
            
            # Check for errors
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            return result.get("data", [])
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch models: {e}")
            return []
