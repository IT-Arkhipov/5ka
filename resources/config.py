import json
from pprint import pprint

from playwright.sync_api import expect

from utils.init import settings
from resources.locators import locator as loc, base_url


def block_geo_requests(route):
    if 'geolocation' in route.request.url:
        route.abort()
    else:
        route.continue_()


# def get_screen_size():
#     import ctypes
#     user32 = ctypes.windll.user32
#     screen_width = user32.GetSystemMetrics(0)  # 0 for screen width
#     screen_height = user32.GetSystemMetrics(1)  # 1 for screen height
#     return screen_width, screen_height


def run_browser(pw):
    browser = pw.chromium.launch(
        # args=[
        #     '--start-maximized',
        #     "--disable-popup-blocking",  # Disables Chromium's popup blocking feature
        #     "--disable-notifications",  # Disables notifications
        #     "--disable-features=Geolocation",  # Disables geolocation
        #     "--disable-blink-features=AutomationControlled",  # Makes automation less detectable
        # ],
        headless=False,
        slow_mo=500
    )

    browser_context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        permissions=[]
    )
    # browser_context.set_geolocation({"longitude": 48.858455, "latitude": 2.294474})
    page = browser_context.new_page()
    # page = browser.new_page(no_viewport=True)
    # browser_context.clear_permissions()
    # browser_context.set_geolocation(geolocation={'latitude': 55.7558, 'longitude': 37.6176})
    # browser_context.grant_permissions(permissions=['geolocation'], origin=base_url)

    page.goto(base_url)
    # page.route("**/*", block_geo_requests)

    spinner = page.locator(loc.spinner)

    expect(spinner).not_to_be_visible()

    page.get_by_role('button', name='Хорошо').click()
    page.get_by_role('button', name='Уточните адрес доставки').click()

    page.locator(loc.modal_body).locator(loc.modal_input).fill(settings.location)
    expect(spinner).to_have_count(0)

    page.locator(loc.modal_body).locator(loc.dropdown_element).first.click()
    page.get_by_role('button', name='Доставить сюда').click()

    cookies = browser_context.cookies()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    settings.cookies = cookie_dict

    local_storage_data = page.evaluate("JSON.stringify(localStorage)")
    settings.sap_code = json.loads(
        json.loads(local_storage_data).get('DeliveryPanelStore')
    ).get('selectedAddress').get('sapCode')
    return browser, browser_context, page
