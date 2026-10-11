import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_icons():
    output_dir = "icons"
    os.makedirs(output_dir, exist_ok=True)

    # We draw at 1024x1024 for supersampling anti-aliasing
    S = 1024

    def get_canvas():
        return Image.new("RGBA", (S, S), (0, 0, 0, 0))

    def draw_rounded_rect(draw, box, radius, fill, outline=None, width=1):
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

    def draw_linear_gradient_rounded_rect(size, box, radius, color_top, color_bottom):
        # Create gradient image
        grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        for y in range(box[1], box[3]):
            factor = (y - box[1]) / float(max(1, box[3] - box[1]))
            r = int(color_top[0] + factor * (color_bottom[0] - color_top[0]))
            g = int(color_top[1] + factor * (color_bottom[1] - color_top[1]))
            b = int(color_top[2] + factor * (color_bottom[2] - color_top[2]))
            a = int(color_top[3] + factor * (color_bottom[3] - color_top[3])) if len(color_top)>3 and len(color_bottom)>3 else 255

            # draw line
            line_img = Image.new("RGBA", (size, 1), (r, g, b, a))
            grad.paste(line_img, (0, y))

        mask = Image.new("L", (size, size), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle(box, radius=radius, fill=255)

        result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        result.paste(grad, (0, 0), mask)
        return result

    def add_drop_shadow(base_img, offset=(0, 20), blur=30, shadow_color=(0, 0, 0, 80)):
        # Extract alpha as shadow base
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
        # Card background
        bg = draw_linear_gradient_rounded_rect(S, (128, 128, 896, 896), 160, (24, 119, 242, 255), (10, 60, 160, 255))
        img = Image.alpha_composite(img, bg)

        # Document sheet
        doc = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(doc)
        doc_box = (320, 240, 704, 780)
        ddraw.rounded_rectangle(doc_box, radius=40, fill=(255, 255, 255, 245))

        # Page lines
        lines_y = [360, 430, 500, 570, 640]
        widths = [280, 320, 240, 300, 180]
        for y, w in zip(lines_y, widths):
            ddraw.rounded_rectangle((360, y, 360 + w, y + 24), radius=12, fill=(0, 102, 204, 200))

        # Folded corner effect or top ribbon bar
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

        import math
        cx, cy = S // 2, S // 2
        r_outer = 260
        r_inner = 180
        num_teeth = 8

        # Draw teeth
        for i in range(num_teeth):
            angle = i * (2 * math.pi / num_teeth)
            dx = math.cos(angle)
            dy = math.sin(angle)
            tx = cx + dx * 320
            ty = cy + dy * 320
            gdraw.line((cx, cy, tx, ty), fill=(220, 225, 230, 255), width=90)

        # Draw outer body
        gdraw.ellipse((cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer), fill=(220, 225, 230, 255))
        # Draw inner hole
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

        # Back tab
        fdraw.rounded_rectangle((240, 280, 500, 400), radius=30, fill=(230, 160, 30, 255))
        # Main folder body
        fdraw.rounded_rectangle((240, 340, 780, 740), radius=40, fill=(255, 195, 45, 255))

        # Document sticking out
        doc = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(doc)
        ddraw.rounded_rectangle((320, 240, 700, 500), radius=25, fill=(245, 247, 250, 255))
        ddraw.rounded_rectangle((360, 290, 520, 310), radius=10, fill=(0, 120, 215, 255))
        ddraw.rounded_rectangle((360, 330, 620, 345), radius=8, fill=(180, 190, 200, 255))
        ddraw.rounded_rectangle((360, 365, 580, 380), radius=8, fill=(180, 190, 200, 255))

        # Front flap
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

        # Glowing circle ring
        cx, cy = S // 2, S // 2
        odraw.ellipse((cx - 240, cy - 240, cx + 240, cy + 240), outline=(255, 255, 255, 120), width=16)

        # Play triangle
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

        # Latitude lines
        gdraw.ellipse((cx - r, cy - 100, cx + r, cy + 100), outline=(255, 255, 255, 160), width=12)
        gdraw.line((cx - r, cy, cx + r, cy), fill=(255, 255, 255, 200), width=14)

        # Longitude lines
        gdraw.ellipse((cx - 110, cy - r, cx + 110, cy + r), outline=(255, 255, 255, 160), width=12)
        gdraw.line((cx, cy - r, cx, cy + r), fill=(255, 255, 255, 200), width=14)

        # Orbiting cursor arrow
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

        # Display Screen
        cdraw.rounded_rectangle((240, 220, 780, 380), radius=25, fill=(20, 35, 30, 220), outline=(255, 255, 255, 80), width=6)
        # Display numbers line
        cdraw.rounded_rectangle((560, 270, 740, 330), radius=10, fill=(0, 230, 160, 255))

        # Keypad buttons (3x3 grid)
        grid_x = [240, 430, 620]
        grid_y = [430, 550, 670]
        btn_w, btn_h = 140, 90

        for i, x in enumerate(grid_x):
            for j, y in enumerate(grid_y):
                color = (255, 255, 255, 230) if (i==2 or j==2) else (255, 255, 255, 170)
                if i == 2 and j == 2:
                    color = (255, 180, 40, 255) # Accent '=' key
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

        # Shield shape polygon / curves
        shield_pts = [(512, 200), (740, 270), (700, 620), (512, 800), (324, 620), (284, 270)]
        sdraw.polygon(shield_pts, fill=(0, 200, 150, 255))

        # Inner shield detail
        shield_pts_inner = [(512, 240), (700, 300), (665, 600), (512, 750), (359, 600), (324, 300)]
        sdraw.polygon(shield_pts_inner, fill=(5, 160, 120, 255))

        # Glowing Checkmark
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

        # Window frame inside
        tdraw.rounded_rectangle((200, 220, 824, 800), radius=30, fill=(38, 42, 54, 255), outline=(70, 75, 90, 255), width=6)
        # Header window dots
        tdraw.ellipse((240, 250, 264, 274), fill=(255, 95, 86, 255))
        tdraw.ellipse((280, 250, 304, 274), fill=(255, 189, 46, 255))
        tdraw.ellipse((320, 250, 344, 274), fill=(39, 201, 63, 255))

        # Prompt '>'
        prompt_pts = [(260, 350), (320, 400), (260, 450)]
        tdraw.line(prompt_pts, fill=(0, 230, 140, 255), width=20, joint="round")

        # Cursor '_'
        tdraw.line((350, 450, 410, 450), fill=(0, 230, 140, 255), width=20)

        # Code lines
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

        # Grid lines background
        for y in range(260, 780, 100):
            tdraw.line((220, y, 804, y), fill=(255, 255, 255, 30), width=4)
        for x in range(220, 804, 116):
            tdraw.line((x, 260, x, 760), fill=(255, 255, 255, 30), width=4)

        # Chart Line
        pts = [(220, 600), (320, 600), (400, 360), (480, 680), (560, 480), (660, 320), (804, 520)]
        tdraw.line(pts, fill=(0, 240, 255, 255), width=18, joint="round")

        # Glowing dots on peaks
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

        # Sun
        pdraw.ellipse((580, 260, 720, 400), fill=(255, 215, 80, 255))

        # Back mountain
        m1 = [(200, 760), (440, 460), (640, 760)]
        pdraw.polygon(m1, fill=(160, 50, 110, 230))

        # Front mountain
        m2 = [(340, 760), (580, 380), (820, 760)]
        pdraw.polygon(m2, fill=(255, 240, 245, 240))

        # Peak snow cap
        snow = [(580, 380), (530, 450), (560, 470), (580, 460), (610, 475), (630, 450)]
        pdraw.polygon(snow, fill=(255, 255, 255, 255))

        pv = add_drop_shadow(pv, offset=(0, 15), blur=25)
        return Image.alpha_composite(img, pv)

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
    }

    sizes_ico = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    for name, gen_fn in apps.items():
        print(f"Generating icon for {name}...")
        img1024 = gen_fn()
        # Downsample to 512x512 with LANCZOS for high quality anti-aliasing
        img512 = img1024.resize((512, 512), resample=Image.Resampling.LANCZOS)

        png_path = os.path.join(output_dir, f"{name}.png")
        ico_path = os.path.join(output_dir, f"{name}.ico")

        img512.save(png_path, format="PNG")
        img512.save(ico_path, format="ICO", sizes=sizes_ico)
        print(f"Saved {png_path} and {ico_path}")

if __name__ == "__main__":
    create_icons()
