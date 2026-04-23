"""
KayEcomElite Portfolio Image Generator
Run this script to create placeholder images for your portfolio.
Requires: Python 3.x with PIL (Pillow) installed.
Install Pillow: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random


def ensure_dir(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def get_font(size, bold=False):
    """Try to load a nice font, fallback to default."""
    font_names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Windows/Fonts/arial.ttf",
        "/Windows/Fonts/arialbd.ttf" if bold else "/Windows/Fonts/arial.ttf",
    ]
    for name in font_names:
        if os.path.exists(name):
            try:
                return ImageFont.truetype(name, size)
            except:
                pass
    return ImageFont.load_default()


def create_gradient(width, height, color1, color2, direction="vertical"):
    """Create a smooth gradient background."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for i in range(height if direction == "vertical" else width):
        ratio = i / (height if direction == "vertical" else width)
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        if direction == "vertical":
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, height)], fill=(r, g, b))
    
    return img


def add_noise(img, intensity=15):
    """Add subtle film grain noise for texture."""
    pixels = img.load()
    for i in range(0, img.width, 2):
        for j in range(0, img.height, 2):
            r, g, b = pixels[i, j]
            noise = random.randint(-intensity, intensity)
            pixels[i, j] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise))
            )
    return img


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Draw a rectangle with rounded corners."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def create_hero_image():
    """Create hero-image.jpg - E-commerce analytics dashboard."""
    width, height = 1200, 800
    img = create_gradient(width, height, (10, 10, 12), (18, 16, 22), "diagonal")
    draw = ImageDraw.Draw(img)
    
    # Add subtle noise texture
    img = add_noise(img, 8)
    draw = ImageDraw.Draw(img)
    
    # Dashboard frame
    frame_padding = 60
    draw_rounded_rect(draw, 
        [frame_padding, frame_padding, width - frame_padding, height - frame_padding],
        radius=12, fill=(14, 14, 18), outline=(40, 38, 45), width=1)
    
    # Header bar
    header_h = 80
    draw_rounded_rect(draw,
        [frame_padding, frame_padding, width - frame_padding, frame_padding + header_h],
        radius=12, fill=(18, 18, 24))
    
    # Window dots
    dot_colors = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]
    for i, color in enumerate(dot_colors):
        x = frame_padding + 30 + i * 28
        y = frame_padding + 32
        draw.ellipse([x-6, y-6, x+6, y+6], fill=color)
    
    # Title
    font_title = get_font(22, bold=True)
    draw.text((frame_padding + 140, frame_padding + 22), 
              "Revenue Analytics Dashboard", fill=(200, 200, 210), font=font_title)
    
    # Sidebar
    sidebar_w = 200
    draw.rectangle([frame_padding, frame_padding + header_h, 
                    frame_padding + sidebar_w, height - frame_padding],
                   fill=(12, 12, 16))
    
    # Sidebar items
    font_nav = get_font(13)
    nav_items = ["Overview", "Orders", "Products", "Customers", "Reports", "Settings"]
    for i, item in enumerate(nav_items):
        y = frame_padding + header_h + 40 + i * 50
        if i == 0:
            draw_rounded_rect(draw, [frame_padding + 20, y - 10, 
                           frame_padding + sidebar_w - 20, y + 30], 
                           radius=6, fill=(212, 175, 119, 30))
            draw.text((frame_padding + 35, y), item, fill=(212, 175, 119), font=font_nav)
        else:
            draw.text((frame_padding + 35, y), item, fill=(100, 100, 110), font=font_nav)
    
    # Main content area
    main_x = frame_padding + sidebar_w + 40
    main_y = frame_padding + header_h + 40
    
    # KPI Cards
    kpis = [("$847,293", "Total Revenue", "+24.5%"), 
            ("3.8%", "Conversion Rate", "+217%"),
            ("$128", "AOV", "+18.2%"),
            ("12.4K", "Orders", "+32.1%")]
    
    card_w = 210
    card_h = 120
    card_gap = 20
    
    for i, (value, label, change) in enumerate(kpis):
        x = main_x + i * (card_w + card_gap)
        y = main_y
        
        # Card bg
        draw_rounded_rect(draw, [x, y, x + card_w, y + card_h], 
                         radius=8, fill=(18, 18, 24), outline=(35, 35, 42), width=1)
        
        # Value
        font_val = get_font(26, bold=True)
        draw.text((x + 20, y + 20), value, fill=(240, 240, 245), font=font_val)
        
        # Label
        font_lbl = get_font(12)
        draw.text((x + 20, y + 58), label, fill=(120, 120, 130), font=font_lbl)
        
        # Change badge
        badge_color = (61, 220, 132) if "+" in change else (255, 69, 58)
        draw_rounded_rect(draw, [x + 20, y + 82, x + 80, y + 102], 
                         radius=4, fill=(badge_color[0]//4, badge_color[1]//4, badge_color[2]//4))
        font_chg = get_font(11, bold=True)
        draw.text((x + 28, y + 84), change, fill=badge_color, font=font_chg)
    
    # Chart area
    chart_y = main_y + card_h + 40
    chart_h = 280
    chart_w = (card_w + card_gap) * 4 - card_gap
    
    draw_rounded_rect(draw, [main_x, chart_y, main_x + chart_w, chart_y + chart_h],
                     radius=8, fill=(18, 18, 24), outline=(35, 35, 42), width=1)
    
    # Chart title
    font_chart = get_font(16, bold=True)
    draw.text((main_x + 25, chart_y + 20), "Revenue Growth", fill=(200, 200, 210), font=font_chart)
    
    # Draw line chart
    points = []
    for i in range(12):
        x = main_x + 60 + i * ((chart_w - 120) / 11)
        # Upward trend with some variation
        base = 0.3 + (i / 11) * 0.6
        variation = random.uniform(-0.05, 0.05)
        y = chart_y + chart_h - 60 - (base + variation) * (chart_h - 100)
        points.append((x, y))
    
    # Draw area under line
    if len(points) > 1:
        area_points = [(points[0][0], chart_y + chart_h - 40)] + points + [(points[-1][0], chart_y + chart_h - 40)]
        draw.polygon(area_points, fill=(212, 175, 119, 20))
    
    # Draw line
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(212, 175, 119), width=3)
    
    # Draw points
    for x, y in points:
        draw.ellipse([x-5, y-5, x+5, y+5], fill=(212, 175, 119), outline=(18, 18, 24), width=2)
    
    # X-axis labels
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    font_month = get_font(10)
    for i, month in enumerate(months):
        x = main_x + 60 + i * ((chart_w - 120) / 11)
        draw.text((x - 12, chart_y + chart_h - 32), month, fill=(100, 100, 110), font=font_month)
    
    # Right side mini chart
    mini_x = main_x + chart_w + 20
    draw_rounded_rect(draw, [mini_x, chart_y, mini_x + 200, chart_y + chart_h],
                     radius=8, fill=(18, 18, 24), outline=(35, 35, 42), width=1)
    
    font_mini = get_font(14, bold=True)
    draw.text((mini_x + 20, chart_y + 20), "Traffic Sources", fill=(200, 200, 210), font=font_mini)
    
    # Pie chart representation (simplified as bars)
    sources = [("Organic", 45, (212, 175, 119)), 
               ("Paid", 30, (100, 149, 237)),
               ("Social", 15, (61, 220, 132)),
               ("Direct", 10, (155, 89, 182))]
    
    bar_y = chart_y + 60
    for label, pct, color in sources:
        bar_w = int(160 * (pct / 100))
        draw_rounded_rect(draw, [mini_x + 20, bar_y, mini_x + 20 + bar_w, bar_y + 16],
                         radius=3, fill=color)
        font_src = get_font(10)
        draw.text((mini_x + 20, bar_y + 22), f"{label} {pct}%", fill=(140, 140, 150), font=font_src)
        bar_y += 50
    
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    return img


def create_before_image():
    """Create before.jpg - Cluttered, low-performing store."""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), (245, 245, 247))
    draw = ImageDraw.Draw(img)
    
    # Messy header
    draw.rectangle([0, 0, width, 80], fill=(255, 255, 255))
    draw.rectangle([0, 78, width, 80], fill=(220, 220, 220))
    
    # Scattered navigation
    font_nav = get_font(14)
    nav_items = ["HOME", "Shop", "About", "Contact", "Blog", "FAQ"]
    x_pos = 30
    for item in nav_items:
        color = (80, 80, 80) if item != "HOME" else (50, 50, 50)
        draw.text((x_pos, 30), item, fill=color, font=font_nav)
        x_pos += random.randint(70, 110)
    
    # Cluttered hero banner
    draw.rectangle([0, 80, width, 300], fill=(240, 240, 240))
    font_hero = get_font(32, bold=True)
    draw.text((50, 130), "WELCOME TO OUR STORE!!!", fill=(80, 80, 80), font=font_hero)
    font_sub = get_font(16)
    draw.text((50, 180), "We have the best products at the best prices.", fill=(150, 150, 150), font=font_sub)
    
    # Multiple conflicting CTAs
    draw.rectangle([50, 220, 200, 260], fill=(255, 100, 100))
    font_cta = get_font(12, bold=True)
    draw.text((70, 232), "BUY NOW!!!", fill=(255, 255, 255), font=font_cta)
    
    draw.rectangle([220, 220, 380, 260], fill=(100, 100, 255))
    draw.text((240, 232), "CLICK HERE", fill=(255, 255, 255), font=font_cta)
    
    # Cluttered product grid
    products = [
        ("Product 1", "$49.99", "$29.99"),
        ("Item Two", "$89.99", "$59.99"),
        ("Thing 3", "$129.99", "$99.99"),
        ("Stuff Four", "$39.99", "$19.99"),
    ]
    
    y_start = 340
    for row in range(2):
        for col in range(2):
            idx = row * 2 + col
            if idx >= len(products):
                break
            x = 40 + col * 280
            y = y_start + row * 220
            
            # Product card (messy)
            draw.rectangle([x, y, x + 260, y + 200], fill=(255, 255, 255), outline=(200, 200, 200))
            
            # Placeholder image area
            draw.rectangle([x + 10, y + 10, x + 250, y + 120], fill=(230, 230, 230))
            
            name, old, new = products[idx]
            font_name = get_font(14)
            draw.text((x + 10, y + 130), name, fill=(60, 60, 60), font=font_name)
            
            font_old = get_font(12)
            draw.text((x + 10, y + 155), old, fill=(180, 180, 180), font=font_old)
            
            font_new = get_font(16, bold=True)
            draw.text((x + 60, y + 153), new, fill=(255, 80, 80), font=font_new)
            
            # Messy badge
            draw.rectangle([x + 180, y + 10, x + 250, y + 40], fill=(255, 200, 0))
            font_badge = get_font(10, bold=True)
            draw.text((x + 188, y + 16), "SALE!!", fill=(0, 0, 0), font=font_badge)
    
    # Chaotic footer
    draw.rectangle([0, height - 100, width, height], fill=(60, 60, 60))
    font_foot = get_font(11)
    draw.text((30, height - 70), "Copyright 2024 | Terms | Privacy | Shipping | Returns | FAQ | Blog | Contact Us", 
              fill=(180, 180, 180), font=font_foot)
    
    # Add slight blur to simulate low quality
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return img


