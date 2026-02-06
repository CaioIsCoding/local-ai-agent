import ffmpeg
import os

class VideoService:
    @staticmethod
    def crop_to_vertical(input_path: str, output_path: str):
        """
        Crops a video to 9:16 aspect ratio (Stories/Reels).
        It centers the crop.
        """
        probe = ffmpeg.probe(input_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        if not video_stream:
            raise ValueError("No video stream found in the input file.")

        width = int(video_stream['width'])
        height = int(video_stream['height'])

        target_ratio = 9/16
        
        # Calculate crop dimensions
        if width / height > target_ratio:
            # Video is wider than 9:16
            new_width = int(height * target_ratio)
            x_offset = (width - new_width) // 2
            y_offset = 0
            new_height = height
        else:
            # Video is taller than 9:16 (unlikely for standard video but possible)
            new_height = int(width / target_ratio)
            y_offset = (height - new_height) // 2
            x_offset = 0
            new_width = width

        (
            ffmpeg
            .input(input_path)
            .crop(x_offset, y_offset, new_width, new_height)
            .output(output_path, acodec='copy')
            .overwrite_output()
            .run()
        )
        return output_path

    @staticmethod
    def apply_watermark(video_path: str, watermark_path: str, output_path: str, position: str = "bottom_right"):
        """
        Overlays a brand watermark onto a video.
        """
        # Position logic for FFmpeg overlay filter
        # main_w, main_h = video dimensions
        # overlay_w, overlay_h = watermark dimensions
        positions = {
            "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2",
            "bottom_right": "main_w-overlay_w-20:main_h-overlay_h-20",
            "top_right": "main_w-overlay_w-20:20"
        }
        
        overlay_pos = positions.get(position, positions["bottom_right"])

        video = ffmpeg.input(video_path)
        watermark = ffmpeg.input(watermark_path)

        (
            ffmpeg
            .filter([video, watermark], 'overlay', overlay_pos)
            .output(output_path)
            .overwrite_output()
            .run()
        )
        return output_path
