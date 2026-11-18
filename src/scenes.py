import math, random
import cairo
from lib import *

B = STYLES['bagas']
F1 = STYLES['f1']
F2 = STYLES['f2']

# ---------------------------------------------------------------- timeline
T_A, T_B, T_C0, T_C1, T_C2, T_C3, T_C4, T_D, T_END = 0.0, 8.0, 13.1, 18.7, 21.9, 25.1, 28.3, 31.8, 42.4
WIPES = [(T_C0, '#3A86FF'), (T_C1, '#FF7A1A'), (T_C2, '#2EC4B6'), (T_C3, '#E63946'), (T_C4, '#FFC93C'), (T_D, '#7B2CBF')]
WIPE_HALF = 0.3
XFADE = (7.5, 8.0)


def header(ctx, lt, small, title, size=130, fill='#FFFFFF', chipbg='#FFC93C'):
    s1 = back_out(prog(lt, 0.25, 0.35))
    chip(ctx, small, 540, 385, 30, chipbg, OUT, scale=s1, rot=-2)
    s2 = back_out(prog(lt, 0.35, 0.4))
    big_text(ctx, title, 540, 500, size, fill=fill, scale=s2, rot=-3, maxw=980)


# ---------------------------------------------------------------- room (A, B)
FLOOR = 1430
HIP_A = (440, 1308)
S_A = 1.3
HINGE = (800, 1228)


def window(ctx, x, y, w, h, night, t):
    rrect(ctx, x - 14, y - 14, w + 28, h + 28, 10)
    fill_stroke(ctx, '#5B4E8C' if night else '#C9884A', OUT, 5)
    ctx.rectangle(x, y, w, h)
    g = cairo.LinearGradient(0, y, 0, y + h)
    if night:
        g.add_color_stop_rgba(0, *hexc('#1B1F4A'))
        g.add_color_stop_rgba(1, *hexc('#3A3F86'))
    else:
        g.add_color_stop_rgba(0, *hexc('#7CC8F7'))
        g.add_color_stop_rgba(1, *hexc('#CBEBFF'))
    ctx.set_source(g)
    ctx.fill()
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    if night:
        rnd = random.Random(3)
        for i in range(14):
            sx, sy = x + rnd.random() * w, y + rnd.random() * h
            tw = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7)
            sparkle(ctx, sx, sy, 4 + 4 * tw, '#FFFFFF', 0.5 + 0.5 * tw)
        cx, cy = x + w * 0.45, y + h * 0.42
        ctx.arc(cx, cy, 40, 0, 2 * math.pi)
        setc(ctx, '#FFF4C2')
        ctx.fill()
        ctx.arc(cx + 18, cy - 12, 36, 0, 2 * math.pi)
        setc(ctx, '#2A2F68')
        ctx.fill()
    else:
        cx, cy = x + w * 0.5, y + h * 0.5
        rg = cairo.RadialGradient(cx, cy, 10, cx, cy, 140)
        rg.add_color_stop_rgba(0, *hexc('#FFF6B0', 0.9))
        rg.add_color_stop_rgba(1, *hexc('#FFF6B0', 0))
        ctx.set_source(rg)
        ctx.paint()
        ctx.arc(cx, cy, 48, 0, 2 * math.pi)
        setc(ctx, '#FFD23F')
        ctx.fill()
    ctx.restore()
    setc(ctx, '#5B4E8C' if night else '#C9884A')
    ctx.set_line_width(12)
    ctx.move_to(x + w / 2, y)
    ctx.line_to(x + w / 2, y + h)
    ctx.move_to(x, y + h / 2)
    ctx.line_to(x + w, y + h / 2)
    ctx.stroke()
    ctx.rectangle(x, y, w, h)
    setc(ctx, OUT)
    ctx.set_line_width(5)
    ctx.stroke()


def chair(ctx, night):
    col = '#3D4A73' if night else '#4E6A8F'
    for x0, x1 in ((345, 330), (490, 500)):
        ctx.move_to(x0, 1335)
        ctx.line_to(x1, FLOOR)
        setc(ctx, OUT)
        ctx.set_line_width(14)
        ctx.stroke()
        ctx.move_to(x0, 1335)
        ctx.line_to(x1, FLOOR)
        setc(ctx, col)
        ctx.set_line_width(7)
        ctx.stroke()
    rrect(ctx, 318, 1110, 30, 230, 10)
    fill_stroke(ctx, col, OUT, 5)
    rrect(ctx, 330, 1316, 180, 22, 8)
    fill_stroke(ctx, col, OUT, 5)


def desk_back(ctx, night):
    wood = '#7A4E2A' if night else '#A46A36'
    for lx in (612, 990):
        ctx.rectangle(lx - 9, 1255, 18, FLOOR - 1255)
        fill_stroke(ctx, wood, OUT, 5)


def desk_top(ctx, night):
    rrect(ctx, 590, 1236, 430, 24, 6)
    fill_stroke(ctx, '#9A6638' if night else '#C98A4B', OUT, 5)


def mug_books(ctx, t, night):
    # books
    cols = [('#E63946', 'Linux'), ('#3A86FF', 'Python'), ('#22C55E', 'Nmap'), ('#F59E0B', 'Burp')]
    for i, (c, lab) in enumerate(cols):
        y = 1236 - 18 * (i + 1)
        x = 930 + (i % 2) * 6
        rrect(ctx, x, y, 80, 18, 3)
        fill_stroke(ctx, c, OUT, 3.5)
        font(ctx, 'Poppins', 11, True)
        ctx.move_to(x + 12, y + 13)
        setc(ctx, '#FFFFFF')
        ctx.show_text(lab)
        ctx.new_path()
    # mug
    ctx.new_path()
    ctx.arc(895, 1210, 13, -math.pi / 2, math.pi / 2)
    setc(ctx, OUT)
    ctx.set_line_width(12)
    ctx.stroke()
    ctx.arc(895, 1210, 13, -math.pi / 2, math.pi / 2)
    setc(ctx, '#FFFFFF')
    ctx.set_line_width(5)
    ctx.stroke()
    rrect(ctx, 852, 1186, 44, 50, 6)
    fill_stroke(ctx, '#FFFFFF', OUT, 4.5)
    for k in range(2):
        x0 = 866 + k * 16
        ph = t * 2.2 + k * 1.3
        a = 0.35 + 0.25 * math.sin(ph)
        ctx.move_to(x0, 1176)
        for j in range(1, 9):
            yy = 1176 - j * 7
            ctx.line_to(x0 + 6 * math.sin(ph * 2 + j * 0.9), yy)
        setc(ctx, '#FFFFFF' if night else '#9C7A5B', a)
        ctx.set_line_width(4)
        ctx.stroke()


def laptop(ctx, theta, night, glow):
    hx, hy = HINGE
    # screen
    d = (-math.cos(rad(theta)), -math.sin(rad(theta)))
    top = (hx + 138 * d[0], hy + 138 * d[1])
    for w, c in ((22, OUT), (13, '#3A3F4B')):
        ctx.move_to(hx, hy)
        ctx.line_to(*top)
        setc(ctx, c)
        ctx.set_line_width(w)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    if glow > 0:
        # bright edge on screen face
        nx, ny = -d[1], d[0]
        ox, oy = -nx * 6, -ny * 6
        ctx.move_to(hx + ox + d[0] * 10, hy + oy + d[1] * 10)
        ctx.line_to(top[0] + ox - d[0] * 8, top[1] + oy - d[1] * 8)
        setc(ctx, '#7CFFD8', glow)
        ctx.set_line_width(5)
        ctx.stroke()
    rrect(ctx, hx - 172, hy - 2, 180, 13, 5)
    fill_stroke(ctx, '#C3CAD8', OUT, 4.5)
    return top


def glow_light(ctx, cx, cy, r, col, a):
    if a <= 0:
        return
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_SCREEN)
    rg = cairo.RadialGradient(cx, cy, 0, cx, cy, r)
    rg.add_color_stop_rgba(0, *hexc(col, a))
    rg.add_color_stop_rgba(1, *hexc(col, 0))
    ctx.set_source(rg)
    ctx.paint()
    ctx.restore()


def room(ctx, t, night):
    setc(ctx, '#1C2347' if night else '#FDE5C2')
    ctx.paint()
    ctx.rectangle(0, FLOOR, W, H - FLOOR)
    setc(ctx, '#141834' if night else '#D89F65')
    ctx.fill()
    ctx.rectangle(0, FLOOR - 10, W, 14)
    setc(ctx, '#2A3363' if night else '#B9814B')
    ctx.fill()
    ellipse(ctx, 650, FLOOR + 30, 430, 22)
    setc(ctx, '#000000', 0.22)
    ctx.fill()
    window(ctx, 70, 640, 250, 250, night, t)


