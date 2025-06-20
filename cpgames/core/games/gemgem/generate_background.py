import pygame
import random

def create_beautiful_background_texture(width=128, height=128, output_path="background_texture.png"):
    """
    Creates a beautiful repeating background texture with a subtle gradient and noise.

    This texture can be used for the game background and tiled if needed.

    Args:
        width (int): The width of the texture (should be a power of 2 for easy tiling, e.g., 64, 128).
        height (int): The height of the texture.
        output_path (str): The filename and path to save the generated image.
    """
    pygame.init()

    # Create a surface with an alpha channel for potential transparency, though we'll make it opaque
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Define base colors for the gradient
    # A soft, slightly desaturated blue-green
    color1 = (100, 150, 160)
    # A slightly darker, richer blue
    color2 = (70, 110, 140)

    # Draw a vertical gradient
    for y in range(height):
        # Interpolate between color1 and color2 based on y position
        lerp_factor = y / (height - 1)
        r = int(color1[0] + (color2[0] - color1[0]) * lerp_factor)
        g = int(color1[1] + (color2[1] - color1[1]) * lerp_factor)
        b = int(color1[2] + (color2[2] - color1[2]) * lerp_factor)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

    # Add subtle noise for a more organic feel
    for _ in range(int(width * height * 0.1)): # Add noise to 10% of pixels
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        # Get existing pixel color
        pixel_color = surface.get_at((x, y))
        # Add a small random offset to the color, keeping it within bounds
        noise_r = min(255, max(0, pixel_color[0] + random.randint(-10, 10)))
        noise_g = min(255, max(0, pixel_color[1] + random.randint(-10, 10)))
        noise_b = min(255, max(0, pixel_color[2] + random.randint(-10, 10)))
        surface.set_at((x, y), (noise_r, noise_g, noise_b, pixel_color[3])) # Preserve alpha

    # Save the surface as a PNG
    try:
        pygame.image.save(surface, output_path)
        print(f"Successfully created '{output_path}'")
    except Exception as e:
        print(f"Error saving image: {e}")

    pygame.quit()

if __name__ == '__main__':
    # Make sure this path matches your game's resources directory
    # For example: "D:/Do not open/Hacker/Games-master/cpgames/core/games/gemgem/resources/images/"
    output_directory = "D:/Do not open/Hacker/Games-master/cpgames/core/games/gemgem/resources/images/"
    # Ensure the directory exists before saving
    import os
    os.makedirs(output_directory, exist_ok=True)

    create_beautiful_background_texture(
        width=128, # Choose a size. 128x128 is a good balance for tiling.
        height=128,
        output_path=os.path.join(output_directory, "background_texture.png")
    )
    print("\nRemember to place this 'background_texture.png' in your game's resources/images directory.")
    print("Also, ensure 'gemgem.py' is updated to load this image if you want to use it!")