def create_after_image():
    """Create after.jpg - Clean, high-converting optimized store."""
    width, height = 1200, 800
    img = create_gradient(width, height, (10, 10, 12), (14, 14, 18), "vertical")
    draw = ImageDraw.Draw(img)
    
    # Clean dark header
    draw.rectangle([0, 0, width, 70], fill=(10, 10, 12))
    
    # Minimal navigation
    font_nav = get_font(13)
    nav_items = [("Shop", 100), ("Collections", 200), ("About", 340), ("Journal", 460)]
    for label, x in nav_items:
        draw.text((x, 26), label, fill=(160, 160, 170), font=font_nav)
    
    # Logo area
    font_logo = get_font(20, bold=True)
    draw.text((40, 22), "LUXE", fill=(240, 240, 245), font=font_logo)
    
    # Clean hero
    hero_y = 70
    draw.rectangle([0, hero_y, width, hero_y + 350], fill=(12, 12, 16))
    
    # Elegant headline
    font_head = get_font(42, bold=True)
    draw.text((80, hero_y + 80), "Curated Essentials", fill=(240, 240, 245), font=font_head)
    
    font_sub = get_font(18)
    draw.text((80, hero_y + 150), "Thoughtfully designed pieces for modern living.", 
              fill=(140, 140, 150), font=font_sub)
    
    # Single strong CTA
    draw_rounded_rect(draw, [80, hero_y + 210, 260, hero_y + 260], 
                     radius=4, fill=(212, 175, 119))
    font_cta = get_font(13, bold=True)
    draw.text((120, hero_y + 225), "Explore Collection", fill=(10, 10, 12), font=font_cta)
    
    # Clean product grid
    products = [
        ("The Meridian Chair", "$489"),
        ("Oak Dining Table", "$1,299"),
        ("Ceramic Vessel Set", "$189"),
        ("Linen Throw", "$129"),
    ]
    
    y_start = hero_y + 380
    for i, (name, price) in enumerate(products):
        x = 80 + i * 270
        
        # Clean card
        draw_rounded_rect(draw, [x, y_start, x + 250, y_start + 280],
                         radius=6, fill=(16, 16, 20), outline=(30, 30, 36), width=1)
        
        # Image placeholder with subtle gradient
        card_img = create_gradient(250, 180, (35, 35, 42), (25, 25, 30), "diagonal")
        img.paste(card_img, (x, y_start))
        
        # Product info
        font_name = get_font(14)
        draw.text((x + 20, y_start + 200), name, fill=(200, 200, 210), font=font_name)
        
        font_price = get_font(16, bold=True)
        draw.text((x + 20, y_start + 228), price, fill=(212, 175, 119), font=font_price)
        
        # Subtle trust indicator
        font_trust = get_font(10)
        draw.text((x + 20, y_start + 256), "Free shipping • In stock", 
                 fill=(100, 100, 110), font=font_trust)
    
    # Minimal footer
    draw.rectangle([0, height - 60, width, height], fill=(10, 10, 12))
    font_foot = get_font(11)
    draw.text((80, height - 38), "Minimal living, maximum quality.", fill=(100, 100, 110), font=font_foot)
    
    return img