CARDS = [('CTF', '#8B5CF6', 'solve challenge', 1.4), ('PENTEST', '#E63946', 'scan target', 2.2),
         ('AI', '#3A86FF', 'train model', 3.0), ('VIBE CODING', '#22C55E', 'ship project', 3.8)]


def card(ctx, cx, cy, tag, col, label, sc):
    if sc <= 0.001:
        return
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(sc, sc)
    w, h = 380, 66
    rrect(ctx, -w / 2 + 5, -h / 2 + 7, w, h, 16)
    setc(ctx, '#000000', 0.35)
    ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 16)
    fill_stroke(ctx, '#FFFFFF', OUT, 4)
    font(ctx, 'Poppins', 21, True)
    e = ctx.text_extents(tag)
    tw = e.x_advance + 24
    rrect(ctx, -w / 2 + 14, -18, tw, 36, 10)
    setc(ctx, col)
    ctx.fill()
    ctx.move_to(-w / 2 + 26, 8)
    setc(ctx, '#FFFFFF')
    ctx.show_text(tag)
    ctx.new_path()
    font(ctx, 'Poppins', 26, True)
    ctx.move_to(-w / 2 + 30 + tw, 10)
    setc(ctx, OUT)
    ctx.show_text(label)
    ctx.new_path()
    ctx.restore()


def scene_A(ctx, t):
    room(ctx, t, True)
    chair(ctx, True)
    desk_back(ctx, True)
    stressed = t > 4.8
    spd = 26 if stressed else 16
    k1 = abs(math.sin(t * spd))
    k2 = abs(math.sin(t * spd + 1.6))
    targets = {'front': (712 + 8 * math.sin(t * 5), 1218 - 10 * k1),
               'back': (668 + 8 * math.cos(t * 4), 1220 - 10 * k2)}
    face = 'worried' if stressed else 'focus'
    sweat = ((t * 1.2) % 1.0) if stressed else 0
    draw_person(ctx, HIP_A[0], HIP_A[1], S_A, B, sit=True, lean=10, targets=targets, face=face,
                sweat=sweat, look=(4, 3), lens='#38F2C0', tilt=4)
    desk_top(ctx, True)
    laptop(ctx, 102, True, 1.0)
    mug_books(ctx, t, True)
    glow_light(ctx, 700, 1120, 380, '#38F2C0', 0.33 + 0.04 * math.sin(t * 9))
    # UI
    big_text(ctx, 'SENIN - JUMAT', 540, 395, 150, scale=back_out(prog(t, 0.1, 0.45)))
    chip(ctx, 'si paling cyber security', 540, 510, 30, '#0E0E14', '#FFFFFF', border='#FFFFFF',
         scale=back_out(prog(t, 0.4, 0.4)), rot=-2)
    for i, (tag, col, lab, st) in enumerate(CARDS):
        card(ctx, 815, 625 + i * 84, tag, col, lab, back_out(prog(t, st, 0.35)))
    sb = back_out(prog(t, 4.6, 0.35))
    if sb > 0:
        ctx.save()
        ctx.translate(1000, 595)
        ctx.scale(sb, sb)
        ctx.arc(0, 0, 32, 0, 2 * math.pi)
        fill_stroke(ctx, '#E63946', OUT, 4)
        text_center(ctx, '+99', 0, 0, 24, '#FFFFFF')
        ctx.restore()
    if stressed:
        # little stress marks
        a = 0.6 + 0.4 * math.sin(t * 20)
        hx, hy = head_point(*HIP_A, S_A, 10, -262, 10)
        setc(ctx, '#FFFFFF', a)
        ctx.set_line_width(6)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for ang in (-60, -90, -120):
            dx, dy = math.cos(rad(ang)), math.sin(rad(ang))
            ctx.move_to(hx + dx * 30, hy + dy * 30)
            ctx.line_to(hx + dx * 58, hy + dy * 58)
        ctx.stroke()


def scene_B(ctx, t):
    room(ctx, t + 8, False)
    chair(ctx, False)
    desk_back(ctx, False)
    # laptop angle
    if t < 1.5:
        th = 102
    elif t < 2.05:
        th = lerp(102, 0, ease_io(prog(t, 1.5, 0.55)))
    elif t < 2.75:
        th = 0
    else:
        th = lerp(0, 48, ease_out(prog(t, 2.75, 0.45)))
    hx, hy = HINGE
    lid_top = (hx - 138 * math.cos(rad(th)), hy - 138 * math.sin(rad(th)))
    relax = (520, 1292), (548, 1296)
    if t < 1.5:
        tg = {'front': (712, 1214), 'back': (668, 1216)}
        lean, face = 10, 'focus'
    elif t < 2.05:
        p = ease_io(prog(t, 1.5, 0.55))
        tg = {'front': (lerp(712, lid_top[0], 1) - 4, lid_top[1] + 2) if p < 0.85 else relax[1],
              'back': (lerp(668, relax[0][0], p), lerp(1216, relax[0][1], p))}
        lean, face = lerp(10, -6, p), 'smile'
    elif t < 2.65:
        tg = {'front': relax[1], 'back': relax[0]}
        lean, face = -6 + 1.5 * math.sin(t * 3), 'happy'
    else:
        p = ease_out(prog(t, 2.65, 0.4))
        tg = {'front': (lerp(relax[1][0], lid_top[0] - 6, p), lerp(relax[1][1], lid_top[1] + 4, p)),
              'back': relax[0]}
        lean, face = lerp(-6, 14, p), ('grin' if t > 2.95 else 'smile')
    draw_person(ctx, HIP_A[0], HIP_A[1], S_A, B, sit=True, lean=lean, targets=tg, face=face,
                look=(4, 2) if t > 2.75 else (2, 0), tilt=-4 if 2.05 < t < 2.65 else 3)
    desk_top(ctx, False)
    laptop(ctx, th, False, 0.6 if t > 2.95 else 0)
    mug_books(ctx, t, False)
    if t > 2.95:
        glow_light(ctx, 760, 1180, 200, '#38F2C0', 0.25)
    big_text(ctx, 'SABTU - MINGGU', 540, 395, 150, fill='#FFC93C', scale=back_out(prog(t, 0.05, 0.45)))
    if t < 2.8:
        chip(ctx, 'laptop ditutup dulu~', 540, 510, 30, '#0E0E14', '#FFFFFF',
             scale=back_out(prog(t, 0.6, 0.35)), rot=-2)
    else:
        chip(ctx, '...kadang dibuka lagi sih', 540, 510, 30, '#0E0E14', '#FFFFFF',
             scale=back_out(prog(t, 2.8, 0.3)), rot=-2)
    bubble(ctx, 'HEHE', 640, 930, 80, scale=back_out(prog(t, 4.25, 0.35)), rot=-8, tail=(-60, 50))



# ---------------------------------------------------------------- C0 car free day / night
def mixc(a, b, p):
    ca, cb = hexc(a), hexc(b)
    return '#%02X%02X%02X' % tuple(int(255 * lerp(ca[i], cb[i], p)) for i in range(3))


CROWD = [dict(F1, shirt='#8E7DBE', sleeve='#8E7DBE', shirt_d='#6E5DA0', seed=0.1),
         dict(F2, shirt='#2EC4B6', sleeve='#2EC4B6', shirt_d='#1F9488', capc='#FFC93C', seed=0.5),
         dict(F1, shirt='#FF7AA2', sleeve='#FF7AA2', shirt_d='#D9567E', skin='#F2C29B', seed=0.8),
         dict(F2, shirt='#FFD23F', sleeve='#FFD23F', shirt_d='#D4A90F', capc='#3A86FF', seed=0.3),
         dict(F1, shirt='#E63946', sleeve='#E63946', shirt_d='#B02531', seed=0.65)]


def walk_pose(ph, amp=24):
    sn = math.sin(ph)
    l1 = (-amp * sn, -amp * sn - 14 * max(0, -math.cos(ph)))
    l2 = (amp * sn, amp * sn - 14 * max(0, math.cos(ph)))
    a_back = (amp * 0.9 * sn, amp * 0.9 * sn + 18)
    a_front = (-amp * 0.9 * sn, -amp * 0.9 * sn + 18)
    return [l1, l2], [a_back, a_front], -5 * abs(math.cos(ph))


