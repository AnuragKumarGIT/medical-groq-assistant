import os
import groq
import json
import base64

class GroqClient: 
    def __init__(self, api_key=None):
        """
        Initialize the Groq client with API key
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required")
            
        # Updated client initialization without proxies
        from groq import Groq
        self.client = Groq(api_key=self.api_key)
        
        self.llm_model = "llama3-70b-8192"  # Groq's flagship model
        
    def text_completion(self, prompt, system_prompt=None, temperature=0.7):
        """
        Generate text completion using Groq's LLM
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": prompt})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=temperature,
                max_tokens=2048
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error with Groq text completion: {str(e)}")
            
    def analyze_image(self, image_data, prompt):
        """
        Analyze image using Groq's multimodal capabilities
        Note: Implementation depends on Groq's specific API for image analysis
        """
        # For demonstration - actual implementation would use Groq's vision API
        # This is a placeholder that would be updated based on Groq's specific multimodal API
        
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        system_prompt = "You are a medical image analysis assistant. Analyze the uploaded image and provide your assessment."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ]
        
        try:
            # Note: Update this implementation when Groq provides specific multimodal API details
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192-vision",  # Placeholder model name
                messages=messages,
                temperature=0.5,
                max_tokens=1000
            )
            return completion.choices[0].message.content
        except Exception as e:
            # Fallback to text-only analysis if vision model is not available
            return self.text_completion(f"[Image analysis request] {prompt}", 
                                       system_prompt="You are a medical assistant. The user wanted to analyze an image but image analysis is not available. Please explain this limitation politely.")
    
    def transcribe_audio(self, audio_data):
        """
        Transcribe audio using Groq's audio capabilities
        Note: Implementation depends on Groq's specific API for audio processing
        """
        # For demonstration - actual implementation would use Groq's audio API
        # This is a placeholder that would be updated based on Groq's specific audio API
        
        try:
            # Since Groq may not have an audio API yet, we'll return a message
            return "Audio transcription is not currently supported through the Groq API. Please use the text interface instead."
        except Exception as e:
            raise Exception(f"Error with Groq audio transcription: {str(e)}")