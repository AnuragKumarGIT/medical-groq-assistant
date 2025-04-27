import os
from PIL import Image
import io
from utils.groq_client import GroqClient

class ImageAnalyzer:
    def __init__(self, groq_client):
        """
        Initialize the image analyzer with a Groq client
        """
        self.groq_client = groq_client
        
    def analyze(self, image_file, description=""):
        """
        Analyze a medical image using Groq's vision capabilities
        
        Args:
            image_file: The uploaded image file
            description: Optional user description of the image or symptom
        
        Returns:
            analysis: Text analysis of the medical image
        """
        try:
            # Read the image data
            image_data = image_file.read()
            
            # Create a prompt for the image analysis
            prompt = f"Please analyze this medical image. "
            if description:
                prompt += f"The user describes it as: {description}. "
            prompt += "Provide an assessment of what you see, potential concerns, and appropriate next steps."
            
            # Send to Groq for analysis
            analysis = self.groq_client.analyze_image(image_data, prompt)
            
            # Add medical disclaimer
            disclaimer = "\n\nIMPORTANT: This analysis is preliminary and for informational purposes only. Images may not show all relevant details, and AI analysis is not a substitute for professional medical diagnosis. Please consult with a healthcare provider for proper evaluation."
            
            return analysis + disclaimer
            
        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")
    
    def preprocess_image(self, image_data):
        """
        Preprocess an image before analysis if needed
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Resize if necessary (to meet API requirements)
            max_size = 1024
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size))
            
            # Convert to RGB if in another mode
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save to bytes
            output = io.BytesIO()
            image.save(output, format='JPEG')
            
            return output.getvalue()
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")