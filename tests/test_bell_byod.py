import pytest
import allure
import re
from configs.bell_config import CONFIG, SELECTORS
from frameworks.landing_nav_framework import LandingNavigationFramework
from frameworks.checkout_flow_framework import CheckoutFlowFramework
from playwright.sync_api import Page, expect

@allure.feature("Checkout Flows")
@allure.story("Bell BYOD New Activation Flow")
@pytest.mark.parametrize("sim_type", ["esim", "psim"])
def test_full_bell_checkout_flow(page: Page, sim_type, has_upc=False):
    nav = LandingNavigationFramework(page, CONFIG, SELECTORS)
    checkout = CheckoutFlowFramework(page, CONFIG, SELECTORS)

    nav.open_site()
    # Notice: No login_flow() here for standard BYOD
    nav.navigate_byod()
    nav.bell_byod_sb(sim_type=sim_type, has_upc=has_upc)
    nav._bell_enter_cart()
    nav.enter_checkout()
    
    if sim_type == "esim":
        checkout.esim_checkout_flow()
    else:
        checkout.psim_checkout_flow()
        
    expect(page).to_have_url(re.compile(r".*OrderReview.*"))