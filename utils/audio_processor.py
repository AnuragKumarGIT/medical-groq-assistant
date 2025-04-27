import os
import io
# Python 3.13 compatibility - use aifc replacement
try:
    import aifc # type: ignore
except ModuleNotFoundError:
    # For Python 3.13+, we need a workaround as aifc was removed
    from audioread import audio_open
    import wave

import speech_recognition as sr
from pydub import AudioSegment


class AudioProcessor:
    def __init__(self, groq_client):
        """
        Initialize the audio processor with a Groq client
        """
        self.groq_client = groq_client
        self.recognizer = sr.Recognizer()
        
    def transcribe(self, audio_path):
        """
        Transcribe audio file to text using either Groq's audio API or fallback
        
        Args:
            audio_path: Path to the temporary audio file
        
        Returns:
            text: Transcribed text from the audio
        """
        try:
            # First try using Groq's native audio transcription if available
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
                
            try:
                # Try using Groq's audio API
                transcription = self.groq_client.transcribe_audio(audio_data)
                return transcription
            except Exception as e:
                # Fall back to local transcription with SpeechRecognition
                return self._fallback_transcribe(audio_path)
                
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
    
    def _fallback_transcribe(self, audio_path):
        """
        Fallback method for audio transcription using SpeechRecognition library
        Compatible with Python 3.13.3
        """
        try:
            # Convert to WAV if not already in that format
            audio = AudioSegment.from_file(audio_path)
            
            # If not WAV, convert to WAV
            if not audio_path.lower().endswith('.wav'):
                wav_path = "temp_converted.wav"
                audio.export(wav_path, format="wav")
                audio_path = wav_path
            
            # Python 3.13+ compatible audio processing
            # Use a custom approach for Python 3.13 that doesn't depend on aifc
            recognized_text = ""
            
            # Use SpeechRecognition with direct file handling
            with open(audio_path, 'rb') as audio_file:
                # Create a temporary file-like object in memory
                audio_data = audio_file.read()
                audio_io = io.BytesIO(audio_data)
                
                # Use the recognizer directly with the audio data
                audio_source = sr.AudioData(audio_data, 
                                           sample_rate=16000,  # Common sample rate
                                           sample_width=2)     # 16-bit audio
                recognized_text = self.recognizer.recognize_google(audio_source)
            
            # Clean up temporary file if created
            if audio_path == "temp_converted.wav" and os.path.exists(audio_path):
                os.remove(audio_path)
                
            return recognized_text
            
        except Exception as e:
            # More detailed error reporting
            import traceback
            error_details = traceback.format_exc()
            raise Exception(f"Fallback transcription failed: {str(e)}\nDetails: {error_details}")
    
    def text_to_speech(self, text):
        """
        Convert text to speech (placeholder for future implementation)
        
        This functionality would be implemented when Groq provides a text-to-speech API
        """
        # Placeholder for future implementation
        pass