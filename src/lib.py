import cairo, math

W, H, FPS = 1080, 1920, 30
OUT = '#141414'


def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def setc(ctx, h, a=1.0):
    ctx.set_source_rgba(*hexc(h, a))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, t):
    return a + (b - a) * t


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = clamp(t)
    return t ** 3


def ease_io(t):
    t = clamp(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def back_out(t):
    t = clamp(t)
    c1 = 2.0
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def prog(t, start, dur):
    return clamp((t - start) / dur)


def rad(d):
    return d * math.pi / 180


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def fill_stroke(ctx, fill, stroke=OUT, lw=5, a=1.0):
    if fill:
        setc(ctx, fill, a)
        if stroke:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if stroke:
        setc(ctx, stroke, a)
        ctx.set_line_width(lw)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke()


def ellipse(ctx, cx, cy, rx, ry):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def vgrad(ctx, stops, y0=0, y1=H, x=0, w=W):
    g = cairo.LinearGradient(0, y0, 0, y1)
    for off, col in stops:
        g.add_color_stop_rgba(off, *hexc(col))
    ctx.rectangle(x, y0, w, y1 - y0)
    ctx.set_source(g)
    ctx.fill()


def font(ctx, family, size, bold=False):
    ctx.select_font_face(family, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def big_text(ctx, text, cx, cy, size, fill='#FFFFFF', stroke=OUT, rot=-3, scale=1.0,
             maxw=1000, alpha=1.0, shadow=True):
    if scale <= 0.001 or alpha <= 0:
        return
    ctx.save()
    font(ctx, 'Bangers', size)
    e = ctx.text_extents(text)
    if e.x_advance > maxw:
        size *= maxw / e.x_advance
        font(ctx, 'Bangers', size)
        e = ctx.text_extents(text)
    ctx.translate(cx, cy)
    ctx.rotate(rad(rot))
    ctx.scale(scale, scale)
    x = -e.x_advance / 2
    y = -(e.y_bearing + e.height / 2)
    if shadow:
        ctx.move_to(x + 7, y + 9)
        ctx.text_path(text)
        setc(ctx, '#000000', 0.35 * alpha)
        ctx.set_line_width(size * 0.16)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
        ctx.fill()
    ctx.move_to(x, y)
    ctx.text_path(text)
    setc(ctx, stroke, alpha)
    ctx.set_line_width(size * 0.16)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke_preserve()
    setc(ctx, fill, alpha)
    ctx.fill()
    ctx.restore()


def text_center(ctx, text, cx, cy, size, color, family='Poppins', bold=True):
    font(ctx, family, size, bold)
    e = ctx.text_extents(text)
    ctx.move_to(cx - e.x_advance / 2, cy - (e.y_bearing + e.height / 2))
    setc(ctx, color)
    ctx.show_text(text)
    ctx.new_path()
    return e


def chip(ctx, text, cx, cy, size=30, bg='#111111', fg='#FFFFFF', scale=1.0, rot=0,
         border=None, padx=28, pady=14, bold=True, shadow=True):
    if scale <= 0.001:
        return
    ctx.save()
    font(ctx, 'Poppins', size, bold)
    e = ctx.text_extents(text)
    w = e.x_advance + padx * 2
    h = size * 1.15 + pady * 2
    ctx.translate(cx, cy)
    ctx.rotate(rad(rot))
    ctx.scale(scale, scale)
    if shadow:
        rrect(ctx, -w / 2 + 5, -h / 2 + 7, w, h, h / 2)
        setc(ctx, '#000000', 0.3)
        ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2)
    fill_stroke(ctx, bg, border or OUT, 4)
    font(ctx, 'Poppins', size, bold)
    ctx.move_to(-e.x_advance / 2, -(e.y_bearing + e.height / 2))
    setc(ctx, fg)
    ctx.show_text(text)
    ctx.new_path()
    ctx.restore()


def bubble(ctx, text, cx, cy, size=70, scale=1.0, rot=-6, fill='#FFC93C', fg=OUT, tail=(-40, 60)):
    if scale <= 0.001:
        return
    ctx.save()
    font(ctx, 'Bangers', size)
    e = ctx.text_extents(text)
    w = e.x_advance + 50
    h = size * 1.1 + 30
    ctx.translate(cx, cy)
    ctx.rotate(rad(rot))
    ctx.scale(scale, scale)
    # tail
    tx, ty = tail
    ctx.move_to(-18, h / 2 - 6)
    ctx.line_to(tx, ty + h / 2)
    ctx.line_to(18, h / 2 - 6)
    ctx.close_path()
    rrect(ctx, -w / 2, -h / 2, w, h, 22)
    setc(ctx, '#000000', 0.3)
    ctx.save()
    ctx.translate(6, 8)
    ctx.restore()
    fill_stroke(ctx, fill, OUT, 7)
    # redraw body without inner seam
    rrect(ctx, -w / 2 + 4, -h / 2 + 4, w - 8, h - 8, 18)
    setc(ctx, fill)
    ctx.fill()
    font(ctx, 'Bangers', size)
    ctx.move_to(-e.x_advance / 2, -(e.y_bearing + e.height / 2))
    setc(ctx, fg)
    ctx.show_text(text)
    ctx.new_path()
    ctx.restore()


def sparkle(ctx, x, y, r, color='#FFE66D', a=1.0):
    if r <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.move_to(0, -r)
    ctx.curve_to(r * 0.15, -r * 0.15, r * 0.15, -r * 0.15, r, 0)
    ctx.curve_to(r * 0.15, r * 0.15, r * 0.15, r * 0.15, 0, r)
    ctx.curve_to(-r * 0.15, r * 0.15, -r * 0.15, r * 0.15, -r, 0)
    ctx.curve_to(-r * 0.15, -r * 0.15, -r * 0.15, -r * 0.15, 0, -r)
    setc(ctx, color, a)
    ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- character (v2: big-head cartoon style)

CLOCK = [0.0]

STYLES = {
    'bagas': dict(skin='#F6C9A4', hair='messy', hairc='#17171C', vest='#1D2133', vest_l='#323957',
                  sleeve='#FFFFFF', shirt='#1D2133', shoe='#17171C', shades=True, logo=True, zip='#22E39A'),
    'f1': dict(skin='#C98B5E', hair='short', hairc='#2B1B12', vest=None, shirt='#F28C38', shirt_d='#C96A1E',
               sleeve='#F28C38', shoe='#17171C', shades=False, seed=0.31),
    'f2': dict(skin='#E9B48B', hair='cap', hairc='#141414', capc='#E63946', vest=None, shirt='#3A86FF',
               shirt_d='#2563C9', sleeve='#3A86FF', shoe='#17171C', shades=False, seed=0.73),
}

L_TH, L_SH, L_UA, L_FA = 80, 80, 60, 56
HEAD_C, HEAD_R = -170, 60
SH_Y = -98


def vdir(a):
    return math.sin(rad(a)), math.cos(rad(a))


def ang_of(dx, dy):
    return math.degrees(math.atan2(dx, dy))


def ik(sh, tg, l1, l2, elbow='down'):
    dx, dy = tg[0] - sh[0], tg[1] - sh[1]
    d = math.hypot(dx, dy)
    d = clamp(d, abs(l1 - l2) + 1, l1 + l2 - 0.5)
    phi = ang_of(dx, dy)
    c = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)
    al = math.degrees(math.acos(c))
    best = None
    for a1 in (phi + al, phi - al):
        ex, ey = sh[0] + l1 * vdir(a1)[0], sh[1] + l1 * vdir(a1)[1]
        a2 = ang_of(tg[0] - ex, tg[1] - ey)
        key = ey if elbow == 'down' else -ey
        if best is None or key > best[0]:
            best = (key, a1, a2)
    return best[1], best[2]


