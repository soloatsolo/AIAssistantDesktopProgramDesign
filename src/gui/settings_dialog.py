from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QCheckBox, QPushButton, QTabWidget,
                            QSpinBox, QGroupBox, QWidget)
from PyQt6.QtCore import Qt
from utils.config import Config

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # AI Settings Tab
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        
        # API Key group
        api_group = QGroupBox("API Settings")
        api_layout = QVBoxLayout()
        
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("OpenAI API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        api_layout.addLayout(api_key_layout)
        
        model_layout = QHBoxLayout()
        model_label = QLabel("AI Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        api_layout.addLayout(model_layout)
        
        api_group.setLayout(api_layout)
        ai_layout.addWidget(api_group)
        
        # Character Settings Tab
        character_tab = QWidget()
        character_layout = QVBoxLayout(character_tab)
        
        # Character selection
        char_group = QGroupBox("Character Settings")
        char_layout = QVBoxLayout()
        
        gender_layout = QHBoxLayout()
        gender_label = QLabel("Gender:")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["female", "male"])
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combo)
        char_layout.addLayout(gender_layout)
        
        style_layout = QHBoxLayout()
        style_label = QLabel("Style:")
        self.style_combo = QComboBox()
        self.style_combo.addItems(["anime", "cartoon", "realistic"])
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combo)
        char_layout.addLayout(style_layout)
        
        char_group.setLayout(char_layout)
        character_layout.addWidget(char_group)
        
        # Voice Settings Tab
        voice_tab = QWidget()
        voice_layout = QVBoxLayout(voice_tab)
        
        # Voice options
        voice_group = QGroupBox("Voice Settings")
        voice_box_layout = QVBoxLayout()
        
        self.voice_enabled = QCheckBox("Enable Voice")
        voice_box_layout.addWidget(self.voice_enabled)
        
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:")
        self.volume_spin = QSpinBox()
        self.volume_spin.setRange(0, 100)
        self.volume_spin.setSuffix("%")
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_spin)
        voice_box_layout.addLayout(volume_layout)
        
        rate_layout = QHBoxLayout()
        rate_label = QLabel("Speech Rate:")
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(50, 300)
        self.rate_spin.setSingleStep(10)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_spin)
        voice_box_layout.addLayout(rate_layout)
        
        voice_group.setLayout(voice_box_layout)
        voice_layout.addWidget(voice_group)
        
        # Add tabs
        tab_widget.addTab(ai_tab, "AI")
        tab_widget.addTab(character_tab, "Character")
        tab_widget.addTab(voice_tab, "Voice")
        layout.addWidget(tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.load_settings()
        
    def load_settings(self):
        # Load current settings
        self.api_key_input.setText(self.config.get('ai.api_key', ''))
        self.model_combo.setCurrentText(self.config.get('ai.model', 'gpt-4-turbo-preview'))
        
        self.gender_combo.setCurrentText(self.config.get('character.gender', 'female'))
        self.style_combo.setCurrentText(self.config.get('character.style', 'anime'))
        
        self.voice_enabled.setChecked(self.config.get('voice.enabled', True))
        self.volume_spin.setValue(int(self.config.get('voice.volume', 1.0) * 100))
        self.rate_spin.setValue(self.config.get('voice.rate', 150))
        
    def save_settings(self):
        # Save settings to config
        self.config.set('ai.api_key', self.api_key_input.text())
        self.config.set('ai.model', self.model_combo.currentText())
        
        self.config.set('character.gender', self.gender_combo.currentText())
        self.config.set('character.style', self.style_combo.currentText())
        
        self.config.set('voice.enabled', self.voice_enabled.isChecked())
        self.config.set('voice.volume', self.volume_spin.value() / 100.0)
        self.config.set('voice.rate', self.rate_spin.value())
        
        self.config.save_config()
        self.accept()