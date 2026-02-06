"""
RIFT Standard Library - Cloud Agent Module

Cloud-based agent services for task delegation and AI interactions.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, List


def create_cloud_agent_module(interpreter) -> Dict[str, Any]:
    """Create the cloud agent module for RIFT."""
    
    # ========================================================================
    # Agent Configuration
    # ========================================================================
    
    class AgentConfig:
        """Configuration for cloud agent connections."""
        
        def __init__(self):
            self.providers: Dict[str, Dict[str, Any]] = {}
            self.default_provider: Optional[str] = None
        
        def configure(self, provider: str, config: Dict[str, Any]) -> None:
            """Configure a cloud agent provider."""
            self.providers[provider] = config
            if self.default_provider is None:
                self.default_provider = provider
        
        def get_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
            """Get configuration for a provider."""
            provider = provider or self.default_provider
            if provider not in self.providers:
                raise ValueError(f"Provider '{provider}' not configured")
            return self.providers[provider]
    
    config = AgentConfig()
    
    # ========================================================================
    # HTTP Request Helper
    # ========================================================================
    
    def make_request(url: str, method: str = 'POST', 
                    headers: Optional[Dict[str, str]] = None,
                    data: Optional[Dict[str, Any]] = None,
                    timeout: int = 60) -> Dict[str, Any]:
        """Make HTTP request to cloud service."""
        headers = headers or {}
        headers.setdefault('Content-Type', 'application/json')
        
        request_data = json.dumps(data).encode('utf-8') if data else None
        
        req = urllib.request.Request(
            url,
            data=request_data,
            headers=headers,
            method=method
        )
        
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise RuntimeError(f"HTTP {e.code}: {error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection error: {e.reason}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response: {e}")
    
    # ========================================================================
    # OpenAI Integration
    # ========================================================================
    
    def configure_openai(api_key: str, model: str = "gpt-4") -> None:
        """Configure OpenAI as a cloud agent provider."""
        config.configure('openai', {
            'api_key': api_key,
            'model': model,
            'base_url': 'https://api.openai.com/v1'
        })
    
    def openai_complete(prompt: str, **kwargs) -> str:
        """Send completion request to OpenAI."""
        cfg = config.get_config('openai')
        
        url = f"{cfg['base_url']}/chat/completions"
        headers = {
            'Authorization': f"Bearer {cfg['api_key']}",
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': kwargs.get('model', cfg['model']),
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': kwargs.get('temperature', 0.7),
            'max_tokens': kwargs.get('max_tokens', 1000)
        }
        
        response = make_request(url, headers=headers, data=data)
        return response['choices'][0]['message']['content']
    
    # ========================================================================
    # Anthropic Integration
    # ========================================================================
    
    def configure_anthropic(api_key: str, model: str = "claude-3-5-sonnet-20241022") -> None:
        """Configure Anthropic as a cloud agent provider."""
        config.configure('anthropic', {
            'api_key': api_key,
            'model': model,
            'base_url': 'https://api.anthropic.com/v1'
        })
    
    def anthropic_complete(prompt: str, **kwargs) -> str:
        """Send completion request to Anthropic."""
        cfg = config.get_config('anthropic')
        
        url = f"{cfg['base_url']}/messages"
        headers = {
            'x-api-key': cfg['api_key'],
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': kwargs.get('model', cfg['model']),
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': kwargs.get('max_tokens', 1000)
        }
        
        response = make_request(url, headers=headers, data=data)
        return response['content'][0]['text']
    
    # ========================================================================
    # Generic Agent Interface
    # ========================================================================
    
    def delegate(task: str, provider: Optional[str] = None, **kwargs) -> str:
        """
        Delegate a task to a cloud agent.
        
        Args:
            task: The task description or prompt
            provider: Which provider to use ('openai', 'anthropic', etc.)
            **kwargs: Additional provider-specific options
        
        Returns:
            The agent's response
        """
        provider = provider or config.default_provider
        
        if provider == 'openai':
            return openai_complete(task, **kwargs)
        elif provider == 'anthropic':
            return anthropic_complete(task, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def ask(question: str, context: Optional[str] = None, **kwargs) -> str:
        """
        Ask a question to a cloud agent.
        
        Args:
            question: The question to ask
            context: Optional context for the question
            **kwargs: Additional options
        
        Returns:
            The agent's answer
        """
        prompt = question
        if context:
            prompt = f"Context: {context}\n\nQuestion: {question}"
        
        return delegate(prompt, **kwargs)
    
    def analyze(data: Any, instructions: Optional[str] = None, **kwargs) -> str:
        """
        Ask a cloud agent to analyze data.
        
        Args:
            data: The data to analyze (will be converted to string/JSON)
            instructions: Optional analysis instructions
            **kwargs: Additional options
        
        Returns:
            The agent's analysis
        """
        # Convert data to string representation
        if isinstance(data, dict) or isinstance(data, list):
            data_str = json.dumps(data, indent=2)
        else:
            data_str = str(data)
        
        prompt = f"Analyze the following data:\n\n{data_str}"
        if instructions:
            prompt += f"\n\nInstructions: {instructions}"
        
        return delegate(prompt, **kwargs)
    
    def generate(template: str, variables: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """
        Generate content using a template.
        
        Args:
            template: Template with placeholders
            variables: Variables to fill in the template
            **kwargs: Additional options
        
        Returns:
            Generated content
        """
        if variables:
            for key, value in variables.items():
                template = template.replace(f"{{{key}}}", str(value))
        
        return delegate(template, **kwargs)
    
    def batch_delegate(tasks: List[str], **kwargs) -> List[str]:
        """
        Delegate multiple tasks sequentially.
        
        Args:
            tasks: List of task descriptions
            **kwargs: Additional options
        
        Returns:
            List of responses
        """
        results = []
        for task in tasks:
            result = delegate(task, **kwargs)
            results.append(result)
        return results
    
    # ========================================================================
    # Environment Variable Configuration
    # ========================================================================
    
    def configure_from_env() -> None:
        """Configure providers from environment variables."""
        # OpenAI
        openai_key = os.environ.get('OPENAI_API_KEY')
        if openai_key:
            openai_model = os.environ.get('OPENAI_MODEL', 'gpt-4')
            configure_openai(openai_key, openai_model)
        
        # Anthropic
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        if anthropic_key:
            anthropic_model = os.environ.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
            configure_anthropic(anthropic_key, anthropic_model)
    
    # ========================================================================
    # Module Exports
    # ========================================================================
    
    return {
        # Configuration
        'configure_openai': configure_openai,
        'configure_anthropic': configure_anthropic,
        'configure_from_env': configure_from_env,
        
        # Core functionality
        'delegate': delegate,
        'ask': ask,
        'analyze': analyze,
        'generate': generate,
        'batch': batch_delegate,
        
        # Provider-specific
        'openai': {
            'complete': openai_complete,
            'configure': configure_openai,
        },
        'anthropic': {
            'complete': anthropic_complete,
            'configure': configure_anthropic,
        },
    }
