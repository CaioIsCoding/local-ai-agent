from PIL import Image, ImageEnhance
import os

class BrandingService:
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
