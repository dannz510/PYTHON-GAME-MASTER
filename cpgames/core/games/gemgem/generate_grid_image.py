import pygame

def create_hollow_grid_cell_image(size=64, border_width=3, output_path="grid_cell_hollow.png"):
    """
    Creates a visually appealing hollow grid cell image with a transparent center.

    Args:
        size (int): The width and height of the square image (e.g., 64 for 64x64 pixels).
        border_width (int): The thickness of the border.
        output_path (str): The filename and path to save the generated image.
    """
    pygame.init()

    # Create a surface with an alpha channel for transparency
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Define colors
    # A light, slightly desaturated blue for the main border color
    border_main_color = (150, 200, 255, 200) # RGBA - semi-transparent blue
    # A slightly darker shade for a subtle shadow/depth effect
    border_shadow_color = (80, 120, 180, 180)

    # Draw the inner transparent part (the "hollow" section)
    # This fills the entire surface with a transparent color first,
    # then we'll draw the border on top.
    surface.fill((0, 0, 0, 0)) # Fully transparent black

    # Draw the main border rectangle
    pygame.draw.rect(surface, border_main_color, (0, 0, size, size), border_width)

    # Add a subtle inner shadow/glow effect to the border
    # Draw slightly offset rectangles with reduced alpha for depth
    for i in range(1, border_width):
        alpha_factor = 1 - (i / border_width) * 0.7 # Fade out more with distance
        current_alpha_main = int(border_main_color[3] * alpha_factor)
        current_alpha_shadow = int(border_shadow_color[3] * alpha_factor)

        # Inner highlight (top-left) - makes it look slightly raised
        pygame.draw.line(surface, (255, 255, 255, current_alpha_main), (i, i), (size - i - 1, i), 1)
        pygame.draw.line(surface, (255, 255, 255, current_alpha_main), (i, i), (i, size - i - 1), 1)

        # Inner shadow (bottom-right) - gives a recessed look
        pygame.draw.line(surface, (0, 0, 0, current_alpha_shadow), (size - i - 1, i), (size - i - 1, size - i - 1), 1)
        pygame.draw.line(surface, (0, 0, 0, current_alpha_shadow), (i, size - i - 1), (size - i - 1, size - i - 1), 1)

    # Save the surface as a PNG
    try:
        pygame.image.save(surface, output_path)
        print(f"Successfully created '{output_path}'")
    except Exception as e:
        print(f"Error saving image: {e}")

    pygame.quit()

if __name__ == '__main__':
    # Make sure this path matches your game's resources directory
    # For example: "D:/Do not open/Hacker/Games-master/cpgames/core/games/gemgem/resources/images/grid_cell_hollow.png"
    output_directory = "D:/Do not open/Hacker/Games-master/cpgames/core/games/gemgem/resources/images/"
    # Ensure the directory exists before saving
    import os
    os.makedirs(output_directory, exist_ok=True)

    create_hollow_grid_cell_image(
        size=64, # Matches your cfg.GRIDSIZE
        border_width=3,
        output_path=os.path.join(output_directory, "grid_cell_hollow.png")
    )
    print("\nRemember to also provide a 'background_texture.png' if you enabled it in gemgem.py for a complete visual upgrade!")