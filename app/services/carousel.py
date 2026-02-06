from PIL import Image
import os
import math

class CarouselService:
    @staticmethod
    def create_carousel_tiles(image_path: str, output_dir: str, num_tiles: int = 3, ratio: str = "4:5"):
        """
        Splits a single high-res image into sequential tiles for a carousel.
        
        :param image_path: Path to the high-res concept image.
        :param output_dir: Directory to save tiles.
        :param num_tiles: Number of tiles to create (3-5).
        :param ratio: Target ratio for each tile ("4:5" or "1:1").
        """
        if not (3 <= num_tiles <= 5):
            raise ValueError("Number of tiles must be between 3 and 5.")

        img = Image.open(image_path)
        img_w, img_h = img.size

        if ratio == "4:5":
            tile_ratio = 4/5
        elif ratio == "1:1":
            tile_ratio = 1/1
        else:
            raise ValueError("Ratio must be '4:5' or '1:1'.")

        # Each tile will have height = img_h
        # So width per tile = img_h * tile_ratio
        tile_w = int(img_h * tile_ratio)
        
        # Total required width for the whole carousel
        total_required_w = tile_w * num_tiles

        # Resize image so it fits the total width while maintaining aspect ratio
        # We scale based on height to match the tiles
        # But we need to ensure the original image is wide enough.
        # If it's not wide enough, we'll scale it up.
        scale_factor = total_required_w / img_w
        new_h = int(img_h * scale_factor)
        
        # Actually, let's resize the image so its height matches the target tile height
        # then check if we have enough width.
        # Let's simplify: resize image to (total_required_w, new_h)
        # where new_h is calculated to maintain aspect ratio, but we then crop or pad height.
        # Or better: Resize image to have height that matches the ratio for the total width.
        # total_width = num_tiles * tile_width. tile_width = height * ratio.
        
        # Let's target a standard height like 1350 for 4:5 (1080x1350)
        target_height = 1350 if ratio == "4:5" else 1080
        target_tile_width = int(target_height * tile_ratio)
        target_total_width = target_tile_width * num_tiles

        # Resize original image to match target_height
        resize_ratio = target_height / img_h
        resized_img = img.resize((int(img_w * resize_ratio), target_height), Image.Resampling.LANCZOS)
        
        # Now center crop or pad the resized image to match target_total_width
        current_w, current_h = resized_img.size
        
        if current_w < target_total_width:
            # Scale up to match width
            final_scale = target_total_width / current_w
            resized_img = resized_img.resize((target_total_width, int(current_h * final_scale)), Image.Resampling.LANCZOS)
            # Crop height if it became too tall
            curr_w, curr_h = resized_img.size
            top = (curr_h - target_height) // 2
            resized_img = resized_img.crop((0, top, curr_w, top + target_height))
        else:
            # Crop width to match target_total_width
            left = (current_w - target_total_width) // 2
            resized_img = resized_img.crop((left, 0, left + target_total_width, target_height))

        # Split into tiles
        tile_paths = []
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(num_tiles):
            left = i * target_tile_width
            tile = resized_img.crop((left, 0, left + target_tile_width, target_height))
            tile_path = os.path.join(output_dir, f"tile_{i+1}.jpg")
            tile.convert("RGB").save(tile_path, "JPEG", quality=95)
            tile_paths.append(tile_path)

        return tile_paths