def create_analytics_image():
    """Create analytics.jpg - Performance dashboard."""
    width, height = 1000, 700
    img = create_gradient(width, height, (10, 10, 12), (16, 14, 20), "diagonal")
    draw = ImageDraw.Draw(img)
    
    img = add_noise(img, 6)
    draw = ImageDraw.Draw(img)
    
    # Main frame
    padding = 50
    draw_rounded_rect(draw, [padding, padding, width - padding, height - padding],
                     radius=12, fill=(14, 14, 18), outline=(35, 35, 42), width=1)
    
    # Title
    font_title = get_font(24, bold=True)
    draw.text((padding + 40, padding + 30), "Performance Overview", 
             fill=(220, 220, 230), font=font_title)
    
    font_date = get_font(12)
    draw.text((padding + 40, padding + 65), "Last 30 Days", fill=(100, 100, 110), font=font_date)
    
    # Large metric
    font_big = get_font(56, bold=True)
    draw.text((padding + 40, padding + 110), "3.84%", fill=(212, 175, 119), font=font_big)
    
    font_label = get_font(14)
    draw.text((padding + 40, padding + 180), "Conversion Rate", fill=(140, 140, 150), font=font_label)
    
    # Trend indicator
    draw_rounded_rect(draw, [padding + 40, padding + 210, padding + 140, padding + 240],
                     radius=4, fill=(61, 220, 132, 30))
    font_trend = get_font(12, bold=True)
    draw.text((padding + 52, padding + 216), "+217%", fill=(61, 220, 132), font=font_trend)
    
    # Bar chart
    chart_x = padding + 40
    chart_y = padding + 280
    chart_w = width - padding * 2 - 80
    chart_h = 200
    
    bars = [35, 42, 38, 55, 48, 62, 58, 75, 82, 88, 95, 100]
    bar_w = (chart_w - 60) / len(bars)
    
    for i, h in enumerate(bars):
        x = chart_x + 30 + i * bar_w
        bar_height = (h / 100) * (chart_h - 40)
        
        # Gradient bar
        for y in range(int(chart_y + chart_h - 20 - bar_height), int(chart_y + chart_h - 20)):
            ratio = (y - (chart_y + chart_h - 20 - bar_height)) / bar_height if bar_height > 0 else 0
            r = int(212 * ratio + 100 * (1 - ratio))
            g = int(175 * ratio + 100 * (1 - ratio))
            b = int(119 * ratio + 120 * (1 - ratio))
            draw.line([(x, y), (x + bar_w - 8, y)], fill=(r, g, b))
        
        # Rounded top
        draw.ellipse([x, chart_y + chart_h - 20 - bar_height - 4, 
                     x + bar_w - 8, chart_y + chart_h - 20 - bar_height + 4],
                    fill=(212, 175, 119))
    
    # Line overlay
    line_points = []
    for i, h in enumerate(bars):
        x = chart_x + 30 + i * bar_w + (bar_w - 8) / 2
        y = chart_y + chart_h - 20 - (h / 100) * (chart_h - 40)
        line_points.append((x, y))
    
    for i in range(len(line_points) - 1):
        draw.line([line_points[i], line_points[i+1]], fill=(240, 240, 245), width=2)
    
    for x, y in line_points:
        draw.ellipse([x-4, y-4, x+4, y+4], fill=(240, 240, 245))
    
    # Right side metrics
    metric_x = width - padding - 280
    metrics = [
        ("Revenue", "$847,293", "+24.5%"),
        ("AOV", "$128", "+18.2%"),
        ("Orders", "12.4K", "+32.1%"),
        ("ROAS", "4.2x", "+45%"),
    ]
    
    my = padding + 40
    for label, value, change in metrics:
        draw.text((metric_x, my), label, fill=(120, 120, 130), font=font_label)
        
        font_val = get_font(22, bold=True)
        draw.text((metric_x, my + 25), value, fill=(240, 240, 245), font=font_val)
        
        chg_color = (61, 220, 132) if "+" in change else (255, 69, 58)
        font_chg = get_font(12, bold=True)
        draw.text((metric_x, my + 55), change, fill=chg_color, font=font_chg)
        
        my += 100
    
    return img


