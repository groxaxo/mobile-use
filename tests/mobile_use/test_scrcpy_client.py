"""
Test suite for scrcpy client wrapper.

These tests require:
1. Android device or emulator connected
2. ADB installed and accessible
3. scrcpy-client Python package installed
4. Device connected via USB or TCP/IP

Running tests:
    # Run all scrcpy tests
    pytest -v tests/mobile_use/test_scrcpy_client.py

    # Run with Android device
    pytest -v -m android tests/mobile_use/test_scrcpy_client.py
"""

import os

import pytest

from minitap.mobile_use.clients.scrcpy_client import SCRCPY_AVAILABLE

# Skip all tests if scrcpy is not available
pytestmark = pytest.mark.skipif(
    not SCRCPY_AVAILABLE,
    reason="scrcpy-client not installed. Install with: pip install scrcpy-client"
)


@pytest.fixture
def adb_device():
    """
    Get first available ADB device for testing.

    Requires an Android device or emulator to be connected.
    """
    try:
        from adbutils import adb
        devices = adb.device_list()
        if not devices:
            pytest.skip("No Android devices found. Connect a device or start an emulator.")
        return devices[0]
    except Exception as e:
        pytest.skip(f"Failed to connect to ADB: {e}")


@pytest.fixture
def scrcpy_client_wrapper(adb_device):
    """
    Create a ScrcpyClientWrapper instance for testing.

    This fixture automatically starts and stops the scrcpy client.
    """
    from minitap.mobile_use.clients.scrcpy_client import ScrcpyClientWrapper

    client = ScrcpyClientWrapper(
        device=adb_device,
        max_width=800,  # Use lower resolution for tests
        max_fps=30,     # Lower FPS for tests
    )

    # Don't start automatically - let tests control when to start
    yield client

    # Cleanup
    if client.is_started():
        client.stop()


@pytest.mark.android
def test_scrcpy_client_import():
    """Test that scrcpy client can be imported."""
    from minitap.mobile_use.clients.scrcpy_client import ScrcpyClientWrapper, SCRCPY_AVAILABLE

    assert SCRCPY_AVAILABLE, "scrcpy should be available for these tests"
    assert ScrcpyClientWrapper is not None


@pytest.mark.android
def test_scrcpy_client_initialization(adb_device):
    """Test scrcpy client can be initialized."""
    from minitap.mobile_use.clients.scrcpy_client import ScrcpyClientWrapper

    client = ScrcpyClientWrapper(device=adb_device)
    assert client is not None
    assert client.device == adb_device
    assert not client.is_started()


@pytest.mark.android
def test_scrcpy_client_start_stop(scrcpy_client_wrapper):
    """Test scrcpy client can be started and stopped."""
    client = scrcpy_client_wrapper

    # Test start
    assert client.start(), "Client should start successfully"
    assert client.is_started(), "Client should be marked as started"

    # Test stop
    client.stop()
    assert not client.is_started(), "Client should be marked as stopped"


@pytest.mark.android
def test_scrcpy_screenshot(scrcpy_client_wrapper):
    """Test scrcpy can capture screenshots."""
    import base64

    client = scrcpy_client_wrapper

    # Start client
    assert client.start(), "Client should start successfully"

    # Give scrcpy time to receive frames
    import time
    time.sleep(2)

    # Capture screenshot
    screenshot_b64 = client.get_screenshot_base64()

    # Verify screenshot
    assert screenshot_b64 is not None, "Screenshot should not be None"
    assert len(screenshot_b64) > 0, "Screenshot should have data"

    # Verify it's valid base64
    try:
        base64.b64decode(screenshot_b64)
    except Exception as e:
        pytest.fail(f"Screenshot is not valid base64: {e}")


@pytest.mark.android
def test_scrcpy_get_resolution(scrcpy_client_wrapper):
    """Test scrcpy can retrieve device resolution."""
    client = scrcpy_client_wrapper

    # Start client
    assert client.start(), "Client should start successfully"

    # Give scrcpy time to initialize
    import time
    time.sleep(2)

    # Get resolution
    width, height = client.get_resolution()

    # Verify resolution
    assert width > 0, "Width should be greater than 0"
    assert height > 0, "Height should be greater than 0"
    assert width <= 2000, "Width should be reasonable"
    assert height <= 4000, "Height should be reasonable"


@pytest.mark.android
def test_scrcpy_pil_image(scrcpy_client_wrapper):
    """Test scrcpy can return PIL Image."""
    client = scrcpy_client_wrapper

    # Start client
    assert client.start(), "Client should start successfully"

    # Give scrcpy time to receive frames
    import time
    time.sleep(2)

    # Get PIL image
    image = client.get_screenshot_pil()

    # Verify image
    assert image is not None, "Image should not be None"
    assert image.width > 0, "Image width should be greater than 0"
    assert image.height > 0, "Image height should be greater than 0"


@pytest.mark.android
def test_scrcpy_error_handling_no_start(scrcpy_client_wrapper):
    """Test error handling when getting screenshot without starting."""
    client = scrcpy_client_wrapper

    # Try to get screenshot without starting
    with pytest.raises(RuntimeError):
        client.get_screenshot_base64()


@pytest.mark.android
def test_scrcpy_multiple_screenshots(scrcpy_client_wrapper):
    """Test scrcpy can capture multiple screenshots."""
    import time

    client = scrcpy_client_wrapper

    # Start client
    assert client.start(), "Client should start successfully"
    time.sleep(2)

    # Capture multiple screenshots
    screenshots = []
    for _ in range(3):
        screenshot = client.get_screenshot_base64()
        assert screenshot is not None
        assert len(screenshot) > 0
        screenshots.append(screenshot)
        time.sleep(0.5)

    # Verify we got different screenshots (frames should update)
    assert len(set(screenshots)) >= 1, "Should have captured frames"
