from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMenu, QMessageBox
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction
from .character_widget import CharacterWidget
from core.ai_handler import AIState, AIHandler
from .settings_dialog import SettingsDialog
from core.system_handler import SystemHandler
from utils.config import Config
from utils.logger import Logger
import qasync
import asyncio
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.config = Config()
        
        # Create UI elements first
        self.setup_ui()
        self.setup_menu()
        
        # Initialize handlers
        try:
            api_key = self.config.get('ai.api_key')
            if not api_key:
                self.logger.warning("No API key found in config")
                self.show_api_key_message()
            self.ai_handler = AIHandler(api_key) if api_key else None
            self.system_handler = SystemHandler()
        except Exception as e:
            self.logger.error(f"Error initializing handlers: {e}")
            self.show_error_message(str(e))
        
    def show_api_key_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("OpenAI API Key Required")
        msg.setInformativeText("Please configure your OpenAI API key in the settings to use the assistant.")
        msg.setWindowTitle("Configuration Required")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.buttonClicked.connect(self.show_settings)
        msg.exec()
    
    def show_error_message(self, error_text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Error")
        msg.setInformativeText(error_text)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        
    def setup_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add character widget
        self.character_widget = CharacterWidget()
        layout.addWidget(self.character_widget)
        
        # Add input field with async connection
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your command...")
        self.input_field.returnPressed.connect(
            partial(qasync.asyncSlot(self._handle_command_async)())
        )
        layout.addWidget(self.input_field)
        
        # Set window position from config
        pos_x = self.config.get('window.position_x', 100)
        pos_y = self.config.get('window.position_y', 100)
        width = self.config.get('window.width', 300)
        height = self.config.get('window.height', 400)
        self.setGeometry(pos_x, pos_y, width, height)
        self.old_pos = None
        
    def setup_menu(self):
        # Create context menu
        self.context_menu = QMenu(self)
        
        # Add actions
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        self.context_menu.addAction(settings_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.context_menu.addAction(exit_action)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
        elif event.button() == Qt.MouseButton.RightButton:
            self.context_menu.popup(event.globalPosition().toPoint())
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = None
            # Save new position to config
            pos = self.pos()
            self.config.set('window.position_x', pos.x())
            self.config.set('window.position_y', pos.y())
            self.config.save_config()
            
    async def _handle_command_async(self):
        """Async handler for processing commands"""
        command = self.input_field.text()
        if not command:
            return
            
        self.input_field.clear()
        
        if not self.ai_handler:
            self.show_api_key_message()
            return
        
        try:
            # Update character state to processing
            self.character_widget.set_state(AIState.PROCESSING)
            
            # Process command through AI
            response, ai_state = await self.ai_handler.process_text_input(command)
            
            # Update character state based on AI response
            if ai_state:
                self.character_widget.set_state(ai_state)
            
            # If voice is enabled, speak the response
            if self.config.get('voice.enabled', True):
                await qasync.asyncio.to_thread(self.ai_handler.text_to_speech, response)
            
            self.logger.info(f"Command processed: {command}")
            
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            self.character_widget.set_state(AIState.ERROR)
            self.show_error_message(str(e))
        
    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            # Reload configuration
            self.config = Config()
            
            # Update AI handler with new API key
            api_key = self.config.get('ai.api_key')
            if api_key:
                self.ai_handler = AIHandler(api_key)
            
            # Update character appearance
            gender = self.config.get('character.gender')
            style = self.config.get('character.style')
            self.character_widget.set_character(gender, style)
            
            # Update voice settings in AI handler
            if hasattr(self.ai_handler, 'tts_engine'):
                volume = self.config.get('voice.volume', 1.0)
                rate = self.config.get('voice.rate', 150)
                self.ai_handler.tts_engine.setProperty('volume', volume)
                self.ai_handler.tts_engine.setProperty('rate', rate)
        
    def closeEvent(self, event):
        # Save window geometry
        geometry = self.geometry()
        self.config.set('window.position_x', geometry.x())
        self.config.set('window.position_y', geometry.y())
        self.config.set('window.width', geometry.width())
        self.config.set('window.height', geometry.height())
        self.config.save_config()
        super().closeEvent(event)