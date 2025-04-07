from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMenu, QMessageBox, QTextBrowser, QFileDialog
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
        
        # Add chat display with improved styling
        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 15px;
                padding: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                border: 1px solid rgba(200, 200, 200, 100);
            }
            QTextBrowser:hover {
                background-color: rgba(255, 255, 255, 220);
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(200, 200, 200, 50);
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(140, 140, 140, 150);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(140, 140, 140, 200);
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Improved input field styling
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("اكتب رسالتك هنا...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 14px;
                border: 1px solid rgba(200, 200, 200, 100);
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 240);
                border: 1px solid rgba(140, 68, 173, 150);
            }
        """)
        self.input_field.returnPressed.connect(
            partial(qasync.asyncSlot(self._handle_command_async)())
        )
        layout.addWidget(self.input_field)
        
        # Buttons container with improved styling
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.save_chat_btn = QPushButton("💾 حفظ المحادثة")
        self.save_chat_btn.clicked.connect(self.save_chat_history)
        self.save_chat_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(140, 68, 173, 180);
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(140, 68, 173, 220);
            }
            QPushButton:pressed {
                background-color: rgba(140, 68, 173, 250);
                padding: 9px 14px 7px 16px;
            }
        """)
        buttons_layout.addWidget(self.save_chat_btn)
        
        self.clear_chat_btn = QPushButton("🗑️ مسح")
        self.clear_chat_btn.clicked.connect(self.clear_chat_history)
        self.clear_chat_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(231, 76, 60, 180);
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(231, 76, 60, 220);
            }
            QPushButton:pressed {
                background-color: rgba(231, 76, 60, 250);
                padding: 9px 14px 7px 16px;
            }
        """)
        buttons_layout.addWidget(self.clear_chat_btn)
        
        layout.addLayout(buttons_layout)
        
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
        
        # Add chat history actions
        self.context_menu.addSeparator()
        save_chat_action = QAction("Save Chat History", self)
        save_chat_action.triggered.connect(self.save_chat_history)
        self.context_menu.addAction(save_chat_action)
        
        load_chat_action = QAction("Load Chat History", self)
        load_chat_action.triggered.connect(self.load_chat_history)
        self.context_menu.addAction(load_chat_action)
        
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
            
            # Add user message to chat display
            self.chat_display.append(f"<p style='color: #2c3e50'><b>You:</b> {command}</p>")
            
            # Process command through AI
            response, ai_state = await self.ai_handler.process_text_input(command)
            
            # Add AI response to chat display
            self.chat_display.append(f"<p style='color: #8e44ad'><b>Assistant:</b> {response}</p>")
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )
            
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
            
    def save_chat_history(self):
        """Save chat history to a file"""
        if not self.ai_handler:
            return
            
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Chat History",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if filename:
                if not filename.endswith('.json'):
                    filename += '.json'
                self.ai_handler.save_conversation_history(filename)
                QMessageBox.information(
                    self,
                    "Success",
                    "Chat history saved successfully!"
                )
        except Exception as e:
            self.show_error_message(f"Error saving chat history: {str(e)}")
            
    def load_chat_history(self):
        """Load chat history from a file"""
        if not self.ai_handler:
            return
            
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Load Chat History",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if filename:
                self.ai_handler.load_conversation_history(filename)
                self.refresh_chat_display()
        except Exception as e:
            self.show_error_message(f"Error loading chat history: {str(e)}")
            
    def clear_chat_history(self):
        """Clear chat history"""
        if not self.ai_handler:
            return
            
        reply = QMessageBox.question(
            self,
            "Clear Chat History",
            "Are you sure you want to clear the chat history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.ai_handler.clear_conversation_history()
            self.chat_display.clear()
            
    def refresh_chat_display(self):
        """Refresh the chat display with current conversation history"""
        self.chat_display.clear()
        if not self.ai_handler:
            return
            
        for msg in self.ai_handler.conversation_history:
            if msg["role"] == "user":
                self.chat_display.append(
                    f"<p style='color: #2c3e50'><b>You:</b> {msg['content']}</p>"
                )
            elif msg["role"] == "assistant":
                self.chat_display.append(
                    f"<p style='color: #8e44ad'><b>Assistant:</b> {msg['content']}</p>"
                )
        
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