def limb(ctx, p, angs, lens, width, color, outline=8):
    pts = [p]
    for a, l in zip(angs, lens):
        dx, dy = vdir(a)
        pts.append((pts[-1][0] + l * dx, pts[-1][1] + l * dy))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    passes = [(width + outline, OUT), (width, color)] if outline else [(width, color)]
    for w, c in passes:
        ctx.move_to(*pts[0])
        for q in pts[1:]:
            ctx.line_to(*q)
        setc(ctx, c)
        ctx.set_line_width(w)
        ctx.stroke()
    return pts


def draw_arm(ctx, st, sh, pose, which):
    tg = pose['targets'].get(which)
    if tg is not None:
        lx, ly = ctx.device_to_user(*tg)
        a1, a2 = ik(sh, (lx, ly), L_UA, L_FA, pose.get('elbow_' + which, 'down'))
    else:
        a1, a2 = pose['arms'][0 if which == 'back' else 1]
    pts = limb(ctx, sh, (a1, a2), (L_UA, L_FA), 30, st['sleeve'])
    # sleeve shading line
    hx, hy = pts[-1]
    ctx.arc(hx, hy, 11, 0, 2 * math.pi)
    fill_stroke(ctx, st['skin'], OUT, 4.5)
    return ctx.user_to_device(hx, hy)


def draw_leg(ctx, st, hip, angs, front_view):
    pts = limb(ctx, hip, angs, (L_TH, L_SH), 5, OUT, outline=5)
    fx, fy = pts[-1]
    if front_view:
        ellipse(ctx, fx, fy + 4, 17, 10)
    else:
        ellipse(ctx, fx + 10, fy + 2, 21, 10)
    fill_stroke(ctx, st['shoe'], OUT, 3)


def torso_path(ctx):
    ctx.move_to(-38, 6)
    ctx.line_to(38, 6)
    ctx.line_to(42, -88)
    ctx.curve_to(42, -118, -42, -118, -42, -88)
    ctx.close_path()


def draw_torso(ctx, st, front_view):
    cx = 0 if front_view else 10
    if st.get('vest'):
        # white undershirt collar
        ellipse(ctx, cx * 0.4, -108, 24, 12)
        fill_stroke(ctx, st['sleeve'], OUT, 4)
        torso_path(ctx)
        fill_stroke(ctx, st['vest'], OUT, 6)
        ctx.save()
        torso_path(ctx)
        ctx.clip()
        setc(ctx, st['vest_l'])
        ctx.set_line_width(4)
        for y in (-80, -54, -28):
            ctx.move_to(-50, y)
            ctx.curve_to(-20, y + 5, 20, y + 5, 50, y)
        ctx.stroke()
        ctx.move_to(cx, -112)
        ctx.line_to(cx, 8)
        setc(ctx, st['zip'])
        ctx.set_line_width(5)
        ctx.stroke()
        ctx.restore()
        if st.get('logo') and front_view:
            font(ctx, 'DejaVu Sans Mono', 20, True)
            ctx.move_to(cx - (34 if front_view else 30), -78)
            setc(ctx, st['zip'])
            ctx.show_text('>_')
            ctx.new_path()
        # high collar of vest
        ctx.move_to(cx - 26, -104)
        ctx.curve_to(cx - 20, -118, cx + 20, -118, cx + 26, -104)
        setc(ctx, OUT)
        ctx.set_line_width(5)
        ctx.stroke()
    else:
        torso_path(ctx)
        fill_stroke(ctx, st['shirt'], OUT, 6)
        ctx.arc(cx, -110, 15, 0.15 * math.pi, 0.85 * math.pi)
        setc(ctx, st['shirt_d'])
        ctx.set_line_width(5)
        ctx.stroke()


