base_url = 'https://5ka.ru/'

categories_url = (
    lambda sap_code: f'https://5d.5ka.ru/api/catalog/v1/stores/{sap_code}/categories?mode=delivery&include_subcategories=1'
)

products_url = (
    lambda sap_code, category_id, count: f'https://5d.5ka.ru/api/catalog/v1/stores/{sap_code}/categories/{category_id}/products?mode=delivery&limit={count}'
)


class Locators:
    spinner = '.chakra-spinner'
    address_select_button = '//*[contains(@class, "chakra-button")]'
    modal_body = '.chakra-modal__body'
    modal_input = '.chakra-input'
    modal_button = '.chakra-button'

    dropdown = '.chakra-input__group'
    dropdown_element = '//*[contains(@class, "chakra-input__group")]/following::*/*[contains(@class, "chakra-text")]'


locator = Locators()
