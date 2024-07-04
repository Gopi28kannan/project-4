class locates:
    #popup window
    pop_up = '//div[@class="image-poplayer-modal"]//img[@class="pop-close-btn"]'
    set_language_currency = '//div[@class="ship-to--menuItem--WdBDsYl"]'
    #select_countries = '//div[@class="select--wrap--3N7DHe_"]//div[@class="select--arrow--1cha40Y"]'
    country_names = '//div[@class="select--search--20Pss08"]/input'
    click_name = '//div[@class="select--item--32FADYB"]//span'
    click_save = '//div[@class="es--saveBtn--w8EuBuy"]'

    #search_item
    search_item = '//input[@class="search--keyword--15P08Ji"]'
    submit_button = '//input[@class="search--submit--2VTbd-T"][@type="button"]'
    select_price1 = '//div//span[1]//input[@type="text"][@class="comet-input"]'
    select_price2 = '//div//span[3]//input[@type="text"][@class="comet-input"]'
    price_click_ok = '//span[@class="price--ok--30GSiFy"]'

    #select_items
    items='#card-list > div:nth-child('  # by css selector

    #open_item
    review = '//div[@data-pl="product-reviewer"]//a[@href="#nav-review"]'
    buy_orders = '//div[@data-pl="product-reviewer"]/span[2]'

    #extract data
    product_name = '//h1[@data-pl="product-title"]'
    #description = '//div[@id="product-description"]'
    click_description = '//a[@title="Description"]'
    description = "product-description"  #by id
    image_link = '//div[@id="product-description"]//img'
    image_link_1 = '//div[@class="image-view--wrap--ewraVkn"]//img'
    image_link_2= '//div[@class="pdp-info-left"]//img'
    price = '//div[@data-pl="product-price"]/div[1]'

    #go to next page
    click_next_1 = '//li[@class="comet-pagination-next"]'
    click_next_2 = '//li[@class="comet-pagination-next comet-pagination-disabled"][@aria-disabled="true"]'

    