def scene_C0(ctx, t):
    sw = 2.95
    p = ease_io(prog(t, sw - 0.6, 1.2))
    night = p
    vgrad(ctx, [(0, mixc('#6EC3F5', '#1E1B4B', p)), (0.7, mixc('#BFE6FF', '#5B3E96', p)),
                (1, mixc('#FFF1D6', '#E07A7A', p))], 0, 1300)
    # sun / moon
    sy = lerp(820, 1150, p)
    ctx.arc(820, sy, 70, 0, 2 * math.pi)
    setc(ctx, '#FFD23F', 1 - p)
    ctx.fill()
    my = lerp(1000, 720, p)
    ctx.arc(230, my, 46, 0, 2 * math.pi)
    setc(ctx, '#FFF4C2', p)
    ctx.fill()
    ctx.arc(250, my - 14, 40, 0, 2 * math.pi)
    setc(ctx, mixc('#6EC3F5', '#2A2768', p), p)
    ctx.fill()
    rnd = random.Random(12)
    for i in range(30):
        sx, sy2 = rnd.random() * W, 520 + rnd.random() * 420
        tw = 0.5 + 0.5 * math.sin(t * 3 + i)
        sparkle(ctx, sx, sy2, 3 + 3 * tw, '#FFFFFF', p * (0.4 + 0.5 * tw))
    # buildings
    rnd = random.Random(31)
    x = -30
    while x < W + 40:
        w = 90 + rnd.random() * 90
        h = 220 + rnd.random() * 280
        top = 1300 - h
        ctx.rectangle(x, top, w, h + 10)
        fill_stroke(ctx, mixc('#9FB7D9', '#2C2552', p), OUT, 4)
        for wy in range(int(top + 26), 1270, 46):
            for wx in range(int(x + 16), int(x + w - 20), 34):
                lit = rnd.random() < 0.6
                ctx.rectangle(wx, wy, 18, 24)
                setc(ctx, '#FFE08A' if (lit and p > 0.5) else mixc('#D8E6F5', '#3E3670', p))
                ctx.fill()
        x += w + 10
    # sidewalk + road
    ctx.rectangle(0, 1290, W, 70)
    setc(ctx, mixc('#D9CFC1', '#5E5578', p))
    ctx.fill()
    ctx.rectangle(0, 1355, W, H - 1355)
    setc(ctx, mixc('#6B6F7E', '#2B2A3C', p))
    ctx.fill()
    off = (t * 260) % 260
    for i in range(-1, 6):
        rrect(ctx, i * 260 - off, 1560, 150, 14, 7)
        setc(ctx, '#FFFFFF', 0.8)
        ctx.fill()
    # street lamps (scroll)
    loff = (t * 180) % 420
    for i in range(-1, 4):
        lx = i * 420 - loff + 200
        ctx.rectangle(lx - 6, 900, 12, 400)
        fill_stroke(ctx, '#4A4E69', OUT, 4)
        ctx.move_to(lx, 905)
        ctx.curve_to(lx, 860, lx + 60, 860, lx + 70, 880)
        setc(ctx, OUT)
        ctx.set_line_width(10)
        ctx.stroke()
        ellipse(ctx, lx + 72, 888, 24, 10)
        fill_stroke(ctx, '#FFF2A8' if p > 0.5 else '#D6D6D6', OUT, 4)
        if p > 0.5:
            glow_light(ctx, lx + 72, 900, 260, '#FFE08A', 0.45 * (p - 0.5) * 2)
    # banner
    for px in (80, 1000):
        ctx.rectangle(px - 9, 600, 18, 700)
        fill_stroke(ctx, '#C1121F', OUT, 4)
    rrect(ctx, 100, 640, 880, 96, 14)
    fill_stroke(ctx, '#FFFFFF', OUT, 6)
    rrect(ctx, 112, 652, 856, 72, 10)
    setc(ctx, '#E63946')
    ctx.set_line_width(4)
    ctx.stroke()
    big_text(ctx, 'BEBAS KENDARAAN', 540, 690, 58, fill='#E63946', stroke='#FFFFFF', rot=0, shadow=False)
    if p > 0.5:
        for i in range(12):
            bx = 120 + i * 76
            glow_light(ctx, bx, 742, 30, '#FFD23F', 0.6 * (0.6 + 0.4 * math.sin(t * 8 + i)))
            ctx.arc(bx, 742, 7, 0, 2 * math.pi)
            setc(ctx, '#FFD23F')
            ctx.fill()
    # crowd (background)
    for i, st in enumerate(CROWD):
        dirn = 1 if i % 2 == 0 else -1
        speed = 70 + 25 * i
        x = (120 + i * 230 + dirn * t * speed) % (W + 200) - 100
        ph = t * 9 + i
        legs, arms, bob = walk_pose(ph, 20)
        draw_person(ctx, x, 1300 + bob * 0.6, 0.62, st, flip=dirn < 0, legs=legs, arms=arms, face='smile')
    ctx.rectangle(0, 0, W, 1360)
    setc(ctx, mixc('#BFE6FF', '#2A2550', p), 0.18)
    ctx.fill()
    # friend + bagas walking
    ph = t * 9.4
    legs, arms, bob = walk_pose(ph + 1.4)
    draw_person(ctx, 360, 1400 + bob, 1.3, F1, legs=legs, arms=arms, face='laugh' if t > 3.6 else 'smile')
    legs, arms, bob = walk_pose(ph)
    ellipse(ctx, 640, 1648, 120, 14)
    setc(ctx, '#000000', 0.25)
    ctx.fill()
    face = 'grin' if p > 0.5 else 'smile'
    if 0.6 < t < 1.8:
        # waving at camera
        arms = [arms[0], (-150 + 20 * math.sin(t * 16), -170 + 25 * math.sin(t * 16))]
    draw_person(ctx, 640, 1420 + bob, 1.4, B, legs=legs, arms=arms, face=face,
                lens='#FFE08A' if p > 0.5 else None)
    # header: title changes with time of day
    chip(ctx, 'tiap weekend', 540, 385, 30, '#FFC93C', OUT, scale=back_out(prog(t, 0.25, 0.35)), rot=-2)
    if t < sw:
        big_text(ctx, 'CAR FREE DAY', 540, 500, 150, scale=back_out(prog(t, 0.35, 0.4)) * (1 - ease_in(prog(t, sw - 0.15, 0.15))))
    else:
        big_text(ctx, 'CAR FREE NIGHT', 540, 500, 150, fill='#FFC93C', scale=back_out(prog(t, sw, 0.35)))


# ---------------------------------------------------------------- C1 nongkrong
def stool(ctx, x, y, col='#8D5A3B'):
    for dx in (-30, 30):
        ctx.move_to(x + dx * 0.6, y + 15)
        ctx.line_to(x + dx, 1460)
        setc(ctx, OUT)
        ctx.set_line_width(14)
        ctx.stroke()
        ctx.move_to(x + dx * 0.6, y + 15)
        ctx.line_to(x + dx, 1460)
        setc(ctx, col)
        ctx.set_line_width(7)
        ctx.stroke()
    rrect(ctx, x - 52, y + 6, 104, 20, 9)
    fill_stroke(ctx, col, OUT, 4.5)


def glass(ctx, x, y, drink='#6B3E26', h=62):
    ctx.move_to(x - 20, y - h)
    ctx.line_to(x + 20, y - h)
    ctx.line_to(x + 16, y)
    ctx.line_to(x - 16, y)
    ctx.close_path()
    setc(ctx, '#FFFFFF', 0.55)
    ctx.fill()
    ctx.move_to(x - 18, y - h * 0.7)
    ctx.line_to(x + 18, y - h * 0.7)
    ctx.line_to(x + 16, y)
    ctx.line_to(x - 16, y)
    ctx.close_path()
    setc(ctx, drink)
    ctx.fill()
    ctx.move_to(x - 20, y - h)
    ctx.line_to(x + 20, y - h)
    ctx.line_to(x + 16, y)
    ctx.line_to(x - 16, y)
    ctx.close_path()
    setc(ctx, OUT)
    ctx.set_line_width(4)
    ctx.stroke()


def pempek(ctx, x, y):
    ellipse(ctx, x, y - 6, 92, 20)
    fill_stroke(ctx, '#FFFFFF', OUT, 4)
    for dx, dy, r in ((-40, -16, 22), (0, -22, 26), (38, -16, 22)):
        ellipse(ctx, x + dx, y + dy, r, r * 0.6)
        fill_stroke(ctx, '#E9B96E', OUT, 3.5)
    # cuko bowl
    ellipse(ctx, x + 90, y - 12, 24, 14)
    fill_stroke(ctx, '#3B2416', OUT, 4)


