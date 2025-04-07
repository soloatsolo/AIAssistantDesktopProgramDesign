import openai
from typing import Tuple, List, Dict
import pyttsx3
import speech_recognition as sr
from enum import Enum
from utils.logger import AIAssistantError
from textblob import TextBlob
import json
from datetime import datetime
import hashlib
import os
import pickle
import nltk
import threading

class AIState(Enum):
    IDLE = "idle"
    HAPPY = "happy"
    SAD = "sad"
    CONFUSED = "confused"
    THINKING = "thinking"
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
            
        # Initialize NLTK data
        self._initialize_nltk()
            
        try:
            self.client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            raise AIError(f"Failed to initialize OpenAI client: {str(e)}")
        
        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
        except Exception as e:
            raise AIError(f"Failed to initialize text-to-speech engine: {str(e)}")
        
        # Initialize STT recognizer with noise adjustment
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000
        self.is_listening = False
        
        self.state = AIState.IDLE
        
        self.conversation_history: List[Dict] = []
        self.max_history_length = 10  # Keep last 10 exchanges
        
        # Initialize response cache
        self.cache_dir = os.path.join('cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, 'response_cache.pkl')
        self.load_cache()
        
    def _initialize_nltk(self):
        """Initialize NLTK data required for TextBlob"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading required NLTK data...")
            nltk.download('punkt', quiet=True)
            
    def start_listening(self) -> None:
        """Start background listening for speech"""
        if not self.is_listening:
            self.is_listening = True
            threading.Thread(target=self._listen_continuously, daemon=True).start()
            
    def stop_listening(self) -> None:
        """Stop background listening"""
        self.is_listening = False
        
    def _listen_continuously(self) -> None:
        """Continuous listening function for background thread"""
        while self.is_listening:
            try:
                text = self.speech_to_text()
                if text:
                    # Process the recognized text
                    print(f"Recognized: {text}")
                    # Here you could emit a signal or use a callback
            except Exception as e:
                print(f"Listening error: {e}")
                continue
    
    def load_cache(self):
        """Load response cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    self.response_cache = pickle.load(f)
            else:
                self.response_cache = {}
        except Exception:
            self.response_cache = {}
            
    def save_cache(self):
        """Save response cache to file"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.response_cache, f)
        except Exception as e:
            print(f"Error saving cache: {e}")
            
    def get_cache_key(self, text: str, context: List[Dict]) -> str:
        """Generate a cache key from input text and context"""
        # Create a string that includes the input and relevant context
        context_str = ""
        if context:
            # Only include the last 2 exchanges for cache key
            recent_context = context[-4:]
            context_str = json.dumps([
                {'role': msg['role'], 'content': msg['content']}
                for msg in recent_context
            ])
            
        # Combine input and context
        combined = f"{text}|{context_str}"
        
        # Generate hash
        return hashlib.md5(combined.encode()).hexdigest()
        
    async def process_text_input(self, text: str) -> Tuple[str, AIState]:
        """Process text input and return response and emotional state"""
        if not text.strip():
            return "Please provide some input.", AIState.ERROR
            
        try:
            self.state = AIState.PROCESSING
            
            # Check cache first
            cache_key = self.get_cache_key(text, self.conversation_history)
            if cache_key in self.response_cache:
                cached_response = self.response_cache[cache_key]
                # Add to conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": text,
                    "timestamp": datetime.now().isoformat()
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": cached_response,
                    "timestamp": datetime.now().isoformat(),
                    "cached": True
                })
                
                # Analyze sentiment and return
                sentiment = TextBlob(cached_response).sentiment.polarity
                state = self._get_state_from_sentiment(sentiment, cached_response)
                return cached_response, state
            
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": text,
                "timestamp": datetime.now().isoformat()
            })
            
            # Prepare conversation context
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Keep responses concise and friendly."}
            ]
            
            # Add relevant history (last few exchanges)
            history_start = max(0, len(self.conversation_history) - self.max_history_length)
            for msg in self.conversation_history[history_start:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Call OpenAI API for response
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages
            )
            
            if not response.choices:
                raise AIError("No response received from AI")
                
            response_text = response.choices[0].message.content
            
            # Cache the response
            self.response_cache[cache_key] = response_text
            self.save_cache()
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
            
            # Trim history if too long
            if len(self.conversation_history) > self.max_history_length * 2:
                self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
            
            self.state = AIState.RESPONDING
            
            # Analyze emotion in response
            sentiment = TextBlob(response_text).sentiment.polarity
            state = self._get_state_from_sentiment(sentiment, response_text)
            
            return response_text, state
            
        except openai.AuthenticationError:
            raise AIError("Invalid API key. Please check your OpenAI API key in settings.")
        except openai.RateLimitError:
            raise AIError("API rate limit exceeded. Please try again later.")
        except Exception as e:
            self.state = AIState.ERROR
            raise AIError(f"Error processing input: {str(e)}")
    
    def _get_state_from_sentiment(self, sentiment: float, text: str) -> AIState:
        """Determine AI state based on sentiment and text content"""
        if sentiment > 0.3:
            return AIState.HAPPY
        elif sentiment < -0.3:
            return AIState.SAD
        elif "?" in text or "not sure" in text.lower():
            return AIState.CONFUSED
        else:
            return AIState.IDLE
    
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
        """Convert speech to text with improved error handling"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                
                try:
                    # Set timeout and phrase time limit
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    return ""
                
                try:
                    # Try with Google's speech recognition first
                    text = self.recognizer.recognize_google(audio, language="ar-AR")
                    return text
                except sr.UnknownValueError:
                    return ""
                except sr.RequestError:
                    # Fallback to offline recognition if available
                    try:
                        text = self.recognizer.recognize_sphinx(audio, language="ar")
                        return text
                    except:
                        raise AIError("Speech recognition services unavailable")
                        
        except Exception as e:
            raise AIError(f"Speech-to-text error: {str(e)}")
            
    def save_conversation_history(self, filepath: str):
        """Save conversation history to a JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise AIError(f"Failed to save conversation history: {str(e)}")
            
    def load_conversation_history(self, filepath: str):
        """Load conversation history from a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
        except Exception as e:
            raise AIError(f"Failed to load conversation history: {str(e)}")
            
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []