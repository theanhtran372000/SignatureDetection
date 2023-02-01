import fitz


def draw_rect(file_path, coords, dest_path):
    doc = fitz.open(file_path)

    for c in coords:
        page = doc[c['page_num']]
        coord = c['coords']
        page.draw_rect(
            [
                coord[0],
                coord[1],   # top-right
                coord[0] + 5,
                coord[1] + 5    # bottom-right
            ],
            color=(0, 1, 0),
            width=2
        )

    # Save pdf
    doc.save(dest_path)