def scene_C1(ctx, t):
    vgrad(ctx, [(0, '#2A2F6E'), (0.55, '#C96B8C'), (1, '#F6A26B')], 0, 900)
    # wall
    ctx.rectangle(0, 760, W, 700)
    setc(ctx, '#F1D3A1')
    ctx.fill()
    # door / window glowing
    rrect(ctx, 400, 880, 280, 380, 12)
    fill_stroke(ctx, '#FFD98A', OUT, 5)
    glow_light(ctx, 540, 1060, 300, '#FFC86B', 0.35)
    for x in (120, 960):
        rrect(ctx, x - 80, 900, 160, 200, 10)
        fill_stroke(ctx, '#FFE3A3', OUT, 5)
    # awning
    for i in range(12):
        x = i * 90
        ctx.move_to(x, 690)
        ctx.line_to(x + 90, 690)
        ctx.line_to(x + 90, 790)
        ctx.arc(x + 67.5, 790, 22.5, 0, math.pi)
        ctx.arc(x + 22.5, 790, 22.5, 0, math.pi)
        ctx.close_path()
        fill_stroke(ctx, '#E63946' if i % 2 == 0 else '#FFFFFF', OUT, 4)
    # string lights
    ctx.move_to(0, 560)
    pts = []
    for i in range(0, 11):
        x = i * 108
        y = 560 + 50 * math.sin(math.pi * (i % 2 + 0.5))
        pts.append((x, 560))
    setc(ctx, OUT)
    ctx.set_line_width(3)
    ctx.move_to(-20, 560)
    for seg in range(3):
        x0 = seg * 380 - 20
        ctx.curve_to(x0 + 120, 640, x0 + 260, 640, x0 + 380, 560)
    ctx.stroke()
    cols = ['#FFD23F', '#FF7AA2', '#7CFFD8', '#FFFFFF']
    for i in range(20):
        u = i / 19
        seg = min(2, int(u * 3))
        lu = u * 3 - seg
        x0 = seg * 380 - 20
        # cubic bezier eval
        p0, p1, p2, p3 = (x0, 560), (x0 + 120, 640), (x0 + 260, 640), (x0 + 380, 560)
        bx = (1 - lu) ** 3 * p0[0] + 3 * (1 - lu) ** 2 * lu * p1[0] + 3 * (1 - lu) * lu ** 2 * p2[0] + lu ** 3 * p3[0]
        by = (1 - lu) ** 3 * p0[1] + 3 * (1 - lu) ** 2 * lu * p1[1] + 3 * (1 - lu) * lu ** 2 * p2[1] + lu ** 3 * p3[1]
        c = cols[i % 4]
        fl = 0.6 + 0.4 * math.sin(t * 6 + i * 2.1)
        glow_light(ctx, bx, by + 14, 46, c, 0.5 * fl)
        ellipse(ctx, bx, by + 14, 8, 11)
        setc(ctx, c)
        ctx.fill()
    # ground
    ctx.rectangle(0, 1440, W, H - 1440)
    setc(ctx, '#6E5040')
    ctx.fill()
    setc(ctx, '#5C4234')
    ctx.set_line_width(4)
    for i in range(8):
        ctx.move_to(0, 1480 + i * 60)
        ctx.line_to(W, 1480 + i * 60)
    ctx.stroke()
    ellipse(ctx, 540, 1462, 470, 24)
    setc(ctx, '#000000', 0.25)
    ctx.fill()

    s = 1.25
    b1 = 6 * abs(math.sin(t * 7))
    b2 = 6 * abs(math.sin(t * 7 + 1.2))
    b3 = 6 * abs(math.sin(t * 7 + 2.3))
    # friend2 behind table (front view)
    draw_person(ctx, 540, 1300 - b3, 1.2, F2, front=True, hide_legs=True, face='laugh',
                targets={'back': (500, 1236), 'front': (585, 1236)}, tilt=4 * math.sin(t * 5))
    stool(ctx, 290, 1330)
    stool(ctx, 790, 1330)
    draw_person(ctx, 290, 1325 - b1, s, B, sit=True, lean=6 + 4 * math.sin(t * 7), face='laugh',
                targets={'front': (432, 1214), 'back': (400, 1240)}, tilt=-6 + 4 * math.sin(t * 7))
    draw_person(ctx, 790, 1325 - b2, s, F1, sit=True, flip=True, lean=8, face='laugh',
                targets={'front': (660, 1240), 'back': (690, 1238)}, tilt=-5 * math.sin(t * 6))
    # table
    for lx in (420, 660):
        ctx.rectangle(lx - 9, 1262, 18, 190)
        fill_stroke(ctx, '#6B4226', OUT, 5)
    rrect(ctx, 370, 1240, 340, 24, 6)
    fill_stroke(ctx, '#9A6638', OUT, 5)
    glass(ctx, 440, 1240)
    glass(ctx, 640, 1240, '#C0392B')
    glass(ctx, 590, 1240, '#E9B96E', 54)
    pempek(ctx, 500, 1240)
    header(ctx, t, 'si paling nongkrong', 'NONGKRONG BARENG TEMEN', 118)
    bubble(ctx, 'WKWKWK', 860, 920, 64, scale=back_out(prog(t, 0.8, 0.3)), rot=6, tail=(30, 60))
    bubble(ctx, 'HAHAHA', 230, 960, 56, scale=back_out(prog(t, 1.4, 0.3)), rot=-6, fill='#FFFFFF',
           tail=(40, 60))


# ---------------------------------------------------------------- C2 catur
def piece(ctx, x, y, kind, white, rot=0, sc=1.0):
    fc = '#FAFAFA' if white else '#2A2A2A'
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rad(rot))
    ctx.scale(sc, sc)
    # base
    rrect(ctx, -17, -10, 34, 10, 4)
    fill_stroke(ctx, fc, OUT, 3.5)
    if kind == 'pawn':
        ctx.move_to(-11, -10)
        ctx.line_to(-6, -30)
        ctx.line_to(6, -30)
        ctx.line_to(11, -10)
        ctx.close_path()
        fill_stroke(ctx, fc, OUT, 3.5)
        ctx.arc(0, -36, 10, 0, 2 * math.pi)
        fill_stroke(ctx, fc, OUT, 3.5)
    elif kind == 'rook':
        ctx.rectangle(-11, -40, 22, 30)
        fill_stroke(ctx, fc, OUT, 3.5)
        ctx.move_to(-14, -40)
        for i, xx in enumerate((-14, -14, -7, -7, -2, -2, 3, 3, 8, 8, 14, 14)):
            ctx.line_to(xx, -40 - (10 if i % 4 in (1, 2) else 0))
        ctx.line_to(14, -40)
        ctx.close_path()
        fill_stroke(ctx, fc, OUT, 3.5)
    else:
        hgt = 62 if kind == 'king' else 56
        ctx.move_to(-12, -10)
        ctx.curve_to(-6, -30, -10, -hgt + 12, -12, -hgt + 6)
        ctx.line_to(12, -hgt + 6)
        ctx.curve_to(10, -hgt + 12, 6, -30, 12, -10)
        ctx.close_path()
        fill_stroke(ctx, fc, OUT, 3.5)
        if kind == 'king':
            ctx.rectangle(-3, -hgt - 12, 6, 18)
            ctx.rectangle(-8, -hgt - 6, 16, 6)
            fill_stroke(ctx, fc, OUT, 3)
        else:
            for xx in (-10, 0, 10):
                ctx.arc(xx, -hgt + 1, 5, 0, 2 * math.pi)
                fill_stroke(ctx, fc, OUT, 3)
    ctx.restore()


