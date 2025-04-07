from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
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
        
        # Animation properties
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)  # 300ms for fade transition
        self.slide_animation = QPropertyAnimation(self.character_label, b"pos")
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Load initial character state
        self.load_character_image()
        
        # Setup animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_frame = 0
        
    def load_character_image(self):
        image_path = f"assets/images/{self.character_gender}/{self.character_style}/{self.current_state.value}.png"
        try:
            # Start fade out
            self.fade_animation.setStartValue(1.0)
            self.fade_animation.setEndValue(0.5)
            self.fade_animation.start()
            
            # Prepare slide animation
            current_pos = self.character_label.pos()
            self.slide_animation.setStartValue(current_pos)
            self.slide_animation.setEndValue(QPoint(current_pos.x(), current_pos.y() + 10))
            
            # Load and set new image
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                pixmap = QPixmap("assets/images/placeholder.png")
                
            self.character_label.setPixmap(pixmap)
            self.character_label.setFixedSize(pixmap.size())
            self.setFixedSize(pixmap.size())
            
            # Start slide and fade in
            self.slide_animation.start()
            QTimer.singleShot(150, self._fade_in)
            
        except Exception as e:
            print(f"Error loading character image: {e}")
            
    def _fade_in(self):
        self.fade_animation.setStartValue(0.5)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
    
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