from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple
import math

def create_anime_style_image(text, size=(200, 200), bg_color=(255, 255, 255, 0)):
    # Create transparent image
    image = Image.new('RGBA', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Colors
    outline_color = (40, 44, 52, 255)  # Darker outline
    hair_color = (44, 62, 80, 255)     # Dark blue-gray
    
    # Draw character
    center_x = size[0] // 2
    
    # Head shape (more angular for anime style)
    face_points = [
        (center_x - 40, 60),      # Left
        (center_x - 30, 40),      # Top left
        (center_x, 30),           # Top
        (center_x + 30, 40),      # Top right
        (center_x + 40, 60),      # Right
        (center_x + 35, 90),      # Bottom right
        (center_x, 100),          # Bottom
        (center_x - 35, 90),      # Bottom left
    ]
    draw.polygon(face_points, fill=(255, 223, 196, 255), outline=outline_color)
    
    # Hair (spiky anime style)
    hair_points = [
        (center_x - 45, 70),      # Left side
        (center_x - 35, 35),      # Top left
        (center_x - 15, 25),      # Upper left
        (center_x, 20),           # Top
        (center_x + 15, 25),      # Upper right
        (center_x + 35, 35),      # Top right
        (center_x + 45, 70),      # Right side
        (center_x + 30, 45),      # Inner right
        (center_x, 40),           # Center
        (center_x - 30, 45),      # Inner left
    ]
    draw.polygon(hair_points, fill=hair_color, outline=outline_color)
    
    # Eyes (anime style)
    # Left eye
    draw.ellipse([center_x - 25, 60, center_x - 15, 70], fill=(255, 255, 255, 255), outline=outline_color)
    draw.ellipse([center_x - 22, 63, center_x - 18, 67], fill=outline_color)
    
    # Right eye
    draw.ellipse([center_x + 15, 60, center_x + 25, 70], fill=(255, 255, 255, 255), outline=outline_color)
    draw.ellipse([center_x + 18, 63, center_x + 22, 67], fill=outline_color)
    
    # Body (modern style outfit)
    # Neck
    draw.line([center_x, 100, center_x, 120], fill=outline_color, width=3)
    
    # Shoulders and upper body
    draw.line([center_x, 120, center_x - 40, 130], fill=outline_color, width=3)  # Left shoulder
    draw.line([center_x, 120, center_x + 40, 130], fill=outline_color, width=3)  # Right shoulder
    draw.line([center_x - 40, 130, center_x - 35, 180], fill=outline_color, width=3)  # Left side
    draw.line([center_x + 40, 130, center_x + 35, 180], fill=outline_color, width=3)  # Right side
    
    # Add text label
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    text_width = draw.textlength(text, font=font)
    text_position = ((size[0] - text_width) // 2, 5)
    draw.text(text_position, text, fill=(0, 0, 0, 255), font=font)
    
    return image

def generate_character_images():
    states = ['idle', 'talking', 'listening', 'thinking', 'happy', 'sad', 'confused', 'working', 'error']
    genders = ['female', 'male']
    styles = ['anime']
    
    # Create directories
    for gender in genders:
        for style in styles:
            dir_path = f'assets/images/{gender}/{style}'
            os.makedirs(dir_path, exist_ok=True)
            
            # Create images for each state
            for state in states:
                image = create_anime_style_image(f"{gender.title()} - {state.title()}")
                image.save(f'{dir_path}/{state}.png')
                print(f"Generated: {dir_path}/{state}.png")

if __name__ == "__main__":
    generate_character_images()