def draw_hair(ctx, st, front_view):
    kind = st['hair']
    hc = st['hairc']
    if kind == 'messy':
        if front_view:
            pts = [(-56, -170), (-58, -204), (-50, -230), (-40, -252), (-24, -244), (-12, -268), (2, -248),
                   (16, -270), (26, -246), (42, -256), (46, -232), (56, -210), (56, -172),
                   (48, -190), (40, -206), (30, -198), (20, -212), (8, -202), (-4, -214), (-16, -202),
                   (-28, -212), (-38, -198), (-48, -190)]
        else:
            pts = [(-55, -168), (-58, -200), (-50, -228), (-44, -252), (-28, -244), (-20, -268), (-4, -248),
                   (10, -270), (20, -248), (38, -256), (42, -232), (56, -214), (52, -204), (44, -212),
                   (36, -202), (26, -214), (16, -204), (6, -216), (-4, -204), (-16, -214), (-26, -198),
                   (-34, -190), (-40, -172), (-46, -160)]
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.close_path()
        fill_stroke(ctx, hc, OUT, 5)
        # shine
        ctx.move_to(-30, -240)
        ctx.curve_to(-18, -250, 0, -252, 12, -248)
        setc(ctx, '#FFFFFF', 0.25)
        ctx.set_line_width(5)
        ctx.stroke()
    elif kind in ('short', 'cap'):
        ctx.new_sub_path()
        ctx.arc(0, -182, 55, math.pi * 1.02, math.pi * 1.98)
        if front_view:
            ctx.curve_to(40, -210, -40, -210, -55, -186)
        else:
            ctx.curve_to(40, -214, 0, -200, -55, -178)
        ctx.close_path()
        fill_stroke(ctx, hc, OUT, 5)
        if kind == 'cap':
            ctx.new_sub_path()
            ctx.arc(0, -188, 56, math.pi, 2 * math.pi)
            ctx.close_path()
            fill_stroke(ctx, st['capc'], OUT, 5)
            ctx.arc(0, -244, 6, 0, 2 * math.pi)
            fill_stroke(ctx, st['capc'], OUT, 3)
            if front_view:
                ellipse(ctx, 0, -190, 56, 11)
            else:
                rrect(ctx, 20, -196, 60, 13, 6)
            fill_stroke(ctx, st['capc'], OUT, 5)
    elif kind == 'helmet':
        ctx.new_sub_path()
        ctx.arc(0, -186, 64, math.pi * 0.95, math.pi * 2.05)
        ctx.close_path()
        fill_stroke(ctx, st['helmc'], OUT, 5)
        setc(ctx, '#FFFFFF', 0.6)
        ctx.set_line_width(7)
        ctx.arc(0, -186, 50, math.pi * 1.25, math.pi * 1.55)
        ctx.stroke()
        if not front_view:
            rrect(ctx, 30, -202, 46, 12, 6)
            fill_stroke(ctx, '#222222', OUT, 4)


def shades(ctx, front_view, tint=None):
    if front_view:
        lenses = [(-50, -8), (8, 50)]
    else:
        lenses = [(-6, 22), (27, 55)]
    y0, y1 = -200, -170
    g = cairo.LinearGradient(lenses[0][0], y0, lenses[1][1], y1)
    g.add_color_stop_rgba(0, *hexc('#2EF2C9'))
    g.add_color_stop_rgba(0.5, *hexc('#3A86FF'))
    g.add_color_stop_rgba(1, *hexc('#A35CFF'))
    for x0, x1 in lenses:
        rrect(ctx, x0, y0, x1 - x0, y1 - y0, 9)
        ctx.set_source(g)
        ctx.fill_preserve()
        if tint:
            setc(ctx, tint, 0.35)
            ctx.fill_preserve()
        setc(ctx, OUT)
        ctx.set_line_width(5)
        ctx.stroke()
        # glare
        ctx.move_to(x0 + 6, y1 - 6)
        ctx.line_to(x0 + 16, y0 + 5)
        setc(ctx, '#FFFFFF', 0.75)
        ctx.set_line_width(4)
        ctx.stroke()
    setc(ctx, OUT)
    ctx.set_line_width(5)
    ctx.move_to(lenses[0][1], -192)
    ctx.line_to(lenses[1][0], -192)
    ctx.stroke()
    if not front_view:
        ctx.move_to(lenses[0][0], -190)
        ctx.line_to(-38, -182)
        ctx.stroke()


