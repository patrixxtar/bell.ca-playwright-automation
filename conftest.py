import pytest
from playwright_stealth import stealth
from configs.bell_config import DEVICE_PROFILES

def pytest_addoption(parser):
    # Changed from --device to --target-device to avoid conflicts with pytest-playwright
    parser.addoption("--target-device", action="store", default="desktop", help="desktop, iphone_15_pro_max, etc.")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    """Dynamically sets Viewports, User-Agents, and FFMPEG Video Recording"""
    # Updated to fetch the new argument name
    device_key = pytestconfig.getoption("--target-device")
    
    # Find profile in your config (search mobile, tablet, desktop)
    profile = DEVICE_PROFILES.get("desktop") # Default fallback
    for category in DEVICE_PROFILES.values():
        if device_key in category:
            profile = category[device_key]
            break

    args = {
        **browser_context_args,
        "viewport": {"width": profile["display_size"][0], "height": profile["display_size"][1]},
        "record_video_dir": "jenkins_reports/videos/", # Native FFMPEG replacement!
        "record_video_size": {"width": 1280, "height": 720}
    }
    
    if profile.get("mobile_emulation"):
        args["user_agent"] = profile["mobile_emulation"]["userAgent"]
        args["is_mobile"] = True
        args["has_touch"] = profile["mobile_emulation"]["deviceMetrics"]["touch"]

    return args

@pytest.fixture(autouse=True)
def popup_monitor(page):
    """Applies stealth and monitors for popups."""
    # Apply stealth to the page before doing anything else
    stealth(page)
    
    page.add_locator_handler(
        page.locator("#close-lightbox"),
        lambda: page.locator("#close-lightbox").click()
    )
    page.add_locator_handler(
        page.locator("#onetrust-accept-btn-handler"),
        lambda: page.locator("#onetrust-accept-btn-handler").click()
    )
    yield

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Passes arguments to Chromium to hide the automation flag."""
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-sandbox",
        ]
    }