def create_about_image():
    """Create about.jpg - Minimal workspace aesthetic."""
    width, height = 800, 1000
    img = create_gradient(width, height, (15, 15, 18), (10, 10, 12), "vertical")
    draw = ImageDraw.Draw(img)
    
    img = add_noise(img, 5)
    draw = ImageDraw.Draw(img)
    
    # Desk surface
    desk_y = height * 0.6
    draw.rectangle([0, desk_y, width, height], fill=(22, 20, 18))
    
    # Laptop
    lap_x, lap_y = 200, desk_y - 80
    draw_rounded_rect(draw, [lap_x, lap_y, lap_x + 400, lap_y + 260],
                     radius=8, fill=(30, 30, 34), outline=(50, 50, 56), width=1)
    
    # Screen
    draw.rectangle([lap_x + 20, lap_y + 20, lap_x + 380, lap_y + 200], 
                  fill=(12, 12, 16))
    
    # Screen content (subtle chart)
    for i in range(8):
        x = lap_x + 40 + i * 40
        h = 20 + i * 15
        draw.rectangle([x, lap_y + 180 - h, x + 25, lap_y + 180], 
                      fill=(212, 175, 119, 40))
    
    # Coffee cup
    cup_x, cup_y = 650, desk_y - 60
    draw.ellipse([cup_x, cup_y, cup_x + 60, cup_y + 50], fill=(40, 38, 36))
    draw.ellipse([cup_x + 10, cup_y - 10, cup_x + 50, cup_y + 10], fill=(60, 40, 30))
    
    # Steam
    for i in range(3):
        sx = cup_x + 20 + i * 8
        draw.arc([sx, cup_y - 40 - i * 10, sx + 15, cup_y - 10], 
                start=180, end=0, fill=(200, 200, 200, 60), width=1)
    
    # Plant
    plant_x, plant_y = 80, desk_y - 120
    draw.rectangle([plant_x + 20, plant_y + 80, plant_x + 50, plant_y + 140], 
                  fill=(50, 60, 50))
    draw.ellipse([plant_x, plant_y, plant_x + 70, plant_y + 80], fill=(60, 80, 60))
    draw.ellipse([plant_x + 10, plant_y + 20, plant_x + 60, plant_y + 70], fill=(80, 110, 80))
    
    # Notebook
    note_x, note_y = 120, desk_y + 40
    draw_rounded_rect(draw, [note_x, note_y, note_x + 150, note_y + 200],
                     radius=4, fill=(35, 35, 38))
    draw.line([(note_x + 30, note_y + 20), (note_x + 30, note_y + 180)], 
             fill=(60, 60, 65), width=1)
    
    # Pen
    pen_x, pen_y = 300, desk_y + 100
    draw.rectangle([pen_x, pen_y, pen_x + 120, pen_y + 8], fill=(80, 80, 85))
    draw.polygon([(pen_x + 120, pen_y), (pen_x + 140, pen_y + 4), 
                 (pen_x + 120, pen_y + 8)], fill=(212, 175, 119))
    
    # Ambient light glow
    glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([width - 300, -100, width + 100, 300], 
                     fill=(212, 175, 119, 8))
    img = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
    
    return img


