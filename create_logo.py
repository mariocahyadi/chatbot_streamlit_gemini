from PIL import Image, ImageDraw, ImageFont

# Create a blank white image
img = Image.new('RGB', (400, 120), color = (255, 255, 255))
d = ImageDraw.Draw(img)

# Try to use a common font, fallback to default if not found
try:
    font = ImageFont.truetype('arial.ttf', 48)
except:
    font = ImageFont.load_default()

# Text to add
text = "IndoStockBot"
    # Use textbbox for accurate text size (compatible with recent Pillow)
bbox = d.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Center the text
x = (img.width - text_width) // 2
y = (img.height - text_height) // 2

d.text((x, y), text, fill=(0, 102, 204), font=font)

# Save the image
img.save('logo.png')
