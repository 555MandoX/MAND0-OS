#!/usr/bin/env python3
"""Generates the MANDO OS icon set (original artwork) into ../icons. Needs Pillow.  Usage: python3 tools/make-icons.py"""
import os
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'icons')
BG_TOP, BG_BOT = (20, 30, 23), (8, 11, 9)       # forest near-black
GREEN, WHITE = (141, 187, 145), (245, 247, 244)  # accent + text white
PTS = [(0.14, 0.86), (0.14, 0.14), (0.5, 0.60), (0.86, 0.14), (0.86, 0.86)]  # the M, unit box

def render(size, mark_scale, rounded, ss=4):
    S = size * ss
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    bg = Image.new('RGBA', (S, S))
    px = bg.load()
    for y in range(S):  # vertical gradient
        t = y / (S - 1)
        c = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)) + (255,)
        for x in range(S): px[x, y] = c
    glow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-S * .2, -S * .35, S * .75, S * .55], fill=(83, 125, 91, 120))
    bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(S * 0.12)))
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.225), fill=255) if rounded else mask.paste(255, [0, 0, S, S])
    img.paste(bg, (0, 0), mask)
    d = ImageDraw.Draw(img)
    box = S * mark_scale; off = (S - box) / 2
    P = [(off + x * box, off + y * box) for x, y in PTS]
    w = int(box * 0.15)
    def stroke(a, b, col):
        d.line([a, b], fill=col, width=w)
        for p in (a, b): d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=col)
    stroke(P[0], P[1], GREEN); stroke(P[3], P[4], GREEN)      # stems
    stroke(P[1], P[2], WHITE); stroke(P[2], P[3], WHITE)      # V
    r = int(box * 0.055); cx, cy = P[2][0], off + box * 0.90  # accent dot under the V
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN)
    return img.resize((size, size), Image.LANCZOS)

os.makedirs(OUT, exist_ok=True)
jobs = [('icon-192.png', 192, 0.56, True), ('icon-512.png', 512, 0.56, True),
        ('icon-maskable-512.png', 512, 0.50, False),   # full bleed, mark inside the 80% safe zone
        ('apple-touch-icon.png', 180, 0.56, False), ('favicon-32.png', 32, 0.66, True)]
for name, size, scale, rounded in jobs:
    im = render(size, scale, rounded)
    if not rounded: im = im.convert('RGB')
    im.save(os.path.join(OUT, name), optimize=True); print('wrote', name, im.size)
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141e17"/><stop offset="1" stop-color="#080b09"/></linearGradient></defs><rect width="512" height="512" rx="115" fill="url(#g)"/><g fill="none" stroke-width="43" stroke-linecap="round" stroke-linejoin="round"><path d="M143 369V143M369 143V369" stroke="#8dbb91"/><path d="M143 143L256 270L369 143" stroke="#f5f7f4"/></g><circle cx="256" cy="396" r="16" fill="#8dbb91"/></svg>'''
open(os.path.join(OUT, 'icon.svg'), 'w').write(svg); print('wrote icon.svg')