def create_logo():
    """Create logo.png - Simple brand mark."""
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Circle background
    draw.ellipse([20, 20, size - 20, size - 20], fill=(10, 10, 12), outline=(212, 175, 119, 80), width=3)
    
    # K letter
    font = get_font(280, bold=True)
    draw.text((110, 60), "K", fill=(212, 175, 119), font=font)
    
    # Small accent dot
    draw.ellipse([size - 120, size - 120, size - 80, size - 80], fill=(212, 175, 119))
    
    return img


def main():
    """Generate all images."""
    output_dir = "images"
    ensure_dir(output_dir)
    
    print("Generating portfolio images...")
    print("-" * 40)
    
    images = [
        ("hero-image.jpg", create_hero_image),
        ("before.jpg", create_before_image),
        ("after.jpg", create_after_image),
        ("analytics.jpg", create_analytics_image),
        ("about.jpg", create_about_image),
        ("logo.png", create_logo),
    ]
    
    for filename, generator in images:
        print(f"Creating {filename}...")
        img = generator()
        filepath = os.path.join(output_dir, filename)
        
        if filename.endswith('.png'):
            img.save(filepath, 'PNG')
        else:
            img.save(filepath, 'JPEG', quality=95)
        
        print(f"  ✓ Saved to {filepath}")
    
    print("-" * 40)
    print("All images generated successfully!")
    print(f"Location: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    main()