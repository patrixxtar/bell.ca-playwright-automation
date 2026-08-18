import pytest
from configs.bell_config import DEVICE_PROFILES

def pytest_addoption(parser):
    parser.addoption("--device", action="store", default="desktop", help="desktop, iphone_15_pro_max, etc.")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    """Dynamically sets Viewports, User-Agents, and FFMPEG Video Recording"""
    device_key = pytestconfig.getoption("device")
    
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
    """Replaces your Threading PopupHandler. Playwright monitors this in the background natively."""
    page.add_locator_handler(
        page.locator("#close-lightbox"),
        lambda: page.locator("#close-lightbox").click()
    )
    page.add_locator_handler(
        page.locator("#onetrust-accept-btn-handler"),
        lambda: page.locator("#onetrust-accept-btn-handler").click()
    )
    yield