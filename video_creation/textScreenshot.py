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

    font_path = "./fonts/Roboto-Regular.ttf"
    font_size = 40
    image_width = 400  # Smaller since it's just one word
    image_height = 100
    padding_top = 20
    padding_left = 20
    text_color = (255, 255, 255)
    stroke_color = (0, 0, 0)

    font = ImageFont.truetype(font_path, font_size)
    punctuation_marks = {'.', ',', ';', ':', '?', '!'}
    symbols = {'!',"@","#","$","%","^","&","*","&","(",")",0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    for idx, comment in enumerate(comments[:screenshot_num]):
        print_substep(f"Rendering comment {idx} → ID: {comment['comment_id']}")
        words = comment["comment_body"].split()
        letters = os.path.join(output_dir, f"letters_{idx}.txt")
        with open(letters, 'w') as file:
                file.write('')
        
        image_counter = 0

        for word in words:
            img = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            bbox = draw.textbbox((0, 0), word, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (image_width - text_width) // 2
            y = (image_height - text_height) // 2

            draw.text(
                (x, y),
                word,
                font=font,
                fill=text_color,
                stroke_width=4,
                stroke_fill=stroke_color
            )
            
            with open(letters, 'a') as file:
                if any(char in punctuation_marks for char in word):
                    file.write(f'{len(word)+12},') #increases delay if punctuation is detected
                elif any(char in symbols for char in word):
                    file.write(f'{len(word)+8},')
                else:
                    file.write(f'{len(word)},')

            img_path = os.path.join(output_dir, f"comment_{idx}_{image_counter}.png")
            img.save(img_path)
            image_counter += 1
