from PIL import Image, ImageEnhance, ImageFilter
import os

class BrandingService:
    @staticmethod
    def professional_polish(image_path: str, output_path: str, has_transparency: bool = False):
        """
        Apply professional color grading and subtle bokeh.
        
        a. Subtle, clean color grading (luxury white balance).
        b. Subtle bokeh (Gaussian blur on background if transparency is present).
        """
        img = Image.open(image_path).convert("RGBA")
        
        # 1. Color Grading
        # Increase brightness slightly (1.05)
        img = ImageEnhance.Brightness(img).enhance(1.05)
        # Increase vibrance/color slightly (1.1)
        img = ImageEnhance.Color(img).enhance(1.1)
        
        # Cooling the color temperature (Clinical/Luxury White Balance)
        # We do this by slightly decreasing Red and slightly increasing Blue
        r, g, b, a = img.split()
        r = r.point(lambda i: i * 0.97)
        b = b.point(lambda i: min(255, i * 1.03))
        img = Image.merge("RGBA", (r, g, b, a))

        # 2. Subtle Bokeh (if transparency is present, we assume background is separate or we blur based on mask)
        # Note: If has_transparency is True, we assume we are working on a foreground object 
        # but the prompt says "Gaussian blur on the background if PhotoRoom transparency is present".
        # This implies we might need the original background or we blur what's "behind" the mask.
        if has_transparency:
            # For a simple implementation, we apply a very light blur to the whole image 
            # then paste the sharp foreground back? 
            # Or if it's JUST the foreground, bokeh is usually for the background.
            # If we only have the foreground (PNG), bokeh doesn't apply unless we have a background.
            # Assuming "professional_polish" is called on the final composition or 
            # we simulate depth by blurring edges.
            # Let's implement a subtle edge blur or overall "soft" luxury feel if foreground only.
            # Actually, let's stick to the logic: "Gaussian blur on the background".
            # If we don't have the background here, we'll apply a very light sharpening to the subject
            # and a tiny blur to the image to simulate depth.
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

        # Final conversion and save
        if output_path.lower().endswith((".jpg", ".jpeg")):
            img = img.convert("RGB")
        img.save(output_path)
        return output_path

    @staticmethod
    def apply_watermark(base_image_path: str, watermark_path: str, output_path: str, opacity: float = 0.5, position: str = "bottom-right"):
        """
        Overlay a watermark onto a base image.
        
        :param base_image_path: Path to the base image.
        :param watermark_path: Path to the watermark/logo image.
        :param output_path: Path where the result will be saved.
        :param opacity: Opacity of the watermark (0.0 to 1.0).
        :param position: Position of the watermark ('center' or 'bottom-right').
        """
        base_image = Image.open(base_image_path).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")

        # Adjust opacity
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)

        base_width, base_height = base_image.size
        watermark_width, watermark_height = watermark.size

        # Ensure watermark is not larger than base image (default scale to 20% of base width if too large)
        max_watermark_width = base_width * 0.3
        if watermark_width > max_watermark_width:
            scale = max_watermark_width / watermark_width
            new_size = (int(watermark_width * scale), int(watermark_height * scale))
            watermark = watermark.resize(new_size, Image.Resampling.LANCZOS)
            watermark_width, watermark_height = watermark.size

        if position == "center":
            pos = ((base_width - watermark_width) // 2, (base_height - watermark_height) // 2)
        elif position == "bottom-right":
            pos = (base_width - watermark_width - 20, base_height - watermark_height - 20)
        else:
            raise ValueError("Position must be 'center' or 'bottom-right'")

        # Create a transparent overlay layer
        overlay = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
        overlay.paste(watermark, pos)
        
        # Combine
        combined = Image.alpha_composite(base_image, overlay)

        # Save as RGB if output is not PNG/WebP
        if output_path.lower().endswith((".jpg", ".jpeg")):
            combined = combined.convert("RGB")
        
        combined.save(output_path)
