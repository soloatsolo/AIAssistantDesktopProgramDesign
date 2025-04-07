import openai
from typing import Tuple
import pyttsx3
import speech_recognition as sr
from enum import Enum
from utils.logger import AIAssistantError

class AIState(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    RESPONDING = "responding"
    ERROR = "error"

class AIError(AIAssistantError):
    """Raised when there's an error with AI processing"""
    pass

class AIHandler:
    def __init__(self, api_key: str = None):
        if not api_key:
            raise AIError("OpenAI API key is required")
            
        try:
            self.client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            raise AIError(f"Failed to initialize OpenAI client: {str(e)}")
        
        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
        except Exception as e:
            raise AIError(f"Failed to initialize text-to-speech engine: {str(e)}")
        
        # Initialize STT recognizer
        self.recognizer = sr.Recognizer()
        self.state = AIState.IDLE
        
    async def process_text_input(self, text: str) -> Tuple[str, AIState]:
        """Process text input and return response and emotional state"""
        if not text.strip():
            return "Please provide some input.", AIState.ERROR
            
        try:
            self.state = AIState.PROCESSING
            
            # Call OpenAI API for response
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Keep responses concise and friendly."},
                    {"role": "user", "content": text}
                ]
            )
            
            if not response.choices:
                raise AIError("No response received from AI")
                
            response_text = response.choices[0].message.content
            self.state = AIState.RESPONDING
            
            # TODO: Implement emotion analysis for response
            # For now, always return IDLE state
            return response_text, AIState.IDLE
            
        except openai.AuthenticationError:
            raise AIError("Invalid API key. Please check your OpenAI API key in settings.")
        except openai.RateLimitError:
            raise AIError("API rate limit exceeded. Please try again later.")
        except Exception as e:
            self.state = AIState.ERROR
            raise AIError(f"Error processing input: {str(e)}")
    
    def text_to_speech(self, text: str):
        """Convert text to speech"""
        if not text:
            return
            
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            raise AIError(f"Text-to-speech error: {str(e)}")
    
    def speech_to_text(self) -> str:
        """Convert speech to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            raise AIError("Could not understand audio")
        except sr.RequestError as e:
            raise AIError(f"Speech recognition service error: {str(e)}")
        except Exception as e:
            raise AIError(f"Speech-to-text error: {str(e)}")