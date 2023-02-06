import fitz
import random

def random_color():
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    return (r, g, b)

def draw_rect(file_path, placeholders, dest_path):
    doc = fitz.open(file_path)

    for holder in placeholders:
        
        page = doc[holder['page_num']]
        x = holder['x']
        y = holder['y']
        w = holder['width']
        h = holder['height']
        
        page.draw_rect(
            [
                x,
                y,   # top-right
                x + w,
                y + h    # bottom-right
            ],
            color=random_color(),
            width=2
        )

    # Save pdf
    doc.save(dest_path)
