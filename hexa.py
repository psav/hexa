#Clockwise Segment numbering

import math
from PIL import Image, ImageDraw
all_images = []
image_file_names = [
    "/home/user/hex1.png",
    "/home/user/hex2.png",
    "/home/user/hex3.png",
    "/home/user/hex4.png",
    "/home/user/hex5.png",
    "/home/user/hex6.png",
    "/home/user/hex7.png",
    "/home/user/hex8.png",
    "/home/user/hex9.png",
    "/home/user/hex10.png",
    "/home/user/hex11.png",
    "/home/user/hex12.png",
    "/home/user/glue.png"
]

fp_data = [
[
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
    (4, 3, -120),
    (1, 13, 180)
],
[
    (5, 3, -120),
    (5, 5, -120),
    (6, 6, 180),
    (5, 1, -120),
    (4, 9, -60),
    (6, 2, 180),
    (1, 3, 120),
    (1, 5, 120),
    (2, 6, 60),
    (1, 1, 120),
    (6, 9, 180),
    (2, 2, 60),
    (3, 3, 0),
    (3, 5, 0),
    (4, 6, -60),
    (3, 1, 0),
    (2, 9, 60),
    (4, 2, -60)
],
[
    (1, 13, 0),
    (5, 7, 120),
    (1, 8, 0),
    (6, 12, 60),
    (4, 10, 180),
    (6, 4, 60),
    (2, 11, -60),
    (1, 7, 0),
    (3, 8, -120),
    (2, 12, -60),
    (6, 10, 60),
    (2, 4, -60),
    (4, 11, 180),
    (3, 7, -120),
    (5, 8, 120),
    (4, 12, 180),
    (2, 10, -60),
    (4, 4, 180),
    (6, 11, 60)
],
[
    (1, 11, 60),
    (6, 7, 120),
    (2, 8, 0),
    (1, 12, 60),
    (5, 9, 180),
    (1, 4, 60),
    (3, 11, -60),
    (2, 7, 0),
    (4, 8, -120),
    (3, 12, -60),
    (1, 10, 60),
    (3, 4, -60),
    (5, 11, 180),
    (4, 7, -120),
    (6, 8, 120),
    (5, 12, 180),
    (3, 10, -60),
    (5, 4, 180)
]
]
im = Image.open(image_file_names[0])
width, height = im.size
base_image = Image.new("RGBA", (width * 10, height))

trig_width = width / 2.0
trig_height = (trig_width / 2.0) * math.tan(math.radians(60))


def run_tris(tris, row, offset):
    for i, im_place in enumerate(tris):
        print im_place
        segment, image, angle = im_place

        im = Image.open(image_file_names[image - 1])
        width, height = im.size
        #trig_width = width / 2.0
        #trig_height = (trig_width / 2.0) * math.tan(math.radians(60))

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
            [(trig_width / 2.0, upper), (trig_width *1.5, upper), (trig_width, height / 2.0)], #segment 1
            [(trig_width, height / 2.0), (trig_width * 1.5, upper), (trig_width * 2.0, height / 2.0)], # segment 2
            [(trig_width, height / 2.0), (trig_width * 2.0, height / 2.0), (trig_width * 1.5, lower)], # segment 3
            [(trig_width, height / 2.0), (trig_width * 1.5, lower), (trig_width / 2.0, lower)], # segment 4
            [(0, height / 2.0), (trig_width, height / 2.0), (trig_width / 2.0, lower)], # segment 5
            [(0, height / 2.0), (trig_width, height / 2.0), (trig_width / 2.0, upper)] # segement 6
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
        print target_segs[angle], segment, target_segs[angle] + segment, (target_segs[angle] + segment) % 6, target_seg

        al = im.copy().rotate(-angle, Image.BICUBIC)
        compo = Image.new("RGBA", al.size, (0,0,0,0))
        mask = Image.new("RGBA", al.size, (0,0,0,0))

        draw = ImageDraw.Draw(mask, 'RGBA')
        draw.polygon(masks[target_seg], (0, 0, 0, 255))

        compo.paste(al, (0, 0), mask)
        compo.save('/tmp/{}compo.png'.format(i))
        be = compo.crop(coords[target_seg])
        be.save('/tmp/{}{}be.png'.format(image, i))
        mask.save('/tmp/{}mask.png'.format(i))
        t_offset = int(trig_width / 2) if offset == 1 else 0
        base_image.paste(be, (int(trig_width) * i + t_offset, int(row * trig_height)), be)

offset = -1
for i, data in enumerate(fp_data):
    row = 0 if i < 2 else 1
    run_tris(data, row, offset)
    offset = offset * -1

base_image.save("/tmp/moog.png")
