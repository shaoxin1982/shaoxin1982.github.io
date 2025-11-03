"""
Generate portfolio icons from profile photo.
Creates icon-192x192.png, icon-512x512.png, icon.png, and icon.svg
"""
from pathlib import Path
from PIL import Image, ImageDraw
import base64
from io import BytesIO


def create_circular_icon(image_path: str, output_size: int) -> Image.Image:
    """
    Create a circular cropped icon from the profile photo.

    Args:
        image_path: Path to the source image
        output_size: Desired output dimension (square)

    Returns:
        PIL Image object with circular crop
    """
    # Open and convert to RGBA
    img = Image.open(image_path).convert("RGBA")

    # Make square crop (centered)
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))

    # Resize to target size
    img = img.resize((output_size, output_size), Image.Resampling.LANCZOS)

    # Create circular mask
    mask = Image.new("L", (output_size, output_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, output_size, output_size), fill=255)

    # Apply mask
    result = Image.new("RGBA", (output_size, output_size), (255, 255, 255, 0))
    result.paste(img, (0, 0), mask)

    return result


def create_png_icon(source_path: str, output_path: str, size: int):
    """Create a PNG icon at the specified size."""
    icon = create_circular_icon(source_path, size)
    icon.save(output_path, "PNG", optimize=True)
    print(f"✓ Created {output_path} ({size}x{size})")


def create_svg_icon(source_path: str, output_path: str, size: int = 512):
    """
    Create an SVG icon with embedded base64 image data.
    Uses a circular clip path for consistency.
    """
    # Create icon at desired size
    icon = create_circular_icon(source_path, size)

    # Convert to base64
    buffer = BytesIO()
    icon.save(buffer, format="PNG")
    img_data = base64.b64encode(buffer.getvalue()).decode()

    # Generate SVG with embedded image
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <clipPath id="circle">
      <circle cx="256" cy="256" r="256"/>
    </clipPath>
  </defs>
  <image xlink:href="data:image/png;base64,{img_data}"
         width="512" height="512"
         clip-path="url(#circle)"/>
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✓ Created {output_path} (SVG with embedded {size}x{size} image)")


def main():
    """Generate all icon files from the profile photo."""
    source_image = "portfolio_media/profile.jpg"

    if not Path(source_image).exists():
        print(f"Error: Source image not found at {source_image}")
        return

    print("Generating portfolio icons from profile photo...")
    print(f"Source: {source_image}\n")

    # Generate PNG icons
    create_png_icon(source_image, "icon-192x192.png", 192)
    create_png_icon(source_image, "icon-512x512.png", 512)
    create_png_icon(source_image, "icon.png", 180)

    # Generate SVG icon
    create_svg_icon(source_image, "icon.svg", 512)

    print("\n✓ All icons generated successfully!")
    print("\nGenerated files:")
    print("  - icon-192x192.png (PWA icon)")
    print("  - icon-512x512.png (PWA icon)")
    print("  - icon.png (Apple touch icon, 180x180)")
    print("  - icon.svg (Scalable vector icon)")


if __name__ == "__main__":
    main()
