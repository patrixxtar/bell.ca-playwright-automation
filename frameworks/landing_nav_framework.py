import time
import allure
from playwright.sync_api import Page, expect
from utils.shared_utils import PlaywrightUtils
from utils.email_utils import get_latest_otp

class LandingNavigationFramework:
    def __init__(self, page: Page, config, selectors):
        self.page = page
        self.config = config
        self.s = selectors
        self.utils = PlaywrightUtils(page)

    @allure.step("Open Site")
    def open_site(self):
        self.page.goto(self.config['target_url'])
        self.utils.wait_for_ready()

    @allure.step("Login Flow")
    def login_flow(self):
        mobile_menu = self.page.locator(self.utils.parse_loc(self.s["nav"]["mobile_menu"]))
        if mobile_menu.is_visible():
            self.utils.stable_click(self.s["nav"]["mobile_menu"])
            self.utils.stable_click(self.s["login"]["mobile_login_cta"])
        else:
            self.utils.stable_click(self.s["login"]["desktop_login_cta"])

        self.page.locator(self.utils.parse_loc(self.s["login"]["username_input"])).fill(self.config["username"])
        self.utils.bypass_captcha()
        self.utils.stable_click(self.s["login"]["username_cta"])

        self.page.locator(self.utils.parse_loc(self.s["login"]["password_input"])).fill(self.config["password"])
        self.utils.stable_click(self.s["login"]["password_cta"])

    @allure.step("Complete 2FA")
    def complete_2fa(self):
        ciam_page = self.page.locator(self.utils.parse_loc(self.s["ciam"]["ciam_page"])).first
        if ciam_page.is_visible():
            self.utils.stable_click(self.s["ciam"]["another_contact"])
            self.utils.stable_click(self.s["ciam"]["email_option"])
            
            # Fetch OTP
            otp_code = get_latest_otp(self.config["username"])
            
            self.page.locator(self.utils.parse_loc(self.s["ciam"]["otp_input"])).fill(otp_code)
            self.utils.stable_click(self.s["ciam"]["otp_submit"])

    @allure.step("Navigate to BYOD")
    def navigate_byod(self):
        mobility_locator = self.page.locator(self.utils.parse_loc(self.s["nav"]["mobility_btn"])).first
        mobility_locator.wait_for(state="visible", timeout=20000)
        self.utils.stable_click(self.s["nav"]["mobility_btn"])
        self.utils.stable_click(self.s["nav"]["plans_link"])

    @allure.step("Bell BYOD SB Flow")
    def bell_byod_sb(self, sim_type="esim", has_upc=False):
        self._bell_select_byod_plan()
        self._bell_handle_modals()
        self.utils.wait_for_ready()
        
        if has_upc:
            self._bell_process_upc()
            
        self._bell_dynamic_byod_plan()
        
        if has_upc:
            self._bell_add_ons_step()
            
        self._bell_configure_sim(sim_type)

    
    @allure.step("Virgin BYOD SB Flow")
    def virgin_byod_sb(self, sim_type="esim"):
        self._virgin_select_byod_plan()
        self._virgin_handle_modals()
        self.utils.wait_for_ready()
        
        # Check if mobile context based on Playwright's native viewport size
        is_mobile = self.page.viewport_size["width"] < 768
        
        self.page.locator(self.utils.parse_loc(self.s["plan_config"]["next_step"])).wait_for(state="visible")
        self._virgin_dynamic_byod_plan(is_mobile)
        self._virgin_configure_sim(sim_type)

    # --- HELPER METHODS ---
    def _bell_select_byod_plan(self):
        plan_card_loc = self.utils.parse_loc(self.s["plans"]["plan_card"])
        btn_loc = self.utils.parse_loc(self.s["plans"]["plan_button"])
        
        # Auto-retrying assertion for context checking
        expect(self.page.locator(plan_card_loc).first).to_be_visible(timeout=15000)
        self.page.locator(plan_card_loc).first.locator(btn_loc).click()

    def _bell_handle_modals(self):
        if self.page.locator(self.utils.parse_loc(self.s["modals"]["new_customer_btn"])).is_visible():
            self.utils.stable_click(self.s["modals"]["new_customer_btn"])
        if self.page.locator(self.utils.parse_loc(self.s["modals"]["mobility_only_btn"])).is_visible():
            self.utils.stable_click(self.s["modals"]["mobility_only_btn"])

    def _bell_process_upc(self):
        self.page.locator(self.utils.parse_loc(self.s["upc"]["upc_cta"])).click()
        self.page.locator(self.utils.parse_loc(self.s["upc"]["upc_input"])).fill(self.config["upc_code"])
        self.page.locator(self.utils.parse_loc(self.s["upc"]["upc_submit"])).click()
        self.utils.stable_click(self.s["upc"]["continue_btn"])

    def _bell_dynamic_byod_plan(self):
        self.utils.stable_click(self.s["plan_config"]["edit_btn"])
        self.utils.stable_click(self.s["plan_config"]["alt_plan"])
        self.page.wait_for_timeout(1000)
        self.utils.stable_click(self.s["plan_config"]["ultra_plan"])
        self.utils.stable_click(self.s["plan_config"]["next_step"])

    def _bell_add_ons_step(self):
        self.utils.stable_click(self.s["upc"]["add_ons_btn"])

    def _bell_configure_sim(self, sim_type):
        if sim_type == "psim":
            self.utils.stable_click(self.s["byod"]["psim_option"])
            self.utils.stable_click(self.s["byod"]["psim_add_to_cart"])
        else:
            self.page.locator(self.utils.parse_loc(self.s["byod"]["imei_input"])).fill(self.config["esim_imei"])

            loader = self.page.locator(self.utils.parse_loc(self.s["byod"]["esim_loader"]))
            try:
                if loader.is_visible(timeout=2000):
                    loader.wait_for(state="detached", timeout=15000)
            except Exception:
                pass

            # Wait for success icon context validation
            expect(self.page.locator(self.utils.parse_loc(self.s["byod"]["success_icon"]))).to_be_visible(timeout=10000)
            self.utils.stable_click(self.s["byod"]["add_to_cart"])

    def _bell_enter_cart(self):
        self.utils.wait_for_ready()
        self.utils.stable_click(self.s["cart"]["continue_btn"])

        checkout_button = self.page.locator(self.utils.parse_loc(self.s["cart"]["checkout_btn"]))
        checkout_button.wait_for(state="visible", timeout=15000)
        self.utils.stable_click(checkout_button)
        
        # Validate cart
        cart_conf_selector = (
            self.utils.parse_ln(self.s["cart"]["cart_confirmation"]) 
            if hasattr(self.utils, 'parse_ln') 
            else self.utils.parse_loc(self.s["cart"]["cart_confirmation"])
        )
        expect(self.page.locator(cart_conf_selector).first).to_be_visible(timeout=10000)

    def enter_checkout(self):
        self.utils.stable_click(self.s["cart"]["checkout_btn"])

    # --- VIRGIN SPECIFIC HELPER FUNCTIONS ---

    def _virgin_select_byod_plan(self):
        self.utils.stable_click(self.s["nav"]["activate_now"])
        self.page.wait_for_timeout(3000)
        
        # Wait for the dynamic plan container to appear
        dynamic_plan_loc = self.utils.parse_loc(self.s["plans"]["dynamic_plan_container"])
        plan_card = self.page.locator(dynamic_plan_loc).first
        plan_card.wait_for(state="visible", timeout=15000)
        
        # Click the button inside the specific plan card
        plan_button = plan_card.locator(self.utils.parse_loc(self.s["plans"]["plan_button"]))
        plan_button.click()

    def _virgin_handle_modals(self):
        new_customer_btn = self.page.locator(self.utils.parse_loc(self.s["modals"]["new_customer_btn"]))
        if new_customer_btn.is_visible():
            new_customer_btn.click()
            
        # Wait for loading screens to clear natively
        loader1 = self.page.locator(self.utils.parse_loc(self.s["modals"]["loading_overlay1"]))
        loader2 = self.page.locator(self.utils.parse_loc(self.s["modals"]["loading_overlay2"]))
        
        if loader1.is_visible():
            loader1.wait_for(state="hidden")
        if loader2.is_visible():
            loader2.wait_for(state="hidden")

    def _virgin_dynamic_byod_plan(self, is_mobile=False):
        self.utils.wait_for_ready()
        print("--- PERFORMING DYNAMIC PLAN RE-SELECTION ---")
        self.utils.stable_click(self.s["plan_config"]["next_step"])
        
        loader = self.page.locator(self.utils.parse_loc(self.s["device"]["loader"]))
        if loader.is_visible():
            loader.wait_for(state="hidden")
            
        self.page.locator(self.utils.parse_loc(self.s["device"]["imei_input"])).wait_for(state="visible")
        self.utils.stable_click(self.s["plan_config"]["edit_btn"])
        self.page.locator(self.utils.parse_loc(self.s["plan_config"]["plan_tab"])).wait_for(state="visible")
        
        if is_mobile:
            dots = self.page.locator(self.utils.parse_loc(self.s["plan_config"]["carousel_dots"]))
            # Playwright handles element arrays beautifully with .count() and .nth()
            for i in range(1, dots.count()):
                dots.nth(i).click()
                self.page.wait_for_timeout(1200)
            if dots.count() > 0:
                dots.nth(0).click()

        # Radio Toggle Logic
        plan_radios = self.page.locator(self.utils.parse_loc(self.s["plan_config"]["plan_radios"]))
        plan_radios.first.wait_for(state="attached")
        
        target_index = getattr(self, "virgin_plan_index", 1)
        alt_index = 0 if target_index != 1 else 1
        
        plan_radios.nth(alt_index).click()
        self.page.wait_for_timeout(2000)
        
        plan_radios.nth(target_index).click()
        self.page.wait_for_timeout(2000)
        
        self.utils.stable_click(self.s["plan_config"]["next_step"])
        self.utils.wait_for_ready()
        print("Plan re-selection completed.")

    def _virgin_configure_sim(self, sim_type="esim"):
        print(f"--- CONFIGURING SIM / IMEI FOR: {sim_type.upper()} ---")
        self.utils.wait_for_ready()
        self.page.locator(self.utils.parse_loc(self.s["device"]["imei_input"])).wait_for(state="visible")
        
        loader = self.page.locator(self.utils.parse_loc(self.s["device"]["loader"]))
        if loader.is_visible():
            loader.wait_for(state="hidden")
            
        find_imei = self.page.locator(self.utils.parse_loc(self.s["device"]["find_imei_link"]))
        if find_imei.is_visible():
            find_imei.click()
            self.page.wait_for_timeout(1000)
            self.utils.stable_click(self.s["device"]["android_tab"])
            self.page.wait_for_timeout(1000)
            self.utils.stable_click(self.s["device"]["ios_tab"])
            self.page.wait_for_timeout(1000)
            self.utils.stable_click(self.s["device"]["close_imei_modal"])
            
        # Ensure modal is fully closed before proceeding
        self.page.locator(self.utils.parse_loc(self.s["device"]["close_imei_modal"])).wait_for(state="hidden")
        self.utils.wait_for_ready()

        if sim_type == "psim":
            self.utils.stable_click(self.s["device"]["psim_option"])
        else:
            imei_input = self.page.locator(self.utils.parse_loc(self.s["device"]["imei_input"]))
            imei_input.fill(self.config["esim_imei"])
            # Native JS event dispatch in Playwright
            imei_input.evaluate("el => el.dispatchEvent(new Event('blur'))")
            print("IMEI validated!")
            
        self.utils.wait_for_ready()
        self.utils.stable_click(self.s["device"]["add_to_cart"])