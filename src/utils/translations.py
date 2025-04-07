class Translations:
    STRINGS = {
        "ar": {
            # General
            "settings": "الإعدادات",
            "exit": "خروج",
            "save": "حفظ",
            "cancel": "إلغاء",
            
            # Chat
            "save_chat": "حفظ المحادثة",
            "load_chat": "تحميل محادثة",
            "clear_chat": "مسح المحادثة",
            "chat_saved": "تم حفظ المحادثة بنجاح!",
            "type_message": "اكتب رسالتك هنا...",
            
            # Settings Tabs
            "appearance": "المظهر",
            "ai": "الذكاء الاصطناعي",
            "character": "الشخصية",
            "voice": "الصوت",
            
            # Theme
            "theme": "المظهر",
            "theme_light": "فاتح",
            "theme_dark": "داكن",
            
            # Language
            "language": "اللغة",
            "arabic": "العربية",
            "english": "English",
            
            # Character Settings
            "character_settings": "إعدادات الشخصية",
            "gender": "الجنس",
            "female": "أنثى",
            "male": "ذكر",
            "style": "النمط",
            "anime": "أنمي",
            "cartoon": "كرتون",
            "realistic": "واقعي",
            
            # Voice Settings
            "voice_settings": "إعدادات الصوت",
            "enable_voice": "تفعيل الصوت",
            "volume": "مستوى الصوت",
            "speech_rate": "سرعة النطق",
            
            # AI Settings
            "api_settings": "إعدادات API",
            "openai_api_key": "مفتاح OpenAI API",
            "ai_model": "نموذج الذكاء الاصطناعي",
            
            # Messages
            "confirmation": "تأكيد",
            "clear_confirm": "هل أنت متأكد من رغبتك في مسح المحادثة؟",
            "yes": "نعم",
            "no": "لا",
            "api_key_required": "مطلوب مفتاح API",
            "configure_api_key": "يرجى إعداد مفتاح OpenAI API في الإعدادات لاستخدام المساعد.",
            "error": "خطأ",
            "success": "تم بنجاح",
        },
        "en": {
            # General
            "settings": "Settings",
            "exit": "Exit",
            "save": "Save",
            "cancel": "Cancel",
            
            # Chat
            "save_chat": "Save Chat",
            "load_chat": "Load Chat",
            "clear_chat": "Clear Chat",
            "chat_saved": "Chat history saved successfully!",
            "type_message": "Type your message here...",
            
            # Settings Tabs
            "appearance": "Appearance",
            "ai": "AI",
            "character": "Character",
            "voice": "Voice",
            
            # Theme
            "theme": "Theme",
            "theme_light": "Light",
            "theme_dark": "Dark",
            
            # Language
            "language": "Language",
            "arabic": "Arabic",
            "english": "English",
            
            # Character Settings
            "character_settings": "Character Settings",
            "gender": "Gender",
            "female": "Female",
            "male": "Male",
            "style": "Style",
            "anime": "Anime",
            "cartoon": "Cartoon",
            "realistic": "Realistic",
            
            # Voice Settings
            "voice_settings": "Voice Settings",
            "enable_voice": "Enable Voice",
            "volume": "Volume",
            "speech_rate": "Speech Rate",
            
            # AI Settings
            "api_settings": "API Settings",
            "openai_api_key": "OpenAI API Key",
            "ai_model": "AI Model",
            
            # Messages
            "confirmation": "Confirmation",
            "clear_confirm": "Are you sure you want to clear the chat history?",
            "yes": "Yes",
            "no": "No",
            "api_key_required": "API Key Required",
            "configure_api_key": "Please configure your OpenAI API key in settings to use the assistant.",
            "error": "Error",
            "success": "Success",
        }
    }

    @staticmethod
    def get_string(key: str, language: str = "ar") -> str:
        """Get translated string for the given key and language"""
        try:
            return Translations.STRINGS[language][key]
        except KeyError:
            # Fallback to English if translation not found
            try:
                return Translations.STRINGS["en"][key]
            except KeyError:
                return key