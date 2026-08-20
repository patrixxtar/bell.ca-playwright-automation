import pytest
from playwright_stealth.stealth import stealth_sync
from configs.bell_config import DEVICE_PROFILES

def pytest_addoption(parser):
    # Custom option to avoid conflicts with pytest-playwright's built-in --device
    parser.addoption("--target-device", action="store", default="desktop", help="desktop, iphone_15_pro_max, etc.")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    device_key = pytestconfig.getoption("--target-device")
    
    profile = DEVICE_PROFILES.get("desktop") 
    for category in DEVICE_PROFILES.values():
        if device_key in category:
            profile = category[device_key]
            break

    args = {
        **browser_context_args,
        "viewport": {"width": profile["display_size"][0], "height": profile["display_size"][1]}
    }
    
    if profile.get("mobile_emulation"):
        args["user_agent"] = profile["mobile_emulation"]["userAgent"]
        args["is_mobile"] = True
        args["has_touch"] = profile["mobile_emulation"]["deviceMetrics"]["touch"]

    return args

@pytest.fixture(autouse=True)
def popup_monitor(page):
    """Applies stealth and sets up handlers for dynamic popups/overlays."""
    stealth_sync(page)
    
    page.add_locator_handler(
        page.locator("#close-lightbox"),
        lambda overlay: overlay.click()
    )
    page.add_locator_handler(
        page.locator("#onetrust-accept-btn-handler"),
        lambda overlay: overlay.click()
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