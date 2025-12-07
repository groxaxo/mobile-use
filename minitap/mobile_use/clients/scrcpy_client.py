"""
Scrcpy client wrapper for wireless screen mirroring and control.

This module provides a wrapper around the scrcpy-client library to enable
high-performance wireless screen mirroring for Android devices.
"""

import base64
import time
from io import BytesIO
from typing import Optional

import numpy as np
from adbutils import AdbDevice
from PIL import Image

from minitap.mobile_use.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from scrcpy import Client as ScrcpyClient
    SCRCPY_AVAILABLE = True
except ImportError:
    SCRCPY_AVAILABLE = False
    logger.warning("scrcpy-client not available. Install with: pip install scrcpy-client")


class ScrcpyClientWrapper:
    """
    Wrapper for scrcpy client to provide screen mirroring capabilities.
    
    This wrapper enables wireless screen mirroring with better performance
    compared to traditional ADB screenshot methods.
    """

    def __init__(
        self,
        device: AdbDevice,
        max_width: int = 0,
        bitrate: int = 8000000,
        max_fps: int = 60,
        stay_awake: bool = True,
    ):
        """
        Initialize ScrcpyClientWrapper.

        Args:
            device: AdbDevice instance
            max_width: Maximum frame width (0 means device resolution)
            bitrate: Video bitrate (default 8Mbps)
            max_fps: Maximum frames per second (default 60)
            stay_awake: Keep device awake during mirroring
        """
        if not SCRCPY_AVAILABLE:
            raise ImportError(
                "scrcpy-client is required for scrcpy support. "
                "Install it with: pip install scrcpy-client"
            )

        self.device = device
        self.max_width = max_width
        self.bitrate = bitrate
        self.max_fps = max_fps
        self.stay_awake = stay_awake
        self._client: Optional[ScrcpyClient] = None
        self._started = False
        self._last_frame: Optional[np.ndarray] = None
        self._frame_available = False

    def start(self) -> bool:
        """
        Start the scrcpy client and begin screen mirroring.

        Returns:
            bool: True if started successfully, False otherwise
        """
        if self._started:
            logger.warning("Scrcpy client already started")
            return True

        try:
            logger.info(f"Starting scrcpy client for device {self.device.serial}")
            self._client = ScrcpyClient(
                device=self.device,
                max_width=self.max_width,
                bitrate=self.bitrate,
                max_fps=self.max_fps,
                stay_awake=self.stay_awake,
                block_frame=False,
            )

            # Register frame callback
            self._client.add_listener("frame", self._on_frame)

            # Start the client
            self._client.start(threaded=True)
            
            # Wait for first frame
            max_wait = 5  # seconds
            start_time = time.time()
            while not self._frame_available and (time.time() - start_time) < max_wait:
                time.sleep(0.1)

            if not self._frame_available:
                logger.warning("No frame received within timeout, but client started")

            self._started = True
            logger.success(f"Scrcpy client started successfully for {self.device.serial}")
            return True

        except Exception as e:
            logger.error(f"Failed to start scrcpy client: {e}")
            self._cleanup()
            return False

    def _on_frame(self, frame: np.ndarray) -> None:
        """
        Callback for frame updates from scrcpy.

        Args:
            frame: numpy array containing the frame data
        """
        self._last_frame = frame
        self._frame_available = True

    def get_screenshot_base64(self) -> str:
        """
        Get the current frame as a base64-encoded image.

        Returns:
            str: Base64-encoded PNG image of the current frame

        Raises:
            RuntimeError: If client is not started or no frame is available
        """
        if not self._started:
            raise RuntimeError("Scrcpy client not started")

        if self._last_frame is None:
            raise RuntimeError("No frame available from scrcpy")

        try:
            # Convert numpy array to PIL Image
            # scrcpy returns frames in RGB format
            image = Image.fromarray(self._last_frame)

            # Convert to PNG and encode as base64
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()

            return base64.b64encode(image_bytes).decode("utf-8")

        except Exception as e:
            logger.error(f"Failed to encode screenshot: {e}")
            raise

    def get_screenshot_pil(self) -> Optional[Image.Image]:
        """
        Get the current frame as a PIL Image.

        Returns:
            PIL Image or None if no frame available
        """
        if not self._started or self._last_frame is None:
            return None

        try:
            return Image.fromarray(self._last_frame)
        except Exception as e:
            logger.error(f"Failed to convert frame to PIL Image: {e}")
            return None

    def get_resolution(self) -> tuple[int, int]:
        """
        Get the current screen resolution.

        Returns:
            tuple: (width, height) of the screen
        """
        if self._client and self._client.resolution:
            return self._client.resolution
        return (0, 0)

    def is_started(self) -> bool:
        """Check if the scrcpy client is started."""
        return self._started

    def _cleanup(self) -> None:
        """Internal cleanup of resources."""
        if self._client:
            try:
                self._client.stop()
            except Exception as e:
                logger.warning(f"Error stopping scrcpy client: {e}")
            self._client = None

        self._started = False
        self._last_frame = None
        self._frame_available = False

    def stop(self) -> None:
        """
        Stop the scrcpy client and cleanup resources.
        """
        if not self._started:
            return

        logger.info("Stopping scrcpy client")
        self._cleanup()
        logger.success("Scrcpy client stopped")

    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
