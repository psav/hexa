# Clockwise Segment numbering

import math
from PIL import Image, ImageDraw
all_images = []
image_file_names = [
    "/home/user/01.jpeg",
    "/home/user/02.jpeg",
    "/home/user/03.jpeg",
    "/home/user/04.jpeg",
    "/home/user/05.jpeg",
    "/home/user/06.jpeg",
    "/home/user/01.jpeg",
    "/home/user/02.jpeg",
    "/home/user/03.jpeg",
    "/home/user/04.jpeg",
    "/home/user/05.jpeg",
    "/home/user/06.jpeg",
]

positions_f = [
    (4, 1, 0),
    (5, 6, 180),
    (5, 2, -60),
    (3, 9, -60),
    (6, 5, -120),
    (6, 3, 120),
    (6, 1, -120),
    (1, 6, 60),
    (1, 2, 180),
    (5, 9, 180),
    (2, 5, 120),
    (2, 3, 0),
    (2, 1, 120),
    (3, 6, -60),
    (3, 2, 60),
    (1, 9, 60),
    (4, 5, 0),
    (4, 3, -120)
]

base_image = None

for i, im_place in enumerate(positions_f):
    print im_place
    segment, image, angle = im_place

    im = Image.open(image_file_names[image - 1])
    width, height = im.size
    trig_width = width / 2.0
    trig_height = (trig_width / 2.0) * math.tan(math.radians(60))

    upper = (height / 2.0) - (trig_height)
    lower = (height / 2.0) + (trig_height)

    target_segs = {
        0: 1,
        -0: 1,
        180: 4,
        -180: 4,
        -60: 2,
        60: 6,
        -120: 3,
        120: 5,
    }

    masks = [
        # Segment 1
        [(trig_width / 2.0, upper), (trig_width * 1.5, upper), (trig_width, height / 2.0)],
        # Segment 2
        [(trig_width, height / 2.0), (trig_width * 1.5, upper), (trig_width * 2.0, height / 2.0)],
        # Segment 3
        [(trig_width, height / 2.0), (trig_width * 2.0, height / 2.0), (trig_width * 1.5, lower)],
        # Segment 4
        [(trig_width, height / 2.0), (trig_width * 1.5, lower), (trig_width / 2.0, lower)],
        # Segment 5
        [(0, height / 2.0), (trig_width, height / 2.0), (trig_width / 2.0, lower)],
        # Segment 6
        [(0, height / 2.0), (trig_width, height / 2.0), (trig_width / 2.0, upper)]
    ]

    coords = [
        (trig_width / 2.0, upper, trig_width * 1.5, height / 2.0),
        (trig_width, upper, trig_width * 2.0, height / 2.0),
        (trig_width, height / 2.0, trig_width * 2.0, lower),
        (trig_width / 2.0, height / 2.0, trig_width * 1.5, lower),
        (0, height / 2.0, trig_width, lower),
        (0, upper, trig_width, height / 2.0)
    ]

    target_seg = (target_segs[-angle] + segment) % 6 - 2

    al = im.copy().rotate(-angle)
    compo = Image.new("RGBA", al.size, (0, 0, 0, 0))
    mask = Image.new("RGBA", al.size, (0, 0, 0, 0))

    draw = ImageDraw.Draw(mask, 'RGBA')
    draw.polygon(masks[target_seg], (0, 0, 0, 255))

    compo.paste(al, (0, 0), mask)
    compo.save('/tmp/{}compo.png'.format(i))
    be = compo.crop(coords[target_seg])
    be.save('/tmp/{}{}be.png'.format(image, i))
    mask.save('/tmp/{}mask.png'.format(i))
    if not base_image:
        base_image = Image.new("RGBA", (width * 18, height))
    base_image.paste(be, (int(trig_width) * i, 0))
base_image.save("/tmp/moog.png")
