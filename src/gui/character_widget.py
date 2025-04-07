from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from core.ai_handler import AIState

class CharacterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create character label
        self.character_label = QLabel(self)
        self.character_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Initialize state
        self.current_state = AIState.IDLE
        self.character_gender = "female"  # Default character
        self.character_style = "anime"    # Default style
        
        # Load initial character state
        self.load_character_image()
        
        # Setup animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_frame = 0
        
    def load_character_image(self):
        # Path format: assets/images/{gender}/{style}/{state}.png
        image_path = f"assets/images/{self.character_gender}/{self.character_style}/{self.current_state.value}.png"
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                # Load default/placeholder image if character image not found
                pixmap = QPixmap("assets/images/placeholder.png")
            self.character_label.setPixmap(pixmap)
            self.character_label.setFixedSize(pixmap.size())
            self.setFixedSize(pixmap.size())
        except Exception as e:
            print(f"Error loading character image: {e}")
    
    def set_state(self, state: AIState):
        if self.current_state != state:
            self.current_state = state
            self.load_character_image()
            
    def update_animation(self):
        # TODO: Implement frame-based animation if using animated sprites
        self.animation_frame = (self.animation_frame + 1) % 4  # Example: 4 frames per animation
        
    def set_character(self, gender: str, style: str):
        self.character_gender = gender
        self.character_style = style
        self.load_character_image()