def scene_C2(ctx, t):
    setc(ctx, '#9ED8CF')
    ctx.paint()
    # wall decor: stripes
    for i in range(0, W, 120):
        ctx.rectangle(i, 600, 60, 840)
        setc(ctx, '#93CFC5')
        ctx.fill()
    # framed pic: knight
    rrect(ctx, 800, 640, 190, 230, 8)
    fill_stroke(ctx, '#FFF7E6', OUT, 6)
    piece(ctx, 895, 840, 'king', False, sc=2.2)
    # lamp
    ctx.move_to(540, 560)
    ctx.line_to(540, 720)
    setc(ctx, OUT)
    ctx.set_line_width(4)
    ctx.stroke()
    g = cairo.LinearGradient(0, 760, 0, 1300)
    g.add_color_stop_rgba(0, *hexc('#FFF2A8', 0.55))
    g.add_color_stop_rgba(1, *hexc('#FFF2A8', 0.0))
    ctx.move_to(490, 770)
    ctx.line_to(590, 770)
    ctx.line_to(760, 1300)
    ctx.line_to(320, 1300)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    ctx.move_to(490, 772)
    ctx.line_to(510, 720)
    ctx.line_to(570, 720)
    ctx.line_to(590, 772)
    ctx.close_path()
    fill_stroke(ctx, '#2EC4B6', OUT, 5)
    ellipse(ctx, 540, 776, 18, 8)
    setc(ctx, '#FFF7C2')
    ctx.fill()
    # floor
    ctx.rectangle(0, 1440, W, H - 1440)
    setc(ctx, '#3E6E68')
    ctx.fill()
    ellipse(ctx, 540, 1462, 460, 24)
    setc(ctx, '#000000', 0.22)
    ctx.fill()

    s = 1.25
    BH, OH = (300, 1325), (780, 1325)
    stool(ctx, BH[0], BH[1], '#2D4E4A')
    stool(ctx, OH[0], OH[1], '#2D4E4A')
    # timeline
    chin = head_point(BH[0], BH[1], s, 40, -126, 10)
    pick, place = (500, 1196), (606, 1196)
    if t < 1.0:
        hand = chin
        face_b = 'think'
    elif t < 1.5:
        p = ease_io(prog(t, 1.0, 0.5))
        hand = (lerp(chin[0], pick[0], p), lerp(chin[1], pick[1] - 30, p))
        face_b = 'focus'
    elif t < 2.05:
        p = ease_io(prog(t, 1.5, 0.55))
        hand = (lerp(pick[0], place[0], p), lerp(pick[1] - 30, place[1] - 30, p) - 70 * math.sin(math.pi * p))
        face_b = 'grin'
    else:
        p = ease_io(prog(t, 2.25, 0.4))
        hand = (lerp(place[0], 440, p), lerp(place[1] - 30, 1236, p))
        face_b = 'grin'
    lean_b = 10 if t < 1.0 else lerp(10, 24, ease_io(prog(t, 1.0, 0.5))) if t < 2.25 else lerp(24, 12, prog(t, 2.25, 0.4))
    draw_person(ctx, BH[0], BH[1], s, B, sit=True, lean=lean_b, face=face_b, look=(4, 4),
                targets={'front': hand, 'back': (410, 1240)}, tilt=6 if t < 1.0 else 2)
    shock = t > 2.1
    draw_person(ctx, OH[0], OH[1], s, F2, sit=True, flip=True, lean=8 if not shock else -6,
                face='shock' if shock else 'focus', sweat=((t * 1.5) % 1) if shock else 0,
                targets={'front': (660, 1240), 'back': (690, 1238)}, look=(4, 4))
    # table
    ctx.rectangle(531, 1262, 18, 190)
    fill_stroke(ctx, '#5A3A22', OUT, 5)
    rrect(ctx, 410, 1240, 260, 24, 6)
    fill_stroke(ctx, '#8A5A33', OUT, 5)
    # board: top face trapezoid
    bx0, bx1, by = 425, 655, 1236
    ctx.move_to(bx0, by)
    ctx.line_to(bx1, by)
    ctx.line_to(bx1 - 16, by - 26)
    ctx.line_to(bx0 + 16, by - 26)
    ctx.close_path()
    fill_stroke(ctx, '#F3E2C3', OUT, 4)
    for row in range(3):
        for col in range(8):
            if (row + col) % 2:
                continue
            ya, yb = by - row * 26 / 3, by - (row + 1) * 26 / 3
            ia = 16 * row / 3
            ib = 16 * (row + 1) / 3
            xa0 = bx0 + ia + (bx1 - bx0 - 2 * ia) * col / 8
            xa1 = bx0 + ia + (bx1 - bx0 - 2 * ia) * (col + 1) / 8
            xb0 = bx0 + ib + (bx1 - bx0 - 2 * ib) * col / 8
            xb1 = bx0 + ib + (bx1 - bx0 - 2 * ib) * (col + 1) / 8
            ctx.move_to(xa0, ya)
            ctx.line_to(xa1, ya)
            ctx.line_to(xb1, yb)
            ctx.line_to(xb0, yb)
            ctx.close_path()
            setc(ctx, '#8B5A33')
            ctx.fill()
    rrect(ctx, bx0, by, bx1 - bx0, 10, 2)
    fill_stroke(ctx, '#6B4226', OUT, 4)
    # pieces
    piece(ctx, 445, 1222, 'rook', True)
    piece(ctx, 470, 1226, 'pawn', True)
    piece(ctx, 530, 1224, 'pawn', True)
    piece(ctx, 470, 1210, 'king', True, sc=0.9)
    piece(ctx, 630, 1222, 'rook', False)
    piece(ctx, 580, 1226, 'pawn', False)
    krot = 85 * ease_out(prog(t, 2.25, 0.35))
    piece(ctx, 640, 1212, 'king', False, rot=krot, sc=0.9)
    piece(ctx, 562, 1210, 'pawn', False, sc=0.9)
    # moving queen
    if t < 1.5:
        qx, qy = pick
    elif t < 2.05:
        qx, qy = hand[0], hand[1] + 30
    else:
        qx, qy = place
    piece(ctx, qx, qy + 12, 'queen', True)
    # think dots
    if t < 1.0:
        for i in range(3):
            a = clamp((t * 3 - i * 0.6))
            ctx.arc(330 + i * 28, 880 - i * 10, 10 + i * 2, 0, 2 * math.pi)
            setc(ctx, '#FFFFFF', a)
            ctx.fill_preserve()
            setc(ctx, OUT, a)
            ctx.set_line_width(4)
            ctx.stroke()
    header(ctx, t, 'si paling skakmat', 'MAIN CATUR', 150, chipbg='#FFFFFF')
    sk = back_out(prog(t, 2.1, 0.35))
    shake = 6 * math.sin(t * 60) * (1 - prog(t, 2.1, 0.5))
    bubble(ctx, 'SKAKMAT!', 540 + shake, 900, 96, scale=sk, rot=-6, fill='#FFC93C', tail=(-80, 70))


# ---------------------------------------------------------------- C3 bioskop
def screen_color(t):
    cols = ['#4C7DFF', '#FF5E7E', '#FFD166', '#7CFFD8']
    i = int(t * 2.2) % 4
    return cols[i]


def seat(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -92, -300, 184, 300, 40)
    fill_stroke(ctx, '#B5121B', OUT, 5)
    rrect(ctx, -72, -280, 144, 250, 30)
    setc(ctx, '#D62839')
    ctx.fill()
    ctx.restore()


def seat_front(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -96, -4, 192, 40, 16)
    fill_stroke(ctx, '#C1121F', OUT, 5)
    for sx in (-110, 110):
        rrect(ctx, sx - 14, -70, 28, 120, 10)
        fill_stroke(ctx, '#3A2A3A', OUT, 4.5)
    ctx.restore()


def popcorn(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rnd = random.Random(7)
    for i in range(14):
        px, py = -40 + rnd.random() * 80, -66 - rnd.random() * 24
        ctx.arc(px, py, 13, 0, 2 * math.pi)
        fill_stroke(ctx, '#FFF4D6', OUT, 3)
    ctx.move_to(-50, -64)
    ctx.line_to(50, -64)
    ctx.line_to(38, 50)
    ctx.line_to(-38, 50)
    ctx.close_path()
    setc(ctx, '#FFFFFF')
    ctx.fill_preserve()
    ctx.save()
    ctx.clip()
    for k in range(-2, 3):
        ctx.rectangle(k * 40 - 10, -70, 20, 130)
    setc(ctx, '#E63946')
    ctx.fill()
    ctx.restore()
    ctx.move_to(-50, -64)
    ctx.line_to(50, -64)
    ctx.line_to(38, 50)
    ctx.line_to(-38, 50)
    ctx.close_path()
    setc(ctx, OUT)
    ctx.set_line_width(5)
    ctx.stroke()
    ctx.restore()


def scene_C3(ctx, t):
    setc(ctx, '#120E1F')
    ctx.paint()
    sc = screen_color(t)
    flash = clamp(1 - abs(t - 1.75) / 0.25) if 1.5 < t < 2.0 else 0
    # back wall + projector beam
    vgrad(ctx, [(0, '#1B1430'), (1, '#120E1F')], 500, 1100)
    rrect(ctx, 505, 600, 70, 40, 6)
    fill_stroke(ctx, '#FFF6D0', OUT, 4)
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_SCREEN)
    g = cairo.LinearGradient(0, 620, 0, 1500)
    g.add_color_stop_rgba(0, *hexc('#FFF6D0', 0.45))
    g.add_color_stop_rgba(1, *hexc('#FFF6D0', 0.0))
    ctx.move_to(520, 620)
    ctx.line_to(560, 620)
    ctx.line_to(1200, 1500)
    ctx.line_to(-120, 1500)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    ctx.restore()
    rnd = random.Random(11)
    for i in range(30):
        px = rnd.random() * W
        py = 700 + rnd.random() * 700
        py -= (t * 30 + i * 13) % 80
        ctx.arc(px, py, 2.5, 0, 2 * math.pi)
        setc(ctx, '#FFFFFF', 0.35)
        ctx.fill()
    # back rows silhouettes
    for row, (yy, sc_, col) in enumerate(((1060, 0.8, '#24182E'), (1140, 0.9, '#2E1E38'))):
        for i in range(7):
            x = -60 + i * 190 + (95 if row == 0 else 0)
            rrect(ctx, x - 70, yy - 150, 140, 190, 30)
            setc(ctx, col)
            ctx.fill()
            if (i + row) % 3 != 1:
                ctx.arc(x, yy - 170 + 4 * math.sin(t * 3 + i), 40 * sc_, 0, 2 * math.pi)
                setc(ctx, '#170F1F')
                ctx.fill()
                ctx.rectangle(x - 40, yy - 150, 80, 150)
                ctx.fill()
    # front row
    s = 1.45
    hipY = 1470
    pos = [(215, F1, 1.32), (540, B, s), (865, F2, 1.32)]
    for x, st, ss in pos:
        seat(ctx, x, hipY - 10 * ss, ss)
    shock = flash > 0.2 or 1.62 < t < 2.3
    for x, st, ss in pos:
        if st is B:
            cyc = (t * 1.1) % 1.0
            mouth = head_point(x, hipY, ss, 0, -140)
            top = (x + 20, hipY - 150)
            if shock:
                ft = mouth if False else (x + 60, hipY - 300)
                tgt = {'back': (x - 40, hipY - 95), 'front': (x + 70, hipY - 330)}
            else:
                p = 0.5 - 0.5 * math.cos(cyc * 2 * math.pi)
                tgt = {'back': (x - 50, hipY - 95),
                       'front': (lerp(top[0], mouth[0] + 14, p), lerp(top[1], mouth[1] + 18, p))}
            face = 'shock' if shock else ('wow' if (t * 1.1) % 1.0 > 0.35 and (t * 1.1) % 1.0 < 0.65 else 'smile')
            draw_person(ctx, x, hipY, ss, st, front=True, face=face, lens=sc,
                        targets=tgt, legs=[(-4, -2), (4, 2)], look=(0, -2),
                        pre_front=None)
            popcorn(ctx, x - 6, hipY - 90, 1.0)
            if shock:
                # popcorn burst
                pb = prog(t, 1.6, 0.7)
                rr = random.Random(5)
                for i in range(12):
                    ang = rr.uniform(-160, -20)
                    sp = rr.uniform(200, 420)
                    px = x - 6 + math.cos(rad(ang)) * sp * pb
                    py = hipY - 170 + math.sin(rad(ang)) * sp * pb + 500 * pb * pb
                    ctx.arc(px, py, 12, 0, 2 * math.pi)
                    fill_stroke(ctx, '#FFF4D6', OUT, 3)
            elif 0.4 < (t * 1.1) % 1.0 < 0.6:
                pass
        else:
            ff = 'shock' if shock else 'smile'
            if st is F1:
                tgt = {'back': (x - 30, hipY - 90), 'front': (x + 30, hipY - 100)}
                draw_person(ctx, x, hipY, ss, st, front=True, face=ff, targets=tgt, look=(0, -2))
                # drink
                dx, dy = x + 30, hipY - 100
                rrect(ctx, dx - 22, dy - 70, 44, 80, 8)
                fill_stroke(ctx, '#3A86FF', OUT, 4)
                ctx.move_to(dx + 4, dy - 70)
                ctx.line_to(dx + 12, dy - 110)
                setc(ctx, OUT)
                ctx.set_line_width(5)
                ctx.stroke()
            else:
                tgt = {'back': (x - 40, hipY - 80), 'front': (x + 40, hipY - 80)} if not shock else \
                    {'back': (x - 36, hipY - 230), 'front': (x + 36, hipY - 230)}
                draw_person(ctx, x, hipY, ss, st, front=True, face=ff, targets=tgt, look=(0, -2),
                            elbow_back='down', elbow_front='down')
    for x, st, ss in pos:
        seat_front(ctx, x, hipY + 6, ss)
    # floor
    ctx.rectangle(0, 1760, W, H - 1760)
    setc(ctx, '#0B0812')
    ctx.fill()
    # screen light tint
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_SCREEN)
    g = cairo.LinearGradient(0, 900, 0, 1920)
    g.add_color_stop_rgba(0, *hexc(sc, 0.0))
    g.add_color_stop_rgba(0.5, *hexc(sc, 0.16))
    g.add_color_stop_rgba(1, *hexc(sc, 0.06))
    ctx.set_source(g)
    ctx.paint()
    if flash > 0:
        setc(ctx, '#FFFFFF', 0.55 * flash)
        ctx.paint()
    ctx.restore()
    header(ctx, t, 'si paling update film', 'NONTON BIOSKOP', 140, chipbg='#FFFFFF')
    bubble(ctx, 'WAAA!', 760, 1000, 70, scale=back_out(prog(t, 1.65, 0.3)) * (1 - prog(t, 2.6, 0.2)),
           rot=8, fill='#FFFFFF', tail=(-50, 60))


# ---------------------------------------------------------------- Ampera
def ampera(ctx, cx, deck_y, scale, lights=0.0, t=0.0):
    red, dred = '#D62828', '#9D1C1C'
    ctx.save()
    ctx.translate(cx, deck_y)
    ctx.scale(scale, scale)
    tow = [-260, 260]
    th = 340
    # truss between towers (lifting span)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for k in range(2):
        yy = -th + 60 + k * 26
        rrect(ctx, tow[0], yy, tow[1] - tow[0], 18, 3)
        fill_stroke(ctx, red, OUT, 4)
    setc(ctx, dred)
    ctx.set_line_width(6)
    n = 10
    for i in range(n):
        x0 = tow[0] + (tow[1] - tow[0]) * i / n
        x1 = tow[0] + (tow[1] - tow[0]) * (i + 1) / n
        ctx.move_to(x0, -th + 74)
        ctx.line_to(x1, -th + 86)
    ctx.stroke()
    # hanging cables
    setc(ctx, '#5A1010')
    ctx.set_line_width(3)
    for i in range(1, 16):
        x = tow[0] + (tow[1] - tow[0]) * i / 16
        ctx.move_to(x, -th + 104)
        ctx.line_to(x, -20)
    ctx.stroke()
    # towers
    for tx in tow:
        for dx in (-38, 38):
            rrect(ctx, tx + dx - 14, -th, 28, th + 10, 4)
            fill_stroke(ctx, red, OUT, 4)
        for yy in (-th, -th + 120, -th + 220):
            rrect(ctx, tx - 52, yy, 104, 22 if yy == -th else 14, 3)
            fill_stroke(ctx, red, OUT, 4)
        # X bracing
        setc(ctx, dred)
        ctx.set_line_width(5)
        ctx.move_to(tx - 30, -th + 30)
        ctx.line_to(tx + 30, -th + 118)
        ctx.move_to(tx + 30, -th + 30)
        ctx.line_to(tx - 30, -th + 118)
        ctx.stroke()
    # side spans: arches to ends
    for sgn in (-1, 1):
        x0 = tow[0] if sgn < 0 else tow[1]
        ctx.move_to(x0, -th + 130)
        ctx.curve_to(x0 + sgn * 120, -th + 200, x0 + sgn * 260, -60, x0 + sgn * 420, -10)
        setc(ctx, OUT)
        ctx.set_line_width(14)
        ctx.stroke()
        ctx.move_to(x0, -th + 130)
        ctx.curve_to(x0 + sgn * 120, -th + 200, x0 + sgn * 260, -60, x0 + sgn * 420, -10)
        setc(ctx, red)
        ctx.set_line_width(7)
        ctx.stroke()
    # deck
    rrect(ctx, -720, -18, 1440, 30, 4)
    fill_stroke(ctx, '#7A2020', OUT, 4)
    # piers
    for tx in tow:
        ctx.rectangle(tx - 50, 12, 100, 70)
        fill_stroke(ctx, '#6F6F7A', OUT, 4)
    if lights > 0:
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_SCREEN)
        for i in range(30):
            x = -700 + i * 48
            a = lights * (0.7 + 0.3 * math.sin(t * 4 + i))
            rg = cairo.RadialGradient(x, -20, 0, x, -20, 26)
            rg.add_color_stop_rgba(0, *hexc('#FFE08A', a))
            rg.add_color_stop_rgba(1, *hexc('#FFE08A', 0))
            ctx.set_source(rg)
            ctx.arc(x, -20, 26, 0, 2 * math.pi)
            ctx.fill()
        for tx in tow:
            for yy in (-th, -th + 120, -th + 220):
                for dx in (-38, 38):
                    rg = cairo.RadialGradient(tx + dx, yy, 0, tx + dx, yy, 30)
                    rg.add_color_stop_rgba(0, *hexc('#FFD1A8', lights * 0.8))
                    rg.add_color_stop_rgba(1, *hexc('#FFD1A8', 0))
                    ctx.set_source(rg)
                    ctx.arc(tx + dx, yy, 30, 0, 2 * math.pi)
                    ctx.fill()
        ctx.restore()
    ctx.restore()


def river(ctx, y0, y1, t, base='#2D4A7A', refl='#FFB38A', speed=40):
    ctx.rectangle(0, y0, W, y1 - y0)
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, *hexc(base))
    g.add_color_stop_rgba(1, *hexc('#1D2F55'))
    ctx.set_source(g)
    ctx.fill()
    rnd = random.Random(21)
    for i in range(26):
        yy = y0 + 14 + rnd.random() * (y1 - y0 - 20)
        ln = 40 + rnd.random() * 120
        xx = (rnd.random() * (W + 300) - t * speed * (0.6 + rnd.random())) % (W + 300) - 150
        ctx.move_to(xx, yy)
        ctx.line_to(xx + ln, yy)
        setc(ctx, refl, 0.25 + 0.3 * rnd.random())
        ctx.set_line_width(5)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def scooter(ctx, x, y, t):
    # x,y = ground contact centre
    wr = 50
    rear, front = (x - 135, y - wr), (x + 140, y - wr)
    for (wx, wy) in (rear, front):
        ctx.arc(wx, wy, wr, 0, 2 * math.pi)
        fill_stroke(ctx, '#222222', OUT, 5)
        ctx.arc(wx, wy, 26, 0, 2 * math.pi)
        fill_stroke(ctx, '#BFC5D2', OUT, 4)
        setc(ctx, OUT)
        ctx.set_line_width(4)
        for k in range(3):
            a = -t * 14 + k * 2 * math.pi / 3
            ctx.move_to(wx, wy)
            ctx.line_to(wx + 24 * math.cos(a), wy + 24 * math.sin(a))
        ctx.stroke()
    # body
    ctx.move_to(x - 200, y - 110)
    ctx.curve_to(x - 205, y - 175, x - 120, y - 195, x - 40, y - 170)
    ctx.line_to(x + 40, y - 120)
    ctx.line_to(x + 80, y - 115)
    ctx.line_to(x + 120, y - 260)
    ctx.line_to(x + 160, y - 255)
    ctx.line_to(x + 150, y - 120)
    ctx.curve_to(x + 150, y - 90, x + 120, y - 80, x + 90, y - 80)
    ctx.line_to(x - 70, y - 70)
    ctx.curve_to(x - 140, y - 70, x - 195, y - 80, x - 200, y - 110)
    ctx.close_path()
    fill_stroke(ctx, '#F4F7FB', OUT, 5)
    # green stripe
    ctx.move_to(x - 190, y - 125)
    ctx.curve_to(x - 120, y - 150, x - 60, y - 130, x - 20, y - 110)
    setc(ctx, '#22E39A')
    ctx.set_line_width(12)
    ctx.stroke()
    # seat
    rrect(ctx, x - 175, y - 200, 150, 30, 14)
    fill_stroke(ctx, '#2A2A2A', OUT, 4.5)
    # handle
    ctx.move_to(x + 140, y - 258)
    ctx.line_to(x + 110, y - 300)
    setc(ctx, OUT)
    ctx.set_line_width(10)
    ctx.stroke()
    rrect(ctx, x + 84, y - 312, 46, 16, 7)
    fill_stroke(ctx, '#2A2A2A', OUT, 4)
    # headlight
    ellipse(ctx, x + 165, y - 220, 12, 16)
    fill_stroke(ctx, '#FFE66D', OUT, 4)
    return (x + 100, y - 304), (x - 105, y - 205)


def scene_C4(ctx, t):
    vgrad(ctx, [(0, '#5B2A86'), (0.45, '#E8577A'), (0.8, '#FF9A5A'), (1, '#FFC27A')], 0, 1150)
    ctx.arc(780, 1010, 150, 0, 2 * math.pi)
    setc(ctx, '#FFE3A3', 0.9)
    ctx.fill()
    glow_light(ctx, 780, 1010, 420, '#FFD08A', 0.35)
    # far skyline
    rnd = random.Random(4)
    x = -20
    while x < W:
        w = 50 + rnd.random() * 70
        h = 60 + rnd.random() * 150
        ctx.rectangle(x, 1100 - h, w, h + 10)
        setc(ctx, '#7A3E7E', 0.7)
        ctx.fill()
        x += w + 6
    ampera(ctx, 540, 1100, 0.78)
    river(ctx, 1100, 1390, t, base='#4A4E8C', refl='#FFC08A', speed=30)
    # ketek boat
    bx = (t * 60 + 150) % (W + 300) - 150
    ctx.move_to(bx - 70, 1220)
    ctx.line_to(bx + 80, 1220)
    ctx.line_to(bx + 55, 1245)
    ctx.line_to(bx - 55, 1245)
    ctx.close_path()
    fill_stroke(ctx, '#3A86FF', OUT, 4)
    rrect(ctx, bx - 40, 1185, 70, 36, 6)
    fill_stroke(ctx, '#FFC93C', OUT, 4)
    # riverbank wall + railing (scrolling)
    ctx.rectangle(0, 1390, W, 60)
    setc(ctx, '#B9A6A0')
    ctx.fill()
    off = (t * 520) % 120
    setc(ctx, OUT)
    ctx.set_line_width(5)
    ctx.move_to(0, 1352)
    ctx.line_to(W, 1352)
    ctx.stroke()
    for i in range(-1, 11):
        px = i * 120 - off
        rrect(ctx, px - 8, 1340, 16, 56, 4)
        fill_stroke(ctx, '#EDE6E3', OUT, 4)
    # road
    ctx.rectangle(0, 1450, W, H - 1450)
    setc(ctx, '#3A3A4A')
    ctx.fill()
    off2 = (t * 900) % 240
    for i in range(-1, 7):
        rrect(ctx, i * 240 - off2, 1700, 130, 16, 8)
        setc(ctx, '#FFD23F')
        ctx.fill()
    ctx.rectangle(0, 1450, W, 14)
    setc(ctx, '#262634')
    ctx.fill()
    # speed lines
    rr = random.Random(9)
    for i in range(8):
        yy = 1480 + rr.random() * 380
        xx = (rr.random() * 2000 - t * 1400 * (1 + rr.random())) % (W + 400) - 200
        ctx.move_to(xx, yy)
        ctx.line_to(xx + 120, yy)
        setc(ctx, '#FFFFFF', 0.35)
        ctx.set_line_width(5)
        ctx.stroke()
    # scooter + rider
    bob = 3 * math.sin(t * 22)
    gx, gy = 560, 1640
    ellipse(ctx, gx, gy + 6, 250, 18)
    setc(ctx, '#000000', 0.3)
    ctx.fill()
    for i in range(3):
        ph = (t * 3 + i / 3) % 1
        ctx.arc(gx - 230 - ph * 160, gy - 95 - ph * 30, 16 + ph * 26, 0, 2 * math.pi)
        setc(ctx, '#DADAE6', 0.6 * (1 - ph))
        ctx.fill()
    st = dict(B, hair='helmet', helmc='#22E39A')
    s = 1.2
    hip = (gx - 95, gy - 215 + bob)
    handle, seatp = (gx + 100, gy - 304 + bob), None
    ctx.save()
    ctx.translate(0, bob)
    scooter(ctx, gx, gy, t)
    ctx.restore()
    draw_person(ctx, hip[0], hip[1], s, st, sit=True, lean=14, face='grin', legs=[(62, -6), (72, -2)],
                targets={'front': handle, 'back': (handle[0] - 14, handle[1] + 4)}, look=(4, 0))
    # wind
    header(ctx, t, 'si anak Palembang', 'KELILING PALEMBANG', 128)


# ---------------------------------------------------------------- D ending
FIREWORKS = [(2.0, 250, 700, '#FFD23F'), (3.0, 820, 640, '#FF5E7E'), (4.4, 470, 600, '#7CFFD8'),
             (5.8, 900, 760, '#FFFFFF'), (7.2, 170, 620, '#FF9A5A'), (8.6, 760, 620, '#FFD23F'),
             (10.0, 300, 680, '#7CFFD8'), (11.2, 860, 700, '#FF5E7E'), (12.3, 520, 640, '#FFD23F')]


def firework(ctx, t, t0, x, y, col):
    p = (t - t0) / 1.3
    if p < 0 or p > 1:
        return
    if p < 0.25:
        q = p / 0.25
        yy = lerp(1150, y, ease_out(q))
        ctx.arc(x, yy, 5, 0, 2 * math.pi)
        setc(ctx, col, 0.9)
        ctx.fill()
        return
    q = (p - 0.25) / 0.75
    r = 150 * ease_out(q)
    a = 1 - q
    for i in range(18):
        ang = i * 2 * math.pi / 18
        x1 = x + math.cos(ang) * r
        y1 = y + math.sin(ang) * r + 40 * q * q
        x0 = x + math.cos(ang) * r * 0.6
        y0 = y + math.sin(ang) * r * 0.6 + 40 * q * q
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y1)
        setc(ctx, col, a)
        ctx.set_line_width(5)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    glow_light(ctx, x, y, r * 1.4, col, 0.25 * a)


D_LINE2, D_CTA = 4.3, 6.0


def scene_D(ctx, t):
    vgrad(ctx, [(0, '#1E1B4B'), (0.5, '#5B3E96'), (0.85, '#E07A7A'), (1, '#F7A072')], 0, 1240)
    rnd = random.Random(8)
    for i in range(40):
        sx, sy = rnd.random() * W, rnd.random() * 760
        tw = 0.5 + 0.5 * math.sin(t * 2.5 + i)
        sparkle(ctx, sx, sy, 3 + 4 * tw, '#FFFFFF', 0.3 + 0.5 * tw)
    for fw in FIREWORKS:
        firework(ctx, t, *fw)
    ampera(ctx, 540, 1230, 1.0, lights=1.0, t=t)
    river(ctx, 1240, 1520, t, base='#3B3A7A', refl='#FFD08A', speed=20)
    # light reflections
    for x in range(-160, W, 48):
        a = 0.25 + 0.2 * math.sin(t * 3 + x)
        for k in range(5):
            yy = 1270 + k * 45
            ctx.move_to(x + 6 * math.sin(t * 2 + k), yy)
            ctx.line_to(x + 18 + 6 * math.sin(t * 2 + k), yy)
            setc(ctx, '#FFE08A', a * (1 - k / 6))
            ctx.set_line_width(5)
            ctx.stroke()
    # plaza
    ctx.rectangle(0, 1520, W, H - 1520)
    setc(ctx, '#2A2140')
    ctx.fill()
    setc(ctx, OUT)
    ctx.set_line_width(6)
    ctx.move_to(0, 1486)
    ctx.line_to(W, 1486)
    ctx.stroke()
    for i in range(0, W + 1, 90):
        rrect(ctx, i - 7, 1478, 14, 46, 4)
        fill_stroke(ctx, '#C9BFD8', OUT, 3.5)
    ctx.rectangle(0, 1520, W, 10)
    setc(ctx, '#3D3160')
    ctx.fill()
    # character
    s = 1.45
    hip = (540, 1340)
    ellipse(ctx, hip[0], 1590, 150, 16)
    setc(ctx, '#000000', 0.35)
    ctx.fill()
    if t < 1.4:
        tg = {'back': (hip[0] - 70, hip[1] + 20), 'front': (hip[0] + 70, hip[1] + 20)}
        face = 'smile'
    elif t < 3.0:
        p = back_out(prog(t, 1.4, 0.45))
        wav = 12 * math.sin(t * 10)
        tg = {'back': (lerp(hip[0] - 70, hip[0] - 120, p), lerp(hip[1] + 20, hip[1] - 330 + wav, p)),
              'front': (lerp(hip[0] + 70, hip[0] + 120, p), lerp(hip[1] + 20, hip[1] - 330 - wav, p))}
        face = 'laugh'
    else:
        p = ease_out(prog(t, 3.0, 0.4))
        tg = {'back': (lerp(hip[0] - 120, hip[0] - 175, p), lerp(hip[1] - 330, hip[1] - 200, p)),
              'front': (lerp(hip[0] + 120, hip[0] + 175, p), lerp(hip[1] - 330, hip[1] - 200, p))}
        face = 'grin'
    jump = 0
    if 1.4 < t < 2.0:
        jump = -40 * math.sin(math.pi * prog(t, 1.4, 0.6))
    draw_person(ctx, hip[0], hip[1] + jump, s, B, front=True, face=face, targets=tg,
                elbow_back='up' if t > 1.4 else 'down', elbow_front='up' if t > 1.4 else 'down', look=(0, 0))
    if t > 3.0:
        for i in range(6):
            ph = (t * 0.9 + i / 6) % 1
            ang = i * 60 + 20
            r = 230 + 40 * ph
            sparkle(ctx, hip[0] + math.cos(rad(ang)) * r, hip[1] - 250 + math.sin(rad(ang)) * r * 0.7,
                    16 * math.sin(math.pi * ph), '#FFE66D')
    # texts
    big_text(ctx, 'GUA BAGASKARA', 540, 395, 165, scale=back_out(prog(t, 0.4, 0.5)), rot=-3)
    chip(ctx, 'IT Enthusiast', 540, 525, 40, '#FFC93C', OUT,
         scale=back_out(prog(t, 3.2, 0.4)), rot=-2)
    chip(ctx, 'yang hidup nggak cuma di depan layar.', 540, 612, 28, '#FFFFFF', OUT,
         scale=back_out(prog(t, D_LINE2, 0.4)), rot=0)
    # CTA
    sc = back_out(prog(t, D_CTA, 0.4))
    if sc > 0:
        ctx.save()
        ctx.translate(540, 1385)
        ctx.scale(sc, sc)
        w, h = 760, 150
        rrect(ctx, -w / 2 + 6, -h / 2 + 8, w, h, 26)
        setc(ctx, '#000000', 0.35)
        ctx.fill()
        rrect(ctx, -w / 2, -h / 2, w, h, 26)
        fill_stroke(ctx, '#FFFFFF', OUT, 6)
        text_center(ctx, 'Ikutin perjalanan gua,', 0, -28, 38, OUT)
        a2 = prog(t, D_CTA + 1.35, 0.3)
        if a2 > 0:
            font(ctx, 'Poppins', 42, True)
            msg = 'dari laptop sampai Ampera!'
            e = ctx.text_extents(msg)
            ctx.move_to(-e.x_advance / 2, 46 - (1 - a2) * 10)
            setc(ctx, '#E63946', a2)
            ctx.show_text(msg)
            ctx.new_path()
        ctx.restore()
    fs = back_out(prog(t, D_CTA + 2.3, 0.4))
    if fs > 0:
        pulse = 1 + 0.06 * math.sin((t - D_CTA - 2.7) * 7) if t > D_CTA + 2.7 else 1
        ctx.save()
        ctx.translate(540, 1520)
        ctx.scale(fs * pulse, fs * pulse)
        rrect(ctx, -150 + 5, -44 + 7, 300, 88, 44)
        setc(ctx, '#000000', 0.35)
        ctx.fill()
        rrect(ctx, -150, -44, 300, 88, 44)
        fill_stroke(ctx, '#E63946', OUT, 6)
        big_text(ctx, '+ FOLLOW', 0, 2, 58, fill='#FFFFFF', rot=0, shadow=False)
        ctx.restore()
    ha = prog(t, D_CTA + 2.8, 0.4)
    if ha > 0:
        font(ctx, 'Poppins', 30, True)
        e = ctx.text_extents('@bgskara_ap')
        ctx.move_to(540 - e.x_advance / 2, 1605)
        setc(ctx, '#FFFFFF', ha)
        ctx.show_text('@bgskara_ap')
        ctx.new_path()


# ---------------------------------------------------------------- compose
SCENES = [(T_A, T_B, scene_A), (T_B, T_C0, scene_B), (T_C0, T_C1, scene_C0), (T_C1, T_C2, scene_C1), (T_C2, T_C3, scene_C2),
          (T_C3, T_C4, scene_C3), (T_C4, T_D, scene_C4), (T_D, T_END, scene_D)]


def scene_at(ctx, t):
    for a, b, fn in SCENES:
        if a <= t < b or (fn is scene_D and t >= a):
            fn(ctx, t - a)
            return


def wipe(ctx, t):
    for tb, col in WIPES:
        if tb - WIPE_HALF <= t <= tb + WIPE_HALF:
            p = ease_io((t - tb + WIPE_HALF) / (2 * WIPE_HALF))
            off = lerp(H + 260, -(H + 640), p)
            for k, (c, d) in enumerate(((OUT, 0), (col, 30))):
                y0 = off + d
                ctx.move_to(0, y0 + 150)
                ctx.line_to(W, y0 - 150)
                ctx.line_to(W, y0 + H + 250)
                ctx.line_to(0, y0 + H + 550)
                ctx.close_path()
                setc(ctx, c)
                ctx.fill()


def frame(ctx, t):
    CLOCK[0] = t
    ctx.save()
    scene_at(ctx, t)
    ctx.restore()
    if XFADE[0] <= t < XFADE[1]:
        a = ease_io((t - XFADE[0]) / (XFADE[1] - XFADE[0]))
        ctx.push_group()
        scene_B(ctx, 0.0)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(a)
    wipe(ctx, t)
    # fade out at end
    if t > T_END - 0.5:
        setc(ctx, '#000000', clamp((t - (T_END - 0.5)) / 0.5) * 0.9)
        ctx.paint()


VO = [('a', 0.4), ('a2', 5.9), ('b1', T_B + 0.15), ('b2', T_B + 2.35), ('c0', T_C0 + 0.3), ('c1', T_C1 + 0.25),
      ('c2', T_C2 + 0.25), ('c3', T_C3 + 0.25), ('c4', T_C4 + 0.25), ('d1', T_D + 0.4),
      ('d2', T_D + 3.15), ('d3', T_D + 5.65)]

SFX = ([('pop', st) for _, _, _, st in CARDS] + [('alert', 4.6), ('close', 9.55), ('pop', 12.25)] +
       [('whoosh', tb - 0.3) for tb, _ in WIPES] + [('whoosh', 7.5)] +
       [('pop', T_C0 + 3.15), ('pop', T_C1 + 0.8), ('pop', T_C1 + 1.4), ('pop', T_C2 + 2.1), ('scare', T_C3 + 1.6),
        ('pop', T_D + 0.4), ('pop', T_D + 3.2), ('pop', T_D + D_LINE2), ('pop', T_D + D_CTA),
        ('pop', T_D + D_CTA + 1.35), ('ding', T_D + D_CTA + 2.3)] + [('boom', T_D + f[0] + 0.33) for f in FIREWORKS])
