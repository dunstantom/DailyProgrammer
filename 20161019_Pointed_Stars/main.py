from PIL import Image, ImageDraw
from math import sin, cos, pi, ceil


def draw_pointed_star(n):
    im = Image.new("RGB", (300, 300), 'white')
    draw = ImageDraw.Draw(im)

    points = []
    for i in range(0,n):
        rads = i*2*pi/n - pi/2.0
        points.append((150*cos(rads) + 150, 150*sin(rads) + 150))
        if i > 0:
            draw.line(points[i-1]+points[i],fill=128)
    draw.line(points[n-1]+points[0],fill=128)

    for i in range(0, n):
        cw_point = int((i + ceil(n/2.0) - 1) % n)
        ccw_point = int(abs( (i - ceil(n / 2.0) + 1) % n ))
        draw.line(points[i] + points[cw_point], fill=128)
        draw.line(points[i] + points[ccw_point], fill=128)

    del draw
    im.save("pointed_star_%d.png" % n, "PNG")


if __name__ == "__main__":
    n = 0
    while n != -1:
        n = input("Number of points: ")
        draw_pointed_star(n)
