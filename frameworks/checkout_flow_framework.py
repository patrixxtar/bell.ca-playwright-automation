import allure
from playwright.sync_api import Page, expect
from utils.shared_utils import PlaywrightUtils

class CheckoutFlowFramework:
    def __init__(self, page: Page, config, locators):
        self.page = page
        self.config = config
        self.locators = locators
        self.utils = PlaywrightUtils(page)

    @allure.step("Fill Personal Info")
    def fill_personal_info(self):
        self.utils.wait_for_ready()
        locs = self.locators["personal"]
        
        self.page.locator(self.utils.parse_loc(locs["first_name"])).fill(self.config["first_name"])
        self.page.locator(self.utils.parse_loc(locs["last_name"])).fill(self.config["last_name"])
        self.page.locator(self.utils.parse_loc(locs["email"])).fill(self.config["email"])
        self.page.locator(self.utils.parse_loc(locs["confirm_email"])).fill(self.config["email"])
        self.page.locator(self.utils.parse_loc(locs["phone"])).fill(self.config["phone"])
        
        # Address
        addr_input = self.page.locator(self.utils.parse_loc(locs["address"]))
        addr_input.fill(self.config["address"])
        self.page.locator(self.utils.parse_loc(locs["address_dropdown"])).first.click()
        
        self.utils.stable_click(locs["continue_btn"])
        
        # Handle Confirm Modal
        modal = self.page.locator(self.utils.parse_loc(locs["confirm_modal_title"]))
        if modal.is_visible():
            self.utils.stable_click(locs["confirm_btn"])

    @allure.step("Setup Number")
    def setup_number(self):
        self.utils.wait_for_ready()
        locs = self.locators["number"]
        self.utils.stable_click(locs["new_number_label"])
        self.utils.stable_click(locs["first_phone_option"])
        self.utils.stable_click(locs["bell_continue"])

    @allure.step("Shipping")
    def shipping(self):
        self.utils.wait_for_ready()
        self.utils.stable_click(self.locators["shipping"]["continue_btn"])

    @allure.step("Process Credit Check")
    def process_credit_check(self):
        self.utils.wait_for_ready()
        locs = self.locators["credit"]
        
        # Viewport logic translated to Playwright
        if self.page.viewport_size["width"] < 768:
            self.utils.stable_click(locs["mobile_summary_btn"])
            self.utils.stable_click(locs["bell_price_accordion"])
            self.utils.stable_click(locs["bell_purchase_accordion"])
            self.utils.stable_click(locs["why_purchase_mobile"])
            self.utils.stable_click(locs["close_why_purchase_mobile"])
        else:
            self.utils.stable_click(locs["why_purchase_desktop"])
            self.utils.stable_click(locs["close_why_purchase_desktop"])

        # Card details
        self.page.locator(self.utils.parse_loc(locs["card_number"])).fill(self.config["card_number"])
        self.page.locator(self.utils.parse_loc(locs["exp_month"])).select_option(index=1)
        self.page.locator(self.utils.parse_loc(locs["exp_year"])).select_option(index=1)
        self.page.locator(self.utils.parse_loc(locs["cvv"])).fill(self.config["cvv"])
        self.page.locator(self.utils.parse_loc(locs["dob"])).fill(self.config["birthday"])
        
        self.utils.stable_click(locs["continue_btn"])

        # VALIDATION: Context checking for Error Banner
        error_banner = self.page.locator(f"{self.utils.parse_loc(locs['error_banner_standard'])}, {self.utils.parse_loc(locs['error_banner_pink'])}").first
        expect(error_banner).to_be_visible(timeout=10000)
        
        # VISUAL VALIDATION: Take screenshot of the error state (Goal 3)
        expect(self.page).to_have_screenshot("credit_check_error.png", full_page=True)

    @allure.step("Review Page")
    def review_page(self):
        self.utils.wait_for_ready()
        expect(self.page).to_have_url(self.config["review_url"])
        self.utils.stable_click(self.locators["review"]["submit_btn"])

    def esim_checkout_flow(self):
        self.fill_personal_info()
        self.setup_number()
        self.process_credit_check()
        self.review_page()

    def psim_checkout_flow(self):
        self.fill_personal_info()
        self.setup_number()
        self.shipping()
        self.process_credit_check()
        self.review_page()