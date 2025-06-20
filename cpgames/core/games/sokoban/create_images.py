from PIL import Image, ImageDraw

def create_placeholder_image(filepath, size=(60, 60), color=(150, 100, 50), border_color=(100, 70, 30)):
    """
    Creates a simple placeholder image with a solid color and a border,
    representing a modern box.
    """
    img = Image.new('RGBA', size, (0, 0, 0, 0)) # Start with a transparent image
    draw = ImageDraw.Draw(img)

    # Draw the main box
    draw.rectangle([0, 0, size[0], size[1]], fill=color)

    # Draw a simple inner highlight/shadow to give a slight 3D effect
    # Top-left highlight
    draw.line([(0, 0), (size[0]-1, 0)], fill=border_color, width=2)
    draw.line([(0, 0), (0, size[1]-1)], fill=border_color, width=2)

    # Bottom-right shadow
    draw.line([(size[0]-1, 0), (size[0]-1, size[1]-1)], fill=border_color, width=2)
    draw.line([(0, size[1]-1), (size[0]-1, size[1]-1)], fill=border_color, width=2)

    img.save(filepath)
    print(f"Placeholder image created at: {filepath}")

if __name__ == "__main__":
    # Define the directory where the image should be saved
    # This path should match the one in your error message or your game's config
    # Make sure this path is correct for your setup.
    image_directory = 'D:/Do not open/Hacker/Games-master/cpgames/core/games/sokoban/resources/images'
    
    # Ensure the directory exists
    import os
    os.makedirs(image_directory, exist_ok=True)

    # File paths for all missing images
    images_to_create = {
        'box_modern.png': (150, 100, 50),    # Brownish for box
        'player_modern.png': (0, 150, 0),    # Green for player
        'target_modern.png': (200, 200, 0),  # Yellow for target
        'wall_modern.png': (80, 80, 80),     # Gray for wall
        'game_bg.png': (50, 50, 50),         # Dark gray for game background
        'menu_bg.png': (40, 40, 60)          # Dark blue-gray for menu background
    }

    for filename, color in images_to_create.items():
        filepath = os.path.join(image_directory, filename)
        if "bg" in filename: # Backgrounds might be larger
            create_placeholder_image(filepath, size=(800, 600) if "menu" in filename else (100,100), color=color) # Adjust game_bg size based on typical level size, or make it tileable
        else:
            create_placeholder_image(filepath, size=(60, 60), color=color) # Use block size for elements