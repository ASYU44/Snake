import pygame


def clip(surface: pygame.Surface, x: int, y: int, x_size: int, y_size: int) -> pygame.Surface:
    """
    Get a part of the image
    """
    clip_rect = pygame.Rect(x, y, x_size, y_size)  # Part of the image
    image = surface.subsurface(clip_rect)  # Get subsurface ace
    return image.copy()  # Return


def slicing_surface(image, num_slices_x: int = 1, num_slices_y: int = 1) -> list[pygame.Surface]:
    """
    Convert image to smaller parts of the image
    """
    image_width = image.get_width()
    image_height = image.get_height()

    if (image_width % num_slices_x != 0 or image_height % num_slices_y != 0
            or num_slices_y <= 0 or num_slices_x <= 0):
        print('Error while slicing Surface')
        return [image]

    frames = []
    slice_width = image_width // num_slices_x
    slice_height = image_height // num_slices_y
    for slice_x in range(num_slices_x):
        for slice_y in range(num_slices_y):
            frame = clip(image, slice_x * slice_width, slice_y * slice_height,
                         slice_width, slice_height)
            frames.append(frame)
    return frames


def create_text_with_outline(font: pygame.font, text: str,
                             text_color: tuple[int, int, int], outline_color: tuple[int, int, int], outline_width: int):
    # Render the main text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()

    # Create a surface for the outline
    outline_surface = pygame.Surface((text_rect.width + 2 * outline_width, text_rect.height + 2 * outline_width),
                                     pygame.SRCALPHA)
    outline_surface.fill((0, 0, 0, 0))  # Make the background transparent

    # Render the outline by blitzing the text at the corners
    positions = [
        (-outline_width, -outline_width),  # Top-left
        (outline_width, -outline_width),   # Top-right
        (-outline_width, outline_width),   # Bottom-left
        (outline_width, outline_width)     # Bottom-right
    ]

    for pos in positions:
        offset_rect = text_rect.copy()
        offset_rect.topleft = (outline_width + pos[0], outline_width + pos[1])
        outline_surface.blit(font.render(text, True, outline_color), offset_rect)

    # Blit the original text onto the outline surface
    outline_surface.blit(text_surface, (outline_width, outline_width))

    return outline_surface
