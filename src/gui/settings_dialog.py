from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QCheckBox, QPushButton, QTabWidget,
                            QSpinBox, QGroupBox, QWidget)
from PyQt6.QtCore import Qt
from utils.config import Config
from utils.translations import Translations

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.tr = lambda key: Translations.get_string(key, self.config.get('appearance.language', 'ar'))
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        self.setWindowTitle(self.tr("settings"))
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Add Appearance Tab
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout(appearance_tab)
        
        # Theme selection
        theme_group = QGroupBox(self.tr("theme"))
        theme_layout = QHBoxLayout()
        theme_label = QLabel(self.tr("theme") + ":")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([self.tr("theme_light"), self.tr("theme_dark")])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)
        appearance_layout.addWidget(theme_group)
        
        # Language selection
        lang_group = QGroupBox(self.tr("language"))
        lang_layout = QHBoxLayout()
        lang_label = QLabel(self.tr("language") + ":")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([self.tr("arabic"), self.tr("english")])
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        appearance_layout.addWidget(lang_group)
        
        # AI Settings Tab
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        
        # API Key group
        api_group = QGroupBox(self.tr("api_settings"))
        api_layout = QVBoxLayout()
        
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel(self.tr("openai_api_key") + ":")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        api_layout.addLayout(api_key_layout)
        
        model_layout = QHBoxLayout()
        model_label = QLabel(self.tr("ai_model") + ":")
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
        char_group = QGroupBox(self.tr("character_settings"))
        char_layout = QVBoxLayout()
        
        gender_layout = QHBoxLayout()
        gender_label = QLabel(self.tr("gender") + ":")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems([self.tr("female"), self.tr("male")])
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combo)
        char_layout.addLayout(gender_layout)
        
        style_layout = QHBoxLayout()
        style_label = QLabel(self.tr("style") + ":")
        self.style_combo = QComboBox()
        self.style_combo.addItems([self.tr("anime"), self.tr("cartoon"), self.tr("realistic")])
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combo)
        char_layout.addLayout(style_layout)
        
        char_group.setLayout(char_layout)
        character_layout.addWidget(char_group)
        
        # Voice Settings Tab
        voice_tab = QWidget()
        voice_layout = QVBoxLayout(voice_tab)
        
        # Voice options
        voice_group = QGroupBox(self.tr("voice_settings"))
        voice_box_layout = QVBoxLayout()
        
        self.voice_enabled = QCheckBox(self.tr("enable_voice"))
        voice_box_layout.addWidget(self.voice_enabled)
        
        volume_layout = QHBoxLayout()
        volume_label = QLabel(self.tr("volume") + ":")
        self.volume_spin = QSpinBox()
        self.volume_spin.setRange(0, 100)
        self.volume_spin.setSuffix("%")
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_spin)
        voice_box_layout.addLayout(volume_layout)
        
        rate_layout = QHBoxLayout()
        rate_label = QLabel(self.tr("speech_rate") + ":")
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(50, 300)
        self.rate_spin.setSingleStep(10)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_spin)
        voice_box_layout.addLayout(rate_layout)
        
        voice_group.setLayout(voice_box_layout)
        voice_layout.addWidget(voice_group)
        
        # Add tabs
        tab_widget.addTab(ai_tab, self.tr("ai"))
        tab_widget.addTab(character_tab, self.tr("character"))
        tab_widget.addTab(voice_tab, self.tr("voice"))
        tab_widget.addTab(appearance_tab, self.tr("appearance"))
        layout.addWidget(tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton(self.tr("save"))
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton(self.tr("no"))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.load_settings()
    
    def apply_theme(self):
        theme = self.config.get('appearance.theme', 'light')
        if theme == 'dark':
            self.setStyleSheet("""
                QDialog, QWidget {
                    background-color: #2c2c2c;
                    color: #ffffff;
                }
                QGroupBox {
                    border: 1px solid #555555;
                    margin-top: 0.5em;
                }
                QComboBox, QLineEdit, QSpinBox {
                    background-color: #3c3c3c;
                    color: #ffffff;
                    border: 1px solid #555555;
                }
                QPushButton {
                    background-color: #444444;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 5px 15px;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
            """)
        else:
            self.setStyleSheet("")  # Use default light theme
        
    def load_settings(self):
        # Load current settings
        self.theme_combo.setCurrentText(
            self.tr("theme_dark") if self.config.get('appearance.theme') == 'dark' 
            else self.tr("theme_light")
        )
        self.lang_combo.setCurrentText(
            self.tr("arabic") if self.config.get('appearance.language') == 'ar'
            else self.tr("english")
        )
        self.api_key_input.setText(self.config.get('ai.api_key', ''))
        self.model_combo.setCurrentText(self.config.get('ai.model', 'gpt-4-turbo-preview'))
        
        self.gender_combo.setCurrentText(self.config.get('character.gender', self.tr('female')))
        self.style_combo.setCurrentText(self.config.get('character.style', self.tr('anime')))
        
        self.voice_enabled.setChecked(self.config.get('voice.enabled', True))
        self.volume_spin.setValue(int(self.config.get('voice.volume', 1.0) * 100))
        self.rate_spin.setValue(self.config.get('voice.rate', 150))
        
    def save_settings(self):
        # Save appearance settings
        self.config.set('appearance.theme', 
                       'dark' if self.theme_combo.currentText() == self.tr("theme_dark")
                       else 'light')
        self.config.set('appearance.language',
                       'ar' if self.lang_combo.currentText() == self.tr("arabic")
                       else 'en')
        
        self.config.set('ai.api_key', self.api_key_input.text())
        self.config.set('ai.model', self.model_combo.currentText())
        
        self.config.set('character.gender', self.gender_combo.currentText())
        self.config.set('character.style', self.style_combo.currentText())
        
        self.config.set('voice.enabled', self.voice_enabled.isChecked())
        self.config.set('voice.volume', self.volume_spin.value() / 100.0)
        self.config.set('voice.rate', self.rate_spin.value())
        
        self.config.save_config()
        self.accept()