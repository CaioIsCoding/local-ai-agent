import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Mock PIL before importing CarouselService
mock_pil = MagicMock()
mock_image = MagicMock()
mock_pil.Image = mock_image
mock_pil.Image.Resampling.LANCZOS = 1
sys.modules['PIL'] = mock_pil
sys.modules['PIL.Image'] = mock_image

from app.services.carousel import CarouselService
from app.core.constants import ProcessingLimits

class TestCarouselServiceMock(unittest.TestCase):
    @patch('os.makedirs')
    def test_create_carousel_tiles_4_5(self, mock_makedirs):
        # Setup mock image
        mock_img_instance = MagicMock()
        mock_img_instance.size = (2000, 2000)
        mock_image.open.return_value = mock_img_instance

        # Mock resize to return another mock image
        mock_resized_img = MagicMock()
        mock_resized_img.size = (1080 * 3, 1350)
        mock_img_instance.resize.return_value = mock_resized_img

        # Mock crop to return another mock image
        mock_cropped_img = MagicMock()
        mock_resized_img.crop.return_value = mock_cropped_img
        mock_cropped_img.size = (1080 * 3, 1350)

        # Mock tile crop
        mock_tile = MagicMock()
        mock_cropped_img.crop.return_value = mock_tile

        num_tiles = 3
        ratio = "4:5"
        output_dir = "dummy_dir"

        tile_paths = CarouselService.create_carousel_tiles("dummy.jpg", output_dir, num_tiles=num_tiles, ratio=ratio)

        # Verify target height used
        self.assertEqual(ProcessingLimits.HEIGHT_FEED, 1350)

        # Verify resize was called with correct height
        # resize_ratio = 1350 / 2000 = 0.675
        # 2000 * 0.675 = 1350
        mock_img_instance.resize.assert_called()
        args, kwargs = mock_img_instance.resize.call_args
        self.assertEqual(args[0][1], ProcessingLimits.HEIGHT_FEED)

        # Verify crop or further resize logic (simplified here)
        self.assertEqual(len(tile_paths), num_tiles)

    @patch('os.makedirs')
    def test_create_carousel_tiles_1_1(self, mock_makedirs):
        # Setup mock image
        mock_img_instance = MagicMock()
        mock_img_instance.size = (2000, 2000)
        mock_image.open.return_value = mock_img_instance

        # Mock resize to return another mock image
        mock_resized_img = MagicMock()
        mock_resized_img.size = (1080 * 3, 1080)
        mock_img_instance.resize.return_value = mock_resized_img

        # Mock crop
        mock_cropped_img = MagicMock()
        mock_resized_img.crop.return_value = mock_cropped_img
        mock_cropped_img.size = (1080 * 3, 1080)

        # Mock tile crop
        mock_tile = MagicMock()
        mock_cropped_img.crop.return_value = mock_tile

        num_tiles = 3
        ratio = "1:1"
        output_dir = "dummy_dir"

        tile_paths = CarouselService.create_carousel_tiles("dummy.jpg", output_dir, num_tiles=num_tiles, ratio=ratio)

        # Verify target height used
        self.assertEqual(ProcessingLimits.HEIGHT_SQUARE, 1080)

        # Verify resize was called with correct height
        mock_img_instance.resize.assert_called()
        args, kwargs = mock_img_instance.resize.call_args
        self.assertEqual(args[0][1], ProcessingLimits.HEIGHT_SQUARE)

        self.assertEqual(len(tile_paths), num_tiles)

if __name__ == "__main__":
    unittest.main()
