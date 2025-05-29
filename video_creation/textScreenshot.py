from PIL import Image, ImageDraw, ImageFont
import os
from utils.console import print_step, print_substep

def wrap_text(text, draw, font, max_width):
    """
    Wrap text so each line fits within max_width pixels.
    Returns a list of lines.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)
    return lines

def generateTextScreenshots(reddit_object: dict, screenshot_num: int):
    print_step("Generating Text Screenshots")

    comments = reddit_object["comments"]
    output_dir = f"assets/temp/{reddit_object['thread_id']}/png"
    os.makedirs(output_dir, exist_ok=True)

    font_path = "./fonts/Roboto-Regular.ttf"  # Update this path if needed
    font_size = 40
    image_width = 1052
    image_height = 300
    padding_top = 20
    padding_left = 20
    line_spacing = 6
    text_color = (255, 255, 255)
    stroke_color = (0, 0, 0)
    font = ImageFont.truetype(font_path, font_size)
    for idx, comment in enumerate(comments[:screenshot_num]):
        print_substep(f"Rendering comment {idx} → ID: {comment['comment_id']}")
        img = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        lines = wrap_text(comment["comment_body"], draw, font, image_width - 2 * padding_left)

        y = padding_top
        for line in lines:
            draw.text(
                (padding_left, y),
                line,
                font=font,
                fill=text_color,
                stroke_width=4,
                stroke_fill=stroke_color
            )
            bbox = draw.textbbox((padding_left, y), line, font=font)
            line_height = bbox[3] - bbox[1] + line_spacing  # add spacing after line
            y += line_height


        # Save the image
        img_path = os.path.join(output_dir, f"comment_{idx}z.png")
        img.save(img_path)
