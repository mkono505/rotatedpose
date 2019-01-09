import numpy as np
from PIL import Image, ImageDraw


# draw the lines
def drawLines(draw, joints, clr, line_width):
    def drawLine(first_idx, second_idx, clr_idx):
        if joints[first_idx, 2] and joints[second_idx, 2]:
            draw.line((joints[first_idx, 0], joints[first_idx, 1],
                       joints[second_idx, 0], joints[second_idx, 1]),
                      fill=(clr[clr_idx, 0], clr[clr_idx, 1], clr[clr_idx, 2]),
                      width=line_width)

    drawLine(1, 2, 0)
    drawLine(1, 5, 1)
    drawLine(2, 3, 2)
    drawLine(3, 4, 3)
    drawLine(5, 6, 4)
    drawLine(6, 7, 5)
    drawLine(1, 8, 6)
    drawLine(8, 9, 7)
    drawLine(9, 10, 8)
    drawLine(1, 11, 9)
    drawLine(11, 12, 10)
    drawLine(12, 13, 11)
    drawLine(0, 1, 12)
    drawLine(0, 14, 13)
    drawLine(15, 17, 14)
    drawLine(0, 15, 15)
    drawLine(0, 15, 16)


# draw the elements transparent
def draw_transparent(canvas, alpha, joints, clr, joint_size, line_width):
    mask = Image.new("L", canvas.size, 1)
    a_canvas = Image.new("RGB", canvas.size,  (255, 255, 255))
    a_canvas.putalpha(mask)
    draw = ImageDraw.Draw(a_canvas)

    drawLines(draw, joints, clr, line_width)

    for i in range(18):
        draw.ellipse((joints[i, 0]-joint_size, joints[i, 1]-joint_size,
                      joints[i, 0]+joint_size, joints[i, 1]+joint_size),
                     fill=(clr[i, 0], clr[i, 1], clr[i, 2]), outline=None)

    del draw

    canvas.putalpha(mask)
    return Image.blend(canvas, a_canvas, alpha).convert("RGB")


def draw_joints(img_path, output_path, reconst_joints):
    # define color params
    c1 = 255
    c2 = c1-(int(c1/4))
    c3 = c2-(int(c1/4))
    c4 = 0

    # define the colors
    set_clr = np.array([[c1, c4, c4],
                        [c1, c3, c4],
                        [c1, c2, c4],
                        [c1, c1, c4],
                        [c2, c1, c4],
                        [c3, c1, c4],
                        [c4, c1, c4],
                        [c4, c1, c3],
                        [c4, c1, c2],
                        [c4, c1, c1],
                        [c4, c2, c1],
                        [c4, c3, c1],
                        [c4, c4, c1],
                        [c3, c4, c1],
                        [c2, c4, c1],
                        [c1, c4, c2],
                        [c1, c4, c1],
                        [c1, c4, c3]])

    # set size of joints
    joint_size = 5

    # set line width
    line_width = 7

    # set alpha
    alpha_val = 0.5

    # read image here
    canvas = Image.open(img_path)

    canvas = draw_transparent(
        canvas, alpha_val, reconst_joints, set_clr, joint_size, line_width)

    # save the images
    canvas.save(output_path)