def draw_face(ctx, st, pose, front_view):
    face = pose.get('face', 'smile')
    look = pose.get('look', (2, 0))
    if front_view:
        eyes = [(-19, -184), (19, -184)]
        mx = 0
    else:
        eyes = [(10, -184), (40, -184)]
        mx = 30
    my = -152
    tm = pose.get('tm', 0)
    blink = ((tm * 0.42 + st.get('seed', 0.5)) % 1.0) < 0.045
    if not st.get('shades'):
        for ex, ey in eyes:
            if face in ('happy', 'laugh') or blink:
                ctx.arc(ex, ey + 3, 7, math.pi * 1.1, math.pi * 1.9)
                setc(ctx, OUT)
                ctx.set_line_width(4.5)
                ctx.stroke()
            else:
                r = 7 if face in ('shock', 'wow') else 6
                ctx.arc(ex + look[0], ey + look[1], r, 0, 2 * math.pi)
                setc(ctx, OUT)
                ctx.fill()
                ctx.arc(ex + look[0] + 2, ey + look[1] - 2, 2, 0, 2 * math.pi)
                setc(ctx, '#FFFFFF')
                ctx.fill()
    # brows
    setc(ctx, OUT)
    ctx.set_line_width(5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    by0 = -212 if st.get('shades') else -206
    for i, (ex, ey) in enumerate(eyes):
        by = by0
        if face in ('worried', 'shock'):
            inner = 1 if i == 0 else -1
            ctx.move_to(ex - 9, by - 4 * inner - (6 if face == 'shock' else 0))
            ctx.line_to(ex + 9, by + 4 * inner - (6 if face == 'shock' else 0))
        elif face == 'think':
            ctx.move_to(ex - 9, by + (3 if i == 0 else -5))
            ctx.line_to(ex + 9, by + (-3 if i == 0 else -5))
        elif face in ('grin', 'laugh', 'happy'):
            ctx.move_to(ex - 9, by + 1)
            ctx.curve_to(ex - 3, by - 5, ex + 3, by - 5, ex + 9, by + 1)
        else:
            if st.get('shades'):
                continue
            ctx.move_to(ex - 9, by)
            ctx.line_to(ex + 9, by - 2)
        ctx.stroke()
    if st.get('shades'):
        shades(ctx, front_view, pose.get('lens'))
    # mouth
    setc(ctx, OUT)
    ctx.set_line_width(5)
    if face in ('smile', 'happy'):
        ctx.arc(mx, my - 12, 15, rad(25), rad(155))
        ctx.stroke()
    elif face in ('grin', 'laugh', 'wow'):
        wdt = 19 if face != 'wow' else 12
        dep = 26 if face == 'laugh' else (20 if face == 'grin' else 16)
        ctx.move_to(mx - wdt, my - 6)
        ctx.curve_to(mx - wdt + 2, my + dep, mx + wdt - 2, my + dep, mx + wdt, my - 6)
        ctx.close_path()
        fill_stroke(ctx, '#6B1D1D', OUT, 4.5)
        if face != 'wow':
            ctx.rectangle(mx - wdt + 3, my - 5, wdt * 2 - 6, 6)
            setc(ctx, '#FFFFFF')
            ctx.fill()
            ellipse(ctx, mx, my + dep * 0.55, wdt * 0.5, 5)
            setc(ctx, '#FF7B8A')
            ctx.fill()
    elif face == 'shock':
        ellipse(ctx, mx, my, 10, 13)
        fill_stroke(ctx, '#6B1D1D', OUT, 4)
    elif face == 'worried':
        ctx.move_to(mx - 14, my)
        ctx.curve_to(mx - 7, my - 7, mx - 2, my + 5, mx + 4, my - 2)
        ctx.curve_to(mx + 8, my - 7, mx + 12, my, mx + 14, my - 2)
        ctx.stroke()
    else:
        ctx.move_to(mx - 11, my - 2)
        ctx.line_to(mx + 11, my - 4)
        ctx.stroke()
    if face in ('laugh', 'happy', 'grin', 'smile'):
        for ex, ey in eyes:
            ellipse(ctx, ex + (4 if not front_view else 0), ey + 26, 10, 6)
            setc(ctx, '#FF7B9C', 0.35)
            ctx.fill()
    if pose.get('sweat', 0) > 0:
        sx = -46 if not front_view else 54
        ctx.save()
        ctx.translate(sx, -214 + 12 * pose['sweat'])
        ctx.move_to(0, -16)
        ctx.curve_to(10, 0, 10, 12, 0, 12)
        ctx.curve_to(-10, 12, -10, 0, 0, -16)
        fill_stroke(ctx, '#7FD6FF', OUT, 3.5)
        ctx.restore()


def draw_head(ctx, st, pose, front_view):
    tilt = pose.get('tilt', 0)
    ctx.save()
    ctx.translate(0, -112)
    ctx.rotate(rad(tilt))
    ctx.translate(0, 112)
    # map old head space (centre 0,-182 r52) onto new (0,HEAD_C r HEAD_R)
    k = HEAD_R / 52
    ctx.translate(0, HEAD_C)
    ctx.scale(k, k)
    ctx.translate(0, 182)
    if front_view:
        for sx in (-52, 52):
            ctx.arc(sx, -178, 11, 0, 2 * math.pi)
            fill_stroke(ctx, st['skin'], OUT, 4.5)
    ctx.arc(0, -182, 52, 0, 2 * math.pi)
    fill_stroke(ctx, st['skin'], OUT, 5.5)
    if not front_view:
        ellipse(ctx, -36, -170, 8, 11)
        fill_stroke(ctx, st['skin'], OUT, 4)
    draw_face(ctx, st, pose, front_view)
    draw_hair(ctx, st, front_view)
    ctx.restore()


def draw_person(ctx, x, y, s, st, **kw):
    pose = dict(lean=0, tilt=0, face='smile', front=False, flip=False, sit=False, legs=None,
                arms=None, targets={}, sweat=0, tm=CLOCK[0])
    pose.update(kw)
    front = pose['front']
    if pose['legs'] is None:
        if front:
            pose['legs'] = [(-4, -2), (4, 2)]
        elif pose['sit']:
            pose['legs'] = [(84, -4), (92, 2)]
        else:
            pose['legs'] = [(-6, -2), (6, 0)]
    if pose['arms'] is None:
        pose['arms'] = [(-22, -12), (22, 12)] if front else [(8, 18), (14, 30)]
    br = 1 + 0.018 * math.sin(pose['tm'] * 2.6 + st.get('seed', 0) * 6)
    hands = {}
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if pose['flip'] else s, s)
    if front:
        if not pose.get('hide_legs'):
            draw_leg(ctx, st, (-16, 0), pose['legs'][0], True)
            draw_leg(ctx, st, (16, 0), pose['legs'][1], True)
        ctx.save()
        ctx.rotate(rad(pose['lean']))
        ctx.scale(1, br)
        draw_torso(ctx, st, True)
        draw_head(ctx, st, pose, True)
        hands['back'] = draw_arm(ctx, st, (-36, SH_Y), pose, 'back')
        hands['front'] = draw_arm(ctx, st, (36, SH_Y), pose, 'front')
        ctx.restore()
    else:
        ctx.save()
        ctx.rotate(rad(pose['lean']))
        ctx.scale(1, br)
        hands['back'] = draw_arm(ctx, st, (-2, SH_Y), pose, 'back')
        ctx.restore()
        if not pose.get('hide_legs'):
            draw_leg(ctx, st, (-4, 0), pose['legs'][0], False)
            draw_leg(ctx, st, (4, 0), pose['legs'][1], False)
        ctx.save()
        ctx.rotate(rad(pose['lean']))
        ctx.scale(1, br)
        draw_torso(ctx, st, False)
        draw_head(ctx, st, pose, False)
        hands['front'] = draw_arm(ctx, st, (6, SH_Y), pose, 'front')
        ctx.restore()
    ctx.restore()
    return hands


def head_point(x, y, s, lx, ly, lean=0, flip=False):
    c, si = math.cos(rad(lean)), math.sin(rad(lean))
    rx, ry = lx * c - ly * si, lx * si + ly * c
    return x + (-rx if flip else rx) * s, y + ry * s
