import json

from playwright.sync_api import expect

from utils.init import settings
from resources.locators import locator as loc, base_url


def block_geo_requests(route):
    if 'geolocation' in route.request.url:
        route.abort()
    else:
        route.continue_()


def run_browser(pw):
    browser = pw.chromium.launch(
        headless=False,
        slow_mo=500
    )

    browser_context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        permissions=[]
    )
    page = browser_context.new_page()
    page.goto(base_url)

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
