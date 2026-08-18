import time
from playwright.sync_api import Page, expect

class PlaywrightUtils:
    def __init__(self, page: Page):
        self.page = page

    def parse_loc(self, locator):
        """Helper to seamlessly convert your Selenium (By.ID, 'val') tuples to Playwright strings"""
        if isinstance(locator, tuple):
            by, val = locator
            if by == "id": return f"#{val}"
            if by == "css selector": return val
            if by == "xpath": return f"xpath={val}"
            if by == "class name": return f".{val}"
        return locator

    def stable_click(self, locator_tuple, timeout=15000, scroll=True):
        """Playwright natively auto-scrolls, waits for actionability, and clicks."""
        loc_str = self.parse_loc(locator_tuple)
        element = self.page.locator(loc_str).first
        
        if scroll:
            element.scroll_into_view_if_needed()
            
        # Playwright's click is inherently stable (waits for visible, enabled, stable)
        element.click(timeout=timeout)

    def flash_element(self, locator_tuple):
        """Visual debugging highlight using Playwright's evaluate"""
        loc_str = self.parse_loc(locator_tuple)
        element = self.page.locator(loc_str).first
        
        self.page.evaluate("""(el) => {
            const originalOutline = el.style.outline;
            const originalTransition = el.style.transition;
            el.style.transition = 'all 0.2s ease';
            el.style.outline = '4px solid #ef4444';
            el.style.outlineOffset = '2px';
            setTimeout(() => {
                el.style.outline = originalOutline;
                el.style.transition = originalTransition;
            }, 400);
        }""", element.element_handle())

    def wait_for_ready(self):
        """Replaces your custom stabilization loops"""
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")
        
        # Wait for loading overlays to disappear
        loader = self.page.locator("#brfLoadingIndicator")
        if loader.is_visible():
            loader.wait_for(state="hidden")

    def bypass_captcha(self):
        print("Attempting to bypass CAPTCHA...")
        # Note: Playwright stealth plugins exist if Cloudflare blocks you natively
        # For standard checkboxes:
        captcha = self.page.locator("iframe[src*='cloudflare']").content_frame.locator(".ctp-checkbox-label")
        if captcha.is_visible():
            captcha.click()
            self.page.wait_for_timeout(2000)