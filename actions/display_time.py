from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time


### TODO: fix display time function
def generate_time_image():
    while True:
        # Get current time
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Create an image (200x100 pixels, white background)
        img = Image.new('RGB', (300, 100), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Load a font (default PIL font)
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except IOError:
            font = ImageFont.load_default()
        
        # Get text size and position it at the center
        text_size = draw.textbbox((0, 0), current_time, font=font)
        text_width = text_size[2] - text_size[0]
        text_height = text_size[3] - text_size[1]
        position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
        
        # Draw the time text on the image
        draw.text(position, current_time, fill=(0, 0, 0), font=font)
        
        # Save as PNG
        img.save("current_time.png")
        print("Image updated with time:", current_time)
        
        # Wait for 1 second before updating again
        time.sleep(1)

# Run the function
generate_time_image()
