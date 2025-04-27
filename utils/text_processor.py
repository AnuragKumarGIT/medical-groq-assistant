from utils.groq_client import GroqClient
from models.medical_knowledge import medical_disclaimers

class TextProcessor:
    def __init__(self, groq_client):
        """
        Initialize the text processor with a Groq client
        """
        self.groq_client = groq_client
        self.system_prompt = """
        You are MediGroq, a medical assistant AI powered by Groq. You provide helpful, accurate medical information and preliminary advice based on symptoms described.

        Guidelines:
        1. Provide clear, concise, and accurate medical information
        2. Consider differential diagnoses for symptom descriptions
        3. Always include proper disclaimers about seeking professional medical advice
        4. When uncertain, be clear about limitations
        5. Format responses in an easily readable way
        6. Avoid technical jargon when possible, or explain terms when used
        7. Be empathetic and compassionate in responses
        8. Focus on evidence-based medical information
        
        Remember: Your purpose is to provide preliminary information only, not to diagnose or replace medical professionals.
        """
    
    def process(self, text_query):
        """
        Process a text query about medical concerns
        """
        try:
            # Add context and format the user query
            formatted_query = f"User medical query: {text_query}\n\nProvide a helpful, accurate, and compassionate response."
            
            # Get response from Groq
            response = self.groq_client.text_completion(
                prompt=formatted_query,
                system_prompt=self.system_prompt,
                temperature=0.5
            )
            
            # Ensure medical disclaimer is included
            if not any(disclaimer in response for disclaimer in medical_disclaimers):
                response += "\n\n" + medical_disclaimers[0]
                
            return response
        except Exception as e:
            raise Exception(f"Error processing text: {str(e)}")
    
    def categorize_query(self, text):
        """
        Categorize the medical query type (symptoms, condition info, medication, etc.)
        """
        categorization_prompt = f"""
        Categorize the following medical query into one of these categories:
        - Symptom Analysis
        - Condition Information
        - Medication Question
        - Lifestyle/Prevention
        - Emergency Guidance
        - General Medical Question
        
        Query: {text}
        
        Category:
        """
        
        try:
            category = self.groq_client.text_completion(
                prompt=categorization_prompt,
                temperature=0.3
            ).strip()
            
            return category
        except Exception:
            # Default category if categorization fails
            return "General Medical Question"