#bell_config

CONFIG = {
    "target_url": "https://www.bell.ca/",
    "username": "baddaline1",
    "password": "Azul1234$",
    "device_name": "S26 Ultra",
    "plan_name": "Ultra",
    "upc_code": "UPC1",
    "esim_imei": "357498198275732",
    "first_name": "Bqat",
    "last_name": "Testing",
    "email": "test@yopmail.com",
    "phone": "4167020880",
    "address": "5115 creekbank",
    "card_number": "41111111111111111",
    "cvv": "233",
    "birthday": "01/01/1991",
    "review_url": "https://bell.ca/Order/Index#/OrderReview",
}

SELECTORS = {
    "popups": {
        "close": "#close-lightbox",
        "cookie_banner": "#onetrust-accept-btn-handler",
        "chat_minimize": "#ujet-minimize",
        "chat_close": "xpath=//div[@class='home_foot']//button[text()='No']",
    },

    "nav": {
        "mobile_menu": "#mobileBarNavBtnG",
        "mobility_btn": "xpath=//button[contains(., 'Mobility')]",
        "plans_link": "xpath=//a[contains(@href, '/Mobility/Cell_phone_plans')]",
        "device_link": "xpath=//a[contains(@href, '/Mobility/Smartphones_and_mobile_internet_devices')]",
    },

    "login": {
        "desktop_login_cta": "#desktopLoginLink",
        "mobile_login_cta": "#mobileLoginLinkG",
        "username_input": "#username",
        "username_cta": "xpath=//button[contains(@class, '_button-login-id')]",
        "password_input": "#password",
        "password_cta": "xpath=//button[contains(text(), 'Log in')]",
    },

    "ciam": {
        "ciam_page": "xpath=//h1[contains(text(), 'Confirm your identity')]",
        "another_contact": "xpath=//button[contains(text(), 'Use another contact method')]",
        "another_contact_option": "xpath=//h1[contains(text(), 'Select another contact method')]",
        "email_option": "xpath=//button[//span[text()='Email']]",
        "otp_input": "#code",
        "otp_submit": "xpath=//button[contains(text(), 'Submit')]",
        "email_input": "#userInput",
        "open_inbox": "#openInboxBtn",
        "inbox_container": "#inbox-container",
        "email_rows": "xpath=//details[contains(@class, 'group')]",
        "datetime": "xpath=.//*[contains(@class, 'date-local')]",
        "copy_code": "xpath=.//button[contains(@class, 'copy-btn')]",
    },

    "plans": {
        "plan_card": f"xpath=//h3[contains(text(), '{CONFIG['plan_name']}')]/ancestor::div[contains(@class,'card-plan')]",
        "plan_button": "xpath=.//button[contains(text(),'Bring your own phone')]",
        "carousel_next": "xpath=//button[contains(@class, 'slick-next')]",
        "carousel_prev": "xpath=//button[contains(@class, 'slick-prev')]",
        "slick_dots": ".slick-dots",
    },

    "device_listing": {
        "phone_container": "xpath=//h1[contains(text(), 'Cell Phones')]",
        "samsung_list": "#viewall_Samsung",
        "apple_list": "#viewall_Apple",
        "google_list": "#viewall_Google",
    },

    "modals": {
        "offer_close": "xpath=//div[contains(@class, 'personalization-modal-container')]//button[contains(@class, 'personalization-modal-close')]",
        "new_customer_btn": "#newCustomerButton",
        "mobility_only_btn": "#btnMobilityOnly",
    },

    "plan_config": {
        "edit_btn": "#editBtnRatePlanSection_SBPage",
        "plan_tab": "#tabpanel-pills-data-allotment",
        "alt_plan": "xpath=//div[@id='tabpanel-pills-data-allotment']//h3[not(contains(text(), 'Ultra'))]/ancestor::div[contains(@class, 'graphical_ctrl_container')]",
        "ultra_plan": "xpath=//div[@id='tabpanel-pills-data-allotment']//h3[contains(text(), 'Ultra')]/ancestor::div[contains(@class, 'graphical_ctrl_container')]",
        "next_step": "#next-step-button-1",
    },

    "upc": {
        "upc_cta": "#enterPromoCodeCTA",
        "upc_input": "#modal-enter-code",
        "upc_submit": "#submitbtn",
        "accordion_container": "#promoCode-accordion",
        "accordions": "#promoCode-accordion .collapse-trigger",
        "continue_btn": "#promoCodeContinueBtn",
        "add_ons_btn": "#next-step-button-2",
    },

    "byod": {
        "imei_input": "#imei-number",
        "find_imei_link": "#whereToFindImeiInfo",
        "android_tab": "#android",
        "ios_tab": "#iOS",
        "close_imei_modal": "#closeIMEIModalButton",
        "success_icon": ".icon-checkmark",
        "add_to_cart": "#addToCartCTA",
        "psim_add_to_cart": "#next-step-button-3",
        "psim_option": "xpath=//label[@for='multiSimCard']",
    },

    "device": {
        "device_name": "xpath=//h1[@class='device-name']",
    },

    "cart": {
        "continue_btn": "xpath=//button[contains(text(), 'Continue to cart')]",
        "offer_modal_title": "#modal-addition-offers-title",
        "offer_modal_close": "#eligible_offers_lightbox",
        "cart_confirmation": "xpath=//*[contains(text(), 'Order summary') or contains(text(), 'Cart')]",
        "footer": "xpath=//nav[@aria-label='Privacy, security and legal'] | //nav[contains(@class, 'legal-links')]",
        "checkout_btn": "#next-step-button-undefined",
    },
}

DEVICE_PROFILES = {
    "desktop": {
        "display_size": (2560, 1440),
        "mobile_emulation": None,
        "folder": "desktop-views"
    },

    "mobile": {
        "iphone_15_pro_max": {
            "display_size": (394, 852),
            "mobile_emulation": {
                "deviceMetrics": {"width": 394, "height": 852, "pixelRatio": 3.0, "touch": True},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
            },
            "folder": "mobile-views"
        },
        "galaxy_s24_fe": {
            "display_size": (360, 780),
            "mobile_emulation": {
                "deviceMetrics": {"width": 360, "height": 780, "pixelRatio": 3.0, "touch": True},
                "userAgent": "Mozilla/5.0 (Linux; Android 14; SM-S721B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
            },
            "folder": "mobile-views"
        }
    },

    "tablet": {
        "tablet_mobile_ui": {
            "display_size": (820, 1180),
            "mobile_emulation": {
                "deviceMetrics": {"width": 820, "height": 1180, "pixelRatio": 2.0, "touch": True},
                "userAgent": "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
            },
            "folder": "tablet-views"
        },
        "tablet_desktop_ui": {
            "display_size": (1366, 1024),
            "mobile_emulation": {
                "deviceMetrics": {"width": 1366, "height": 1024, "pixelRatio": 2.0, "touch": True},
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
            },
            "folder": "tablet-views"
        }
    }
}