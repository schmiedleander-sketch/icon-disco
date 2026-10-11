import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_icons():
    output_dir = "icons"
    os.makedirs(output_dir, exist_ok=True)

    # Draw at 1024x1024 for high quality supersampling
    S = 1024

    def get_canvas():
        return Image.new("RGBA", (S, S), (0, 0, 0, 0))

    def draw_linear_gradient_rounded_rect(size, box, radius, color_top, color_bottom):
        grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        for y in range(box[1], box[3]):
            factor = (y - box[1]) / float(max(1, box[3] - box[1]))
            r = int(color_top[0] + factor * (color_bottom[0] - color_top[0]))
            g = int(color_top[1] + factor * (color_bottom[1] - color_top[1]))
            b = int(color_top[2] + factor * (color_bottom[2] - color_top[2]))
            a = int(color_top[3] + factor * (color_bottom[3] - color_top[3])) if len(color_top)>3 and len(color_bottom)>3 else 255

            line_img = Image.new("RGBA", (size, 1), (r, g, b, a))
            grad.paste(line_img, (0, y))

        mask = Image.new("L", (size, size), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle(box, radius=radius, fill=255)

        result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        result.paste(grad, (0, 0), mask)
        return result

    def add_drop_shadow(base_img, offset=(0, 20), blur=30, shadow_color=(0, 0, 0, 80)):
        alpha = base_img.split()[3]
        shadow = Image.new("RGBA", base_img.size, shadow_color)
        shadow_mask = alpha.filter(ImageFilter.GaussianBlur(blur))

        canvas = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
        canvas.paste(shadow, offset, shadow_mask)
        canvas.alpha_composite(base_img)
        return canvas

    # --- 1. Text Editor ---
    def make_text_editor():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (24, 119, 242, 255), (10, 60, 160, 255))
        img = Image.alpha_composite(img, bg)

        doc = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(doc)
        doc_box = (320, 240, 704, 780)
        ddraw.rounded_rectangle(doc_box, radius=40, fill=(255, 255, 255, 245))

        lines_y = [360, 430, 500, 570, 640]
        widths = [280, 320, 240, 300, 180]
        for y, w in zip(lines_y, widths):
            ddraw.rounded_rectangle((360, y, 360 + w, y + 24), radius=12, fill=(0, 102, 204, 200))

        ddraw.rounded_rectangle((320, 240, 704, 300), radius=30, fill=(0, 180, 230, 255))
        doc = add_drop_shadow(doc, offset=(0, 15), blur=20, shadow_color=(0, 0, 0, 60))
        return Image.alpha_composite(img, doc)

    # --- 2. Settings ---
    def make_settings():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (60, 64, 72, 255), (30, 32, 38, 255))
        img = Image.alpha_composite(img, bg)

        gear = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(gear)

        cx, cy = S // 2, S // 2
        r_outer = 260
        num_teeth = 8

        for i in range(num_teeth):
            angle = i * (2 * math.pi / num_teeth)
            dx = math.cos(angle)
            dy = math.sin(angle)
            tx = cx + dx * 320
            ty = cy + dy * 320
            gdraw.line((cx, cy, tx, ty), fill=(220, 225, 230, 255), width=90)

        gdraw.ellipse((cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer), fill=(220, 225, 230, 255))
        gdraw.ellipse((cx - 100, cy - 100, cx + 100, cy + 100), fill=(45, 48, 55, 255))

        gear = add_drop_shadow(gear, offset=(0, 10), blur=25, shadow_color=(0, 0, 0, 80))
        return Image.alpha_composite(img, gear)

    # --- 3. File Explorer ---
    def make_file_explorer():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (30, 40, 50, 255), (15, 20, 30, 255))
        img = Image.alpha_composite(img, bg)

        folder = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        fdraw = ImageDraw.Draw(folder)

        fdraw.rounded_rectangle((240, 280, 500, 400), radius=30, fill=(230, 160, 30, 255))
        fdraw.rounded_rectangle((240, 340, 780, 740), radius=40, fill=(255, 195, 45, 255))

        doc = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(doc)
        ddraw.rounded_rectangle((320, 240, 700, 500), radius=25, fill=(245, 247, 250, 255))
        ddraw.rounded_rectangle((360, 290, 520, 310), radius=10, fill=(0, 120, 215, 255))
        ddraw.rounded_rectangle((360, 330, 620, 345), radius=8, fill=(180, 190, 200, 255))
        ddraw.rounded_rectangle((360, 365, 580, 380), radius=8, fill=(180, 190, 200, 255))

        flap = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(flap)
        pdraw.rounded_rectangle((240, 420, 780, 740), radius=40, fill=(255, 210, 65, 255))

        img = Image.alpha_composite(img, add_drop_shadow(folder, blur=10))
        img = Image.alpha_composite(img, add_drop_shadow(doc, blur=15))
        img = Image.alpha_composite(img, add_drop_shadow(flap, blur=20))
        return img

    # --- 4. Media Player ---
    def make_media_player():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (130, 40, 220, 255), (70, 15, 140, 255))
        img = Image.alpha_composite(img, bg)

        overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        cx, cy = S // 2, S // 2
        odraw.ellipse((cx - 240, cy - 240, cx + 240, cy + 240), outline=(255, 255, 255, 120), width=16)
        points = [(cx - 70, cy - 120), (cx - 70, cy + 120), (cx + 130, cy)]
        odraw.polygon(points, fill=(255, 255, 255, 255))

        overlay = add_drop_shadow(overlay, offset=(0, 10), blur=25, shadow_color=(0, 0, 0, 90))
        return Image.alpha_composite(img, overlay)

    # --- 5. Web Browser ---
    def make_web_browser():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (0, 160, 230, 255), (0, 70, 170, 255))
        img = Image.alpha_composite(img, bg)

        globe = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(globe)

        cx, cy = S // 2, S // 2
        r = 250
        gdraw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 220), width=18)
        gdraw.ellipse((cx - r, cy - 100, cx + r, cy + 100), outline=(255, 255, 255, 160), width=12)
        gdraw.line((cx - r, cy, cx + r, cy), fill=(255, 255, 255, 200), width=14)
        gdraw.ellipse((cx - 110, cy - r, cx + 110, cy + r), outline=(255, 255, 255, 160), width=12)
        gdraw.line((cx, cy - r, cx, cy + r), fill=(255, 255, 255, 200), width=14)

        p_arrow = [(cx + 120, cy + 80), (cx + 220, cy + 220), (cx + 160, cy + 220), (cx + 130, cy + 270), (cx + 100, cy + 220)]
        gdraw.polygon(p_arrow, fill=(255, 215, 0, 255), outline=(255, 255, 255, 255), width=6)

        globe = add_drop_shadow(globe, offset=(0, 15), blur=25)
        return Image.alpha_composite(img, globe)

    # --- 6. Calculator ---
    def make_calculator():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (16, 160, 120, 255), (8, 80, 65, 255))
        img = Image.alpha_composite(img, bg)

        calc = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(calc)

        cdraw.rounded_rectangle((240, 220, 780, 380), radius=25, fill=(20, 35, 30, 220), outline=(255, 255, 255, 80), width=6)
        cdraw.rounded_rectangle((560, 270, 740, 330), radius=10, fill=(0, 230, 160, 255))

        grid_x = [240, 430, 620]
        grid_y = [430, 550, 670]
        btn_w, btn_h = 140, 90

        for i, x in enumerate(grid_x):
            for j, y in enumerate(grid_y):
                color = (255, 255, 255, 230) if (i==2 or j==2) else (255, 255, 255, 170)
                if i == 2 and j == 2:
                    color = (255, 180, 40, 255)
                cdraw.rounded_rectangle((x, y, x + btn_w, y + btn_h), radius=20, fill=color)

        calc = add_drop_shadow(calc, offset=(0, 12), blur=20)
        return Image.alpha_composite(img, calc)

    # --- 7. Security ---
    def make_security():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (20, 35, 75, 255), (10, 15, 40, 255))
        img = Image.alpha_composite(img, bg)

        sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(sh)

        shield_pts = [(512, 200), (740, 270), (700, 620), (512, 800), (324, 620), (284, 270)]
        sdraw.polygon(shield_pts, fill=(0, 200, 150, 255))

        shield_pts_inner = [(512, 240), (700, 300), (665, 600), (512, 750), (359, 600), (324, 300)]
        sdraw.polygon(shield_pts_inner, fill=(5, 160, 120, 255))

        chk_pts = [(420, 500), (480, 570), (610, 420)]
        sdraw.line(chk_pts, fill=(255, 255, 255, 255), width=32, joint="round")

        sh = add_drop_shadow(sh, offset=(0, 15), blur=25)
        return Image.alpha_composite(img, sh)

    # --- 8. Terminal ---
    def make_terminal():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (25, 28, 36, 255), (12, 14, 18, 255))
        img = Image.alpha_composite(img, bg)

        term = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(term)

        tdraw.rounded_rectangle((200, 220, 824, 800), radius=30, fill=(38, 42, 54, 255), outline=(70, 75, 90, 255), width=6)
        tdraw.ellipse((240, 250, 264, 274), fill=(255, 95, 86, 255))
        tdraw.ellipse((280, 250, 304, 274), fill=(255, 189, 46, 255))
        tdraw.ellipse((320, 250, 344, 274), fill=(39, 201, 63, 255))

        prompt_pts = [(260, 350), (320, 400), (260, 450)]
        tdraw.line(prompt_pts, fill=(0, 230, 140, 255), width=20, joint="round")
        tdraw.line((350, 450, 410, 450), fill=(0, 230, 140, 255), width=20)

        tdraw.rounded_rectangle((260, 520, 500, 540), radius=8, fill=(130, 140, 160, 200))
        tdraw.rounded_rectangle((260, 580, 640, 600), radius=8, fill=(130, 140, 160, 200))
        tdraw.rounded_rectangle((260, 640, 420, 660), radius=8, fill=(130, 140, 160, 200))

        term = add_drop_shadow(term, offset=(0, 15), blur=25)
        return Image.alpha_composite(img, term)

    # --- 9. Task Manager ---
    def make_task_manager():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (20, 80, 120, 255), (10, 40, 70, 255))
        img = Image.alpha_composite(img, bg)

        tm = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(tm)

        for y in range(260, 780, 100):
            tdraw.line((220, y, 804, y), fill=(255, 255, 255, 30), width=4)
        for x in range(220, 804, 116):
            tdraw.line((x, 260, x, 760), fill=(255, 255, 255, 30), width=4)

        pts = [(220, 600), (320, 600), (400, 360), (480, 680), (560, 480), (660, 320), (804, 520)]
        tdraw.line(pts, fill=(0, 240, 255, 255), width=18, joint="round")

        for px, py in [(400, 360), (660, 320)]:
            tdraw.ellipse((px - 20, py - 20, px + 20, py + 20), fill=(255, 255, 255, 255), outline=(0, 240, 255, 255), width=6)

        tm = add_drop_shadow(tm, offset=(0, 12), blur=20)
        return Image.alpha_composite(img, tm)

    # --- 10. Photo Viewer ---
    def make_photo_viewer():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (230, 80, 100, 255), (120, 20, 90, 255))
        img = Image.alpha_composite(img, bg)

        pv = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(pv)

        pdraw.ellipse((580, 260, 720, 400), fill=(255, 215, 80, 255))

        m1 = [(200, 760), (440, 460), (640, 760)]
        pdraw.polygon(m1, fill=(160, 50, 110, 230))

        m2 = [(340, 760), (580, 380), (820, 760)]
        pdraw.polygon(m2, fill=(255, 240, 245, 240))

        snow = [(580, 380), (530, 450), (560, 470), (580, 460), (610, 475), (630, 450)]
        pdraw.polygon(snow, fill=(255, 255, 255, 255))

        pv = add_drop_shadow(pv, offset=(0, 15), blur=25)
        return Image.alpha_composite(img, pv)

    # --- 11. Timeline Explorer ---
    def make_timeline_explorer():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (90, 24, 154, 255), (15, 12, 41, 255))
        img = Image.alpha_composite(img, bg)

        c1 = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        draw1 = ImageDraw.Draw(c1)
        draw1.rounded_rectangle((260, 250, 680, 510), radius=28, fill=(255, 255, 255, 50), outline=(255, 255, 255, 90), width=4)
        draw1.rounded_rectangle((280, 270, 380, 282), radius=6, fill=(255, 255, 255, 120))
        draw1.ellipse((630, 270, 642, 282), fill=(255, 255, 255, 120))
        c1 = add_drop_shadow(c1, offset=(-20, -10), blur=20, shadow_color=(0, 0, 0, 70))
        img = Image.alpha_composite(img, c1)

        c2 = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        draw2 = ImageDraw.Draw(c2)
        draw2.rounded_rectangle((320, 330, 740, 590), radius=28, fill=(255, 255, 255, 100), outline=(255, 255, 255, 140), width=4)
        draw2.rounded_rectangle((340, 350, 460, 362), radius=6, fill=(0, 230, 255, 180))
        draw2.rectangle((340, 390, 480, 470), fill=(255, 255, 255, 80))
        draw2.rectangle((510, 390, 650, 470), fill=(255, 255, 255, 80))
        c2 = add_drop_shadow(c2, offset=(-10, 5), blur=20, shadow_color=(0, 0, 0, 80))
        img = Image.alpha_composite(img, c2)

        c3 = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        draw3 = ImageDraw.Draw(c3)
        draw3.rounded_rectangle((380, 410, 800, 670), radius=28, fill=(20, 25, 45, 235), outline=(0, 225, 255, 220), width=6)
        draw3.rounded_rectangle((380, 410, 800, 455), radius=28, fill=(35, 45, 75, 255))
        draw3.ellipse((405, 427, 420, 442), fill=(255, 90, 90, 255))
        draw3.ellipse((430, 427, 445, 442), fill=(255, 200, 80, 255))
        draw3.ellipse((455, 427, 470, 442), fill=(80, 220, 120, 255))
        draw3.rounded_rectangle((410, 480, 580, 630), radius=16, fill=(0, 150, 255, 200))
        draw3.rounded_rectangle((600, 480, 770, 560), radius=16, fill=(180, 70, 240, 200))
        draw3.rounded_rectangle((600, 580, 770, 630), radius=12, fill=(0, 230, 180, 200))
        c3 = add_drop_shadow(c3, offset=(0, 20), blur=30, shadow_color=(0, 0, 0, 110))
        img = Image.alpha_composite(img, c3)

        tl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        tldraw = ImageDraw.Draw(tl)
        tldraw.rounded_rectangle((220, 740, 804, 756), radius=8, fill=(0, 230, 255, 255))

        nodes_x = [280, 420, 560, 700]
        for idx, nx in enumerate(nodes_x):
            if idx == 2:
                tldraw.ellipse((nx - 24, 748 - 24, nx + 24, 748 + 24), fill=(255, 255, 255, 255), outline=(0, 230, 255, 255), width=8)
                tldraw.ellipse((nx - 12, 748 - 12, nx + 12, 748 + 12), fill=(0, 210, 255, 255))
            else:
                tldraw.ellipse((nx - 16, 748 - 16, nx + 16, 748 + 16), fill=(255, 255, 255, 220), outline=(100, 110, 150, 200), width=4)

        badge = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(badge)
        bcx, bcy = 710, 290
        br = 110
        bdraw.ellipse((bcx - br, bcy - br, bcx + br, bcy + br), fill=(0, 225, 255, 245), outline=(255, 255, 255, 255), width=8)

        bdraw.arc((bcx - 70, bcy - 70, bcx + 70, bcy + 70), start=40, end=320, fill=(20, 25, 50, 255), width=18)
        arrow_head = [(bcx - 15, bcy - 85), (bcx + 25, bcy - 70), (bcx - 5, bcy - 40)]
        bdraw.polygon(arrow_head, fill=(20, 25, 50, 255))
        bdraw.line((bcx, bcy, bcx, bcy - 40), fill=(20, 25, 50, 255), width=14)
        bdraw.line((bcx, bcy, bcx - 30, bcy), fill=(20, 25, 50, 255), width=14)
        bdraw.ellipse((bcx - 12, bcy - 12, bcx + 12, bcy + 12), fill=(20, 25, 50, 255))

        badge = add_drop_shadow(badge, offset=(0, 15), blur=25, shadow_color=(0, 0, 0, 90))
        tl = add_drop_shadow(tl, offset=(0, 10), blur=20, shadow_color=(0, 0, 0, 80))

        img = Image.alpha_composite(img, tl)
        img = Image.alpha_composite(img, badge)
        return img

    # --- 12. DiscoMode ---
    def make_discomode():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (255, 0, 128, 255), (70, 0, 150, 255))
        img = Image.alpha_composite(img, bg)

        disco = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(disco)
        cx, cy = S // 2, 420
        r = 210

        ddraw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(240, 240, 255, 255), outline=(255, 255, 255, 255), width=8)

        for i in range(-r + 30, r - 20, 45):
            h = int(math.sqrt(max(0, r*r - i*i)))
            ddraw.line((cx + i, cy - h, cx + i, cy + h), fill=(180, 200, 240, 180), width=6)
        for j in range(-r + 30, r - 20, 45):
            w = int(math.sqrt(max(0, r*r - j*j)))
            ddraw.line((cx - w, cy + j, cx + w, cy + j), fill=(180, 200, 240, 180), width=6)

        ddraw.line((cx, 128, cx, cy - r), fill=(255, 255, 255, 200), width=8)

        eq_colors = [(0, 240, 255), (255, 0, 200), (255, 230, 0), (0, 255, 120), (255, 100, 0)]
        bars_x = [240, 350, 460, 570, 680]
        bars_h = [180, 280, 360, 250, 190]
        for x, h, col in zip(bars_x, bars_h, eq_colors):
            ddraw.rounded_rectangle((x, 780 - h, x + 70, 780), radius=20, fill=col + (240,))

        disco = add_drop_shadow(disco, offset=(0, 15), blur=25)
        return Image.alpha_composite(img, disco)

    # --- 13. GameGetLink ---
    def make_gamegetlink():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (0, 180, 210, 255), (0, 70, 150, 255))
        img = Image.alpha_composite(img, bg)

        game = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(game)

        ctrl_box = (220, 360, 804, 700)
        gdraw.rounded_rectangle(ctrl_box, radius=120, fill=(245, 248, 255, 255), outline=(200, 220, 250, 255), width=8)

        gdraw.rounded_rectangle((320, 490, 420, 570), radius=15, fill=(40, 50, 70, 255))
        gdraw.rounded_rectangle((345, 465, 395, 595), radius=15, fill=(40, 50, 70, 255))

        btn_center = (700, 530)
        btn_offsets = [(0, -45, (255, 80, 80)), (45, 0, (80, 220, 120)), (-45, 0, (255, 200, 50)), (0, 45, (80, 140, 255))]
        for dx, dy, col in btn_offsets:
            bx, by = btn_center[0] + dx, btn_center[1] + dy
            gdraw.ellipse((bx - 18, by - 18, bx + 18, by + 18), fill=col + (255,))

        badge = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(badge)
        bdraw.ellipse((420, 190, 600, 370), fill=(255, 180, 0, 255), outline=(255, 255, 255, 255), width=8)
        bdraw.rectangle((490, 230, 530, 300), fill=(255, 255, 255, 255))
        bdraw.polygon([(460, 290), (560, 290), (510, 340)], fill=(255, 255, 255, 255))

        badge = add_drop_shadow(badge, offset=(0, 12), blur=20)
        game = add_drop_shadow(game, offset=(0, 15), blur=25)

        img = Image.alpha_composite(img, game)
        img = Image.alpha_composite(img, badge)
        return img

    # --- 14. LinkMyDevice ---
    def make_linkmydevice():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (20, 140, 255, 255), (10, 60, 180, 255))
        img = Image.alpha_composite(img, bg)

        dev = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(dev)

        ddraw.line((320, 360, 700, 360), fill=(0, 240, 255, 220), width=12)
        ddraw.line((320, 360, 512, 680), fill=(0, 240, 255, 220), width=12)
        ddraw.line((700, 360, 512, 680), fill=(0, 240, 255, 220), width=12)

        ddraw.rounded_rectangle((220, 260, 420, 390), radius=16, fill=(240, 245, 255, 255), outline=(0, 200, 255, 255), width=6)
        ddraw.rounded_rectangle((240, 280, 400, 360), radius=10, fill=(30, 40, 65, 255))
        ddraw.rounded_rectangle((190, 390, 450, 410), radius=8, fill=(200, 210, 230, 255))

        ddraw.rounded_rectangle((600, 240, 800, 380), radius=16, fill=(240, 245, 255, 255), outline=(0, 200, 255, 255), width=6)
        ddraw.rounded_rectangle((620, 260, 780, 360), radius=10, fill=(30, 40, 65, 255))
        ddraw.rectangle((685, 380, 715, 410), fill=(200, 210, 230, 255))
        ddraw.rounded_rectangle((650, 410, 750, 425), radius=6, fill=(200, 210, 230, 255))

        ddraw.rounded_rectangle((450, 580, 570, 780), radius=22, fill=(240, 245, 255, 255), outline=(0, 200, 255, 255), width=6)
        ddraw.rounded_rectangle((465, 600, 555, 750), radius=14, fill=(30, 40, 65, 255))
        ddraw.ellipse((502, 756, 518, 772), fill=(180, 190, 210, 255))

        badge = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(badge)
        bdraw.ellipse((442, 402, 582, 542), fill=(0, 230, 255, 255), outline=(255, 255, 255, 255), width=8)
        bdraw.arc((472, 432, 552, 512), start=30, end=170, fill=(15, 30, 70, 255), width=12)
        bdraw.arc((472, 432, 552, 512), start=210, end=350, fill=(15, 30, 70, 255), width=12)

        dev = add_drop_shadow(dev, offset=(0, 15), blur=25)
        badge = add_drop_shadow(badge, offset=(0, 10), blur=20)

        img = Image.alpha_composite(img, dev)
        img = Image.alpha_composite(img, badge)
        return img

    # --- 15. Find This ID/IP ---
    def make_find_this_id_ip():
        img = get_canvas()
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (15, 23, 42, 255), (30, 41, 59, 255))
        img = Image.alpha_composite(img, bg)

        net = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ndraw = ImageDraw.Draw(net)

        cx, cy = S // 2 - 40, S // 2 - 40

        ndraw.ellipse((cx - 260, cy - 260, cx + 260, cy + 260), outline=(0, 230, 160, 80), width=6)
        ndraw.ellipse((cx - 180, cy - 180, cx + 180, cy + 180), outline=(0, 230, 160, 140), width=6)
        ndraw.ellipse((cx - 100, cy - 100, cx + 100, cy + 100), outline=(0, 230, 160, 200), width=6)

        ndraw.line((cx - 280, cy, cx + 280, cy), fill=(0, 230, 160, 100), width=4)
        ndraw.line((cx, cy - 280, cx, cy + 280), fill=(0, 230, 160, 100), width=4)

        targets = [(cx - 120, cy - 80), (cx + 140, cy - 120), (cx + 80, cy + 130)]
        for tx, ty in targets:
            ndraw.ellipse((tx - 16, ty - 16, tx + 16, ty + 16), fill=(0, 255, 180, 255))

        mag = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        mdraw = ImageDraw.Draw(mag)

        mcx, mcy = S // 2 + 30, S // 2 + 30
        mr = 170
        mdraw.ellipse((mcx - mr, mcy - mr, mcx + mr, mcy + mr), outline=(0, 240, 255, 255), width=24)
        mdraw.ellipse((mcx - mr + 12, mcy - mr + 12, mcx + mr - 12, mcy + mr - 12), fill=(0, 180, 255, 40))

        handle_pts = [(mcx + 120, mcy + 120), (mcx + 260, mcy + 260)]
        mdraw.line(handle_pts, fill=(0, 240, 255, 255), width=36)

        # IP address digital segments representation inside magnifying lens
        # Draw "IP" text style graphic or IP node segments
        ip_badge_box = (mcx - 110, mcy - 40, mcx + 110, mcy + 40)
        mdraw.rounded_rectangle(ip_badge_box, radius=16, fill=(0, 230, 160, 255))
        # Draw "IP" letters in badge
        # 'I'
        mdraw.line((mcx - 70, mcy - 20, mcx - 70, mcy + 20), fill=(15, 23, 42, 255), width=10)
        # 'P'
        mdraw.line((mcx - 30, mcy - 20, mcx - 30, mcy + 20), fill=(15, 23, 42, 255), width=10)
        mdraw.rounded_rectangle((mcx - 30, mcy - 20, mcx + 10, mcy), radius=6, outline=(15, 23, 42, 255), width=10)
        # Dots '. . .'
        for dx in [35, 55, 75]:
            mdraw.ellipse((mcx + dx - 4, mcy + 12, mcx + dx + 4, mcy + 20), fill=(15, 23, 42, 255))

        net = add_drop_shadow(net, offset=(0, 10), blur=20)
        mag = add_drop_shadow(mag, offset=(0, 20), blur=30)

        img = Image.alpha_composite(img, net)
        img = Image.alpha_composite(img, mag)
        return img

    apps = {
        "text_editor": make_text_editor,
        "settings": make_settings,
        "file_explorer": make_file_explorer,
        "media_player": make_media_player,
        "web_browser": make_web_browser,
        "calculator": make_calculator,
        "security": make_security,
        "terminal": make_terminal,
        "task_manager": make_task_manager,
        "photo_viewer": make_photo_viewer,
        "timeline_explorer": make_timeline_explorer,
        "discomode": make_discomode,
        "gamegetlink": make_gamegetlink,
        "linkmydevice": make_linkmydevice,
        "find_this_id_ip": make_find_this_id_ip,
    }

    sizes_ico = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    for name, gen_fn in apps.items():
        print(f"Generating icon for {name}...")
        img1024 = gen_fn()
        img512 = img1024.resize((512, 512), resample=Image.Resampling.LANCZOS)

        png_path = os.path.join(output_dir, f"{name}.png")
        ico_path = os.path.join(output_dir, f"{name}.ico")

        img512.save(png_path, format="PNG")
        img512.save(ico_path, format="ICO", sizes=sizes_ico)
        print(f"Saved {png_path} and {ico_path}")

if __name__ == "__main__":
    create_icons()
