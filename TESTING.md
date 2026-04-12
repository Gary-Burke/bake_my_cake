# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

## Code Validation

### HTML

I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.  
Pages that require authentication can not be validated by URL so for those pages I used "validate by input" and therefore there is no link available for those pages.

> [!NOTE]  
> This project uses Django Allauth and since the code in those templates are from a thrid party, I have opted to exclude those templates from my validation checks. 

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| pages | [index.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/templates/pages/index.html) | [LINK](https://validator.w3.org/nu/?doc=https://bake-my-cake-b1b688b8e8e7.herokuapp.com/&out=html#textarea) | ![screenshot](documentation/testing/validation/html-pages-index.png) | No errors/warnings |
| pages | [about.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/templates/pages/about.html) | [LINK](https://validator.w3.org/nu/?doc=https://bake-my-cake-b1b688b8e8e7.herokuapp.com/about&out=html#textarea) | ![screenshot](documentation/testing/validation/html-pages-about.png) | No errors/warnings |
| pages | [custom_order.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/templates/pages/custom_order.html) | [LINK](https://validator.w3.org/nu/?doc=https://bake-my-cake-b1b688b8e8e7.herokuapp.com/custom-order&out=html#textarea) | ![screenshot](documentation/testing/validation/html-pages-custom-order.png) | No errors/warnings |
| products | [products.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/templates/products/products.html) | [LINK](https://validator.w3.org/nu/?doc=https://bake-my-cake-b1b688b8e8e7.herokuapp.com/products/&out=html#textarea) | ![screenshot](documentation/testing/validation/html-products-products.png) | No errors/warnings |
| products | [product_details.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/templates/products/product_details.html) | [LINK](https://validator.w3.org/nu/?doc=https%3A%2F%2Fbake-my-cake-b1b688b8e8e7.herokuapp.com%2Fproducts%2Fbaby-bear%2F73%2F#textarea) | ![screenshot](documentation/testing/validation/html-products-product-details.png) | Every product has a unique URL so the validation was performed on this example (product id 73) |
| products | [add_product.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/templates/products/add_product.html) | n/a | ![screenshot](documentation/testing/validation/html-products-add-product.png) | No errors/warnings |
| products | [edit_product.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/templates/products/edit_product.html) | n/a | ![screenshot](documentation/testing/validation/html-products-edit-product.png) | No errors/warnings |
| basket | [basket.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/basket/templates/basket/basket.html) | n/a | ![screenshot](documentation/testing/validation/html-basket-basket.png) | No errors/warnings |
| basket | [edit_basket.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/basket/templates/basket/edit_basket.html) | n/a | ![screenshot](documentation/testing/validation/html-basket-edit-basket.png) | No errors/warnings |
| checkout | [checkout.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/templates/checkout/checkout.html) | n/a | ![screenshot](documentation/testing/validation/html-checkout-checkout.png) | No errors/warnings |
| checkout | [complete.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/templates/checkout/complete.html) | n/a | ![screenshot](documentation/testing/validation/html-checkout-complete.png) | No errors/warnings |
| profiles | [profile.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/templates/profiles/profile.html) | n/a | ![screenshot](documentation/testing/validation/html-profiles-profile.png) | No errors/warnings |
| profiles | [profile.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/templates/profiles/profile.html) | n/a | ![screenshot](documentation/testing/validation/html-profiles-profile-orders.png) | No errors/warnings. Same template as profiles but with order history included |
| templates | [404.html](https://github.com/Gary-Burke/bake_my_cake/blob/main/templates/errors/404.html) | n/a | ![screenshot](documentation/testing/validation/html-templates-404.png) | No errors/warnings |

### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate all of my CSS files.

> [!NOTE]  
> All warnings were checked and can be safely ignored, as they are related to CSS variables and vendor extensions from Autoprefixer CSS online.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| static | [style.css](https://github.com/Gary-Burke/bake_my_cake/blob/main/static/css/style.css) | [LINK](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fbake-my-cake-b1b688b8e8e7.herokuapp.com%2Fstatic%2Fcss%2Fstyle.985294e43ffb.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en#warnings) | ![screenshot](documentation/testing/validation/css-static-style.png) | No Errors |
| static | [fonts.css](https://github.com/Gary-Burke/bake_my_cake/blob/main/static/css/fonts.css) | [LINK](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fbake-my-cake-b1b688b8e8e7.herokuapp.com%2Fstatic%2Fcss%2Ffonts.d17c6ac80a19.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en) | ![screenshot](documentation/testing/validation/css-static-fonts.png) | No Errors |
| products | [products.css](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/static/products/css/products.css) | [LINK](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fbake-my-cake-b1b688b8e8e7.herokuapp.com%2Fstatic%2Fproducts%2Fcss%2Fproducts.b0902d75363e.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en#warnings) | ![screenshot](documentation/testing/validation/css-products-products.png) | No Errors |
| basket | [basket.css](https://github.com/Gary-Burke/bake_my_cake/blob/main/basket/static/basket/css/basket.css) | [LINK](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fbake-my-cake-b1b688b8e8e7.herokuapp.com%2Fstatic%2Fbasket%2Fcss%2Fbasket.0e50fcd86a6c.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en#warnings) | ![screenshot](documentation/testing/validation/css-basket-basket.png) | No Errors |
| checkout | [checkout.css](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/static/checkout/css/checkout.css) | [LINK](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fbake-my-cake-b1b688b8e8e7.herokuapp.com%2Fstatic%2Fcheckout%2Fcss%2Fcheckout.1e878673ff78.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en#warnings) | ![screenshot](documentation/testing/validation/css-checkout-checkout.png) | No Errors |
| profiles | [profile.css](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/static/profiles/css/profile.css) | [LINK](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fbake-my-cake-b1b688b8e8e7.herokuapp.com%2Fstatic%2Fprofiles%2Fcss%2Fprofile.e1b618fd1a0f.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en#warnings) | ![screenshot](documentation/testing/validation/css-profiles-profile.png) | No Errors |

### JavaScript

I have used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files.

> [!NOTE]  
> When using external libraries such as Stripe and Bootstrap, the JShint validation tool would flag these as "undefined/unused variables".  
> In order to instantiate these components, we need to use their respective declarator. These warnings are acceptable.

| Directory | File | Screenshot | Notes |
| --- | --- | --- | --- |
| checkout | [checkout.js](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/static/checkout/js/checkout.js) | ![screenshot](documentation/testing/validation/js-checkout-checkout.png) | No errors |
| products | [products.js](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/static/products/js/products.js) | ![screenshot](documentation/testing/validation/js-products-products.png) | No errors |
| profiles | [profile.js](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/static/profiles/js/profile.js) | ![screenshot](documentation/testing/validation/js-profiles-profile.png) | No errors |
| static | [base.js](https://github.com/Gary-Burke/bake_my_cake/blob/main/static/js/base.js) | ![screenshot](documentation/testing/validation/js-static-base.png) | No errors |

### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| bake_my_cake | [settings.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/bake_my_cake/settings.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/bake_my_cake/settings.py) | ![screenshot](documentation/testing/validation/py-bake_my_cake-settings.png) | No errors/warnings |
| bake_my_cake | [urls.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/bake_my_cake/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/bake_my_cake/urls.py) | ![screenshot](documentation/testing/validation/py-bake_my_cake-urls.png) | No errors/warnings |
| bake_my_cake | [views.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/bake_my_cake/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/bake_my_cake/views.py) | ![screenshot](documentation/testing/validation/py-bake_my_cake-views.png) | No errors/warnings |
| basket | [contexts.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/basket/contexts.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/basket/contexts.py) | ![screenshot](documentation/testing/validation/py-basket-contexts.png) | No errors/warnings |
| basket | [urls.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/basket/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/basket/urls.py) | ![screenshot](documentation/testing/validation/py-basket-urls.png) | No errors/warnings |
| basket | [utils.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/basket/utils.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/basket/utils.py) | ![screenshot](documentation/testing/validation/py-basket-utils.png) | No errors/warnings |
| basket | [views.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/basket/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/basket/views.py) | ![screenshot](documentation/testing/validation/py-basket-views.png) | No errors/warnings |
| checkout | [admin.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/checkout/admin.py) | ![screenshot](documentation/testing/validation/py-checkout-admin.png) | No errors/warnings |
| checkout | [forms.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/checkout/forms.py) | ![screenshot](documentation/testing/validation/py-checkout-forms.png) | No errors/warnings |
| checkout | [models.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/checkout/models.py) | ![screenshot](documentation/testing/validation/py-checkout-models.png) | No errors/warnings |
| checkout | [urls.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/checkout/urls.py) | ![screenshot](documentation/testing/validation/py-checkout-urls.png) | No errors/warnings |
| checkout | [utils.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/utils.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/checkout/utils.py) | ![screenshot](documentation/testing/validation/py-checkout-utils.png) | No errors/warnings |
| checkout | [views.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/checkout/views.py) | ![screenshot](documentation/testing/validation/py-checkout-views.png) | No errors/warnings |
| checkout | [webhooks.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/checkout/webhooks.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/checkout/webhooks.py) | ![screenshot](documentation/testing/validation/py-checkout-webhooks.png) | No errors/warnings |
| pages | [admin.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/pages/admin.py) | ![screenshot](documentation/testing/validation/py-pages-admin.png) | No errors/warnings |
| pages | [forms.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/pages/forms.py) | ![screenshot](documentation/testing/validation/py-pages-forms.png) | No errors/warnings |
| pages | [models.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/pages/models.py) | ![screenshot](documentation/testing/validation/py-pages-models.png) | No errors/warnings |
| pages | [urls.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/pages/urls.py) | ![screenshot](documentation/testing/validation/py-pages-urls.png) | No errors/warnings |
| pages | [views.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/pages/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/pages/views.py) | ![screenshot](documentation/testing/validation/py-pages-views.png) | No errors/warnings |
| products | [admin.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/admin.py) | ![screenshot](documentation/testing/validation/py-products-admin.png) | No errors/warnings |
| products | [constants.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/constants.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/constants.py) | ![screenshot](documentation/testing/validation/py-products-constants.png) | No errors/warnings |
| products | [forms.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/forms.py) | ![screenshot](documentation/testing/validation/py-products-forms.png) | No errors/warnings |
| products | [models.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/models.py) | ![screenshot](documentation/testing/validation/py-products-models.png) | No errors/warnings |
| products | [display_lables.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/templatetags/display_lables.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/templatetags/display_lables.py) | ![screenshot](documentation/testing/validation/py-products-display_lables.png) | No errors/warnings |
| products | [urls.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/urls.py) | ![screenshot](documentation/testing/validation/py-products-urls.png) | No errors/warnings |
| products | [utils.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/utils.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/utils.py) | ![screenshot](documentation/testing/validation/py-products-utils.png) | No errors/warnings |
| products | [views.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/products/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/products/views.py) | ![screenshot](documentation/testing/validation/py-products-views.png) | No errors/warnings |
| profiles | [forms.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/profiles/forms.py) | ![screenshot](documentation/testing/validation/py-profiles-forms.png) | No errors/warnings |
| profiles | [models.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/profiles/models.py) | ![screenshot](documentation/testing/validation/py-profiles-models.png) | No errors/warnings |
| profiles | [urls.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/profiles/urls.py) | ![screenshot](documentation/testing/validation/py-profiles-urls.png) | No errors/warnings |
| profiles | [views.py](https://github.com/Gary-Burke/bake_my_cake/blob/main/profiles/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Gary-Burke/bake_my_cake/main/profiles/views.py) | ![screenshot](documentation/testing/validation/py-profiles-views.png) | No errors/warnings |

## Responsiveness

I've tested my deployed project to check for responsiveness issues.

| Page | Mobile | Tablet | Desktop | Notes |
| --- | --- | --- | --- | --- |
| index | ![screenshot](documentation/testing/responsiveness/index-mobile.png) | ![screenshot](documentation/testing/responsiveness/index-tablet.png) | ![screenshot](documentation/testing/responsiveness/index-desktop.png) | Works as expected |
| about | ![screenshot](documentation/testing/responsiveness/about-mobile.png) | ![screenshot](documentation/testing/responsiveness/about-tablet.png) | ![screenshot](documentation/testing/responsiveness/about-desktop.png) | Works as expected |
| basket | ![screenshot](documentation/testing/responsiveness/basket-mobile.png) | ![screenshot](documentation/testing/responsiveness/basket-tablet.png) | ![screenshot](documentation/testing/responsiveness/basket-desktop.png) | Works as expected |
| checkout | ![screenshot](documentation/testing/responsiveness/checkout-mobile.png) | ![screenshot](documentation/testing/responsiveness/checkout-tablet.png) | ![screenshot](documentation/testing/responsiveness/checkout-desktop.png) | Works as expected |
| custom-order | ![screenshot](documentation/testing/responsiveness/custom-order-mobile.png) | ![screenshot](documentation/testing/responsiveness/custom-order-tablet.png) | ![screenshot](documentation/testing/responsiveness/custom-order-desktop.png) | Works as expected |
| product-details | ![screenshot](documentation/testing/responsiveness/product-details-mobile.png) | ![screenshot](documentation/testing/responsiveness/product-details-tablet.png) | ![screenshot](documentation/testing/responsiveness/product-details-desktop.png) | Works as expected |
| products-add | ![screenshot](documentation/testing/responsiveness/products-add-mobile.png) | ![screenshot](documentation/testing/responsiveness/products-add-tablet.png) | ![screenshot](documentation/testing/responsiveness/products-add-desktop.png) | Works as expected |
| products-edit | ![screenshot](documentation/testing/responsiveness/products-edit-mobile.png) | ![screenshot](documentation/testing/responsiveness/products-edit-tablet.png) | ![screenshot](documentation/testing/responsiveness/products-edit-desktop.png) | Works as expected |
| products | ![screenshot](documentation/testing/responsiveness/products-mobile.png) | ![screenshot](documentation/testing/responsiveness/products-tablet.png) | ![screenshot](documentation/testing/responsiveness/products-desktop.png) | Works as expected |
| profile | ![screenshot](documentation/testing/responsiveness/profile-mobile.png) | ![screenshot](documentation/testing/responsiveness/profile-tablet.png) | ![screenshot](documentation/testing/responsiveness/profile-desktop.png) | Works as expected |
| 404 | ![screenshot](documentation/testing/responsiveness/404-mobile.png) | ![screenshot](documentation/testing/responsiveness/404-tablet.png) | ![screenshot](documentation/testing/responsiveness/404-desktop.png) | Works as expected |

## Browser Compatibility

I've tested my deployed project on multiple browsers to check for compatibility issues.  
I used a free account from [LambdaTest](https://app.lambdatest.com/) to test my website on **Firefox** and **Edge**.

| Page | Chrome | Firefox | Edge | Notes |
| --- | --- | --- | --- | --- |
| index | ![screenshot](documentation/features/home.png) | ![screenshot](documentation/testing/firefox/index.png) | ![screenshot](documentation/testing/edge/index.png) | Works as expected |
| products | ![screenshot](documentation/features/products.png) | ![screenshot](documentation/testing/firefox/products.png) | ![screenshot](documentation/testing/edge/products.png) | Works as expected |
| product-details | ![screenshot](documentation/features/product-details.png) | ![screenshot](documentation/testing/firefox/product-details.png) | ![screenshot](documentation/testing/edge/product-details.png) | Works as expected |
| basket | ![screenshot](documentation/features/view-basket.png) | ![screenshot](documentation/testing/firefox/basket.png) | ![screenshot](documentation/testing/edge/basket.png) | Works as expected |
| checkout | ![screenshot](documentation/features/checkout.png) | ![screenshot](documentation/testing/firefox/checkout.png) | ![screenshot](documentation/testing/edge/checkout.png) | Works as expected |
| custom-order | ![screenshot](documentation/features/custom-order.png) | ![screenshot](documentation/testing/firefox/custom-order.png) | ![screenshot](documentation/testing/edge/custom-order.png) | Works as expected |

## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool to check for any major issues.  
Some warnings are outside of my control, and mobile results tend to be lower than desktop.

**Index Page**:
- The low score on **Best Practices** is mainly due to third-party cookies directly related to the use of MailChimp for the newsletter.

**Checkout Page**:
- The low score on **Best Practices** is mainly due to third-party cookies directly related to the use of Stripe for the Online Payments.
- The low score on **Performance** for mobile is related to the Stripe pay element, the needed Javascript as well as the use of flatpickr.

| Page | Mobile | Desktop |
| --- | --- | --- |
| Index | ![screenshot](documentation/testing/lighthouse/index-mobile.png) | ![screenshot](documentation/testing/lighthouse/index-desktop.png) |
| Products | ![screenshot](documentation/testing/lighthouse/products-mobile.png) | ![screenshot](documentation/testing/lighthouse/products-desktop.png) |
| Product Details | ![screenshot](documentation/testing/lighthouse/product-details-mobile.png) | ![screenshot](documentation/testing/lighthouse/product-details-desktop.png) |
| Custom Order | ![screenshot](documentation/testing/lighthouse/custom-order-mobile.png) | ![screenshot](documentation/testing/lighthouse/custom-order-desktop.png) |
| Basket | ![screenshot](documentation/testing/lighthouse/basket-mobile.png) | ![screenshot](documentation/testing/lighthouse/basket-desktop.png) |
| Basket Edit | ![screenshot](documentation/testing/lighthouse/basket-edit-mobile.png) | ![screenshot](documentation/testing/lighthouse/basket-edit-desktop.png) |
| Checkout | ![screenshot](documentation/testing/lighthouse/checkout-mobile.png) | ![screenshot](documentation/testing/lighthouse/checkout-desktop.png) |
| Admin Add Product | ![screenshot](documentation/testing/lighthouse/products-admin-add-mobile.png) | ![screenshot](documentation/testing/lighthouse/products-admin-add-desktop.png) |
| Admin Edit Product | ![screenshot](documentation/testing/lighthouse/products-admin-edit-mobile.png) | ![screenshot](documentation/testing/lighthouse/products-admin-edit-desktop.png) |

## User Story Testing

| Target | Expectation | Outcome | Screenshot |
| --- | --- | --- | --- |
| As a user | I would like to see a clean and consistent navigation bar | so that I can easily navigate to where I want to go. | ![screenshot](documentation/features/navbar.png) |
| As a user | I would like to see a clean home page with information about the business | so that I can know what product/service is being sold. | ![screenshot](documentation/features/home.png) |
| As a user | I would like to register an account | so that I can place orders and manage my details. | ![screenshot](documentation/features/register.png) |
| As a user | I would like to log in and log out securely | so that my account information is protected. | ![screenshot](documentation/features/login.png) |
| As a user | I would like to view cakes displayed with images and prices | so that I can easily browse and choose what I want to buy. | ![screenshot](documentation/features/products.png) |
| As a user | I would like to select a cake and view its full details | so that I can understand my customization options before purchasing. | ![screenshot](documentation/features/product-details.png) |
| As a user | I would like to see a about page | so that I can find important contact and location information for the business. | ![screenshot](documentation/features/about.png) |
| As a user | I want to see a footer clearly displayed | so that I can find important information such as the privacy policy. | ![screenshot](documentation/features/footer.png) |
| As a user | I would like to submit a personalized cake request | so that I can request a completely custom design. | ![screenshot](documentation/features/custom-order.png) |
| As the owner | I would like to be able to delete products from the database | so that I can remove products that are no longer on offer. | ![screenshot](documentation/features/admin-delete.png) |
| As the owner | I would like to edit existing products in the database | so that I can keep the product listings accurate and up to date. | ![screenshot](documentation/features/admin-edit.png) |
| As the owner | I would like to add new cake and cupcake products to the website | so that customers can browse and purchase them. | ![screenshot](documentation/features/admin-add.png) |
| As a user | I would like to add customized cakes to my basket | so that I can review them before checkout. | ![screenshot](documentation/features/add-to-basket.png) |
| As a user | I would like to view my current basket | so that I can have an overview of what I have already added before checkout. | ![screenshot](documentation/features/view-basket.png) |
| As a user | I would like to update or remove items from my basket | so that I can adjust my order before purchasing. | ![screenshot](documentation/features/edit-basket.png) |
| As the owner | I would like to have a custom 404 error page displayed when applicable | so that my customers don't lose trust in the website. | ![screenshot](documentation/features/404.png) |
| As a user | I would like to select a pickup date for my order | so that I can collect my cake at a convenient time. | ![screenshot](documentation/features/date-selection.png) |
| As a user | I would like to securely checkout and make an online payment | so that I can complete my purchase safely. | ![screenshot](documentation/features/payment.png) |
| As the owner | I would like my website to meet as many SEO requirements as possible | so that users can easily find my website. | Refer to the SEO & Marketing section in the [README.md](README.md#seo--marketing) file. |
| As the owner | I would like my website to have web marketing strategies implemented | so that my brand can expand. | Refer to the SEO & Marketing section in the [README.md](README.md#seo--marketing) file. |
| As a user | I would like to customize the cake size | so that it suits the number of guests at my event. | ![screenshot](documentation/features/product-details.png) |
| As a user | I would like to change the number of tiers of a cake | so that it matches my celebration needs. | ![screenshot](documentation/features/product-details.png) |
| As a user | I would like to choose the type of sponge for my cake | so that I can select my preferred flavor. | ![screenshot](documentation/features/product-details.png) |
| As a user | I would like to select a filling for my cake | so that it matches my taste preferences. | ![screenshot](documentation/features/product-details.png) |
| As a user | I would like to choose the type of icing | so that the cake fits my taste preferences. | ![screenshot](documentation/features/product-details.png) |
| As a user | I would like to choose the main colour combination of my cake | so that the cake can look the way I want it to . | ![screenshot](documentation/features/product-details.png) |
| As a user | I would like to sort the products alphabetically and by price | so that I can make a better decision on what I want to buy. | ![screenshot](documentation/features/products-sort.png) |
| As a user | I would like to search for cakes based on their names | so that I can find a specific related product. | ![screenshot](documentation/features/products-search.png) |
| As a user | I would like to manage my profile and contact details | so that my order information is always accurate. | ![screenshot](documentation/features/profile-details.png) |
| As a user | I would like to view my order history | so that I can keep track of my previous purchases. | ![screenshot](documentation/features/profile.png) |
| As a user | I would to receive confirmation emails | so that I can be assured of my transactions. | ![screenshot](documentation/features/email-confirmation.png) |

## Defensive Programming

I have implemented measures and fixes to prevent users from hacking my website through html form manipulation and from gaining unrestricted access where applicable.  
When users add invalid data through html form manipulation, the views catch that and assign the default values to the order.  
Many of these measures have been tested through the Django Unit Tests but I have also performed manual testing for such defensive programming.

| Page | Expectation | Test | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Custom Order | Form should not submit when required fields are missing. | Attempt to submit form with empty field.  | Error messages informs user and prevents form submission. | ![screenshot](documentation/testing/defensive/custom-order-fields.png) |
| Products Add | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged out.  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/anonymous-products-add.png) |
| Products Add | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged in (not admin).  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/products-add.png) |
| Products Add | Form should not submit when required fields are missing. | Attempt to submit form with empty field.  | Error messages informs user and prevents form submission. | ![screenshot](documentation/testing/defensive/products-add-fields.png) |
| Products Delete | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged out.  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/anonymous-products-delete.png) |
| Products Delete | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged in (not admin).  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/products-delete.png) |
| Products Admin Edit | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged out.  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/anonymous-products-admin-edit.png) |
| Products Admin Edit | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged in (not admin).  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/products-admin-edit.png) |
| Products Edit | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged out.  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/anonymous-products-edit.png) |
| Products Edit | Only superuser should have access and rights to perform this action. | Attempt to brute force the url while user is logged in (not admin).  | Error messages informs user and prevents access. | ![screenshot](documentation/testing/defensive/products-edit.png) |
| Products Edit | Form should not submit when required fields are missing. | Attempt to submit form with empty field.  | Error messages informs user and prevents form submission. | ![screenshot](documentation/testing/defensive/products-edit-fields.png) |
| Profile Admin | Template should not display admin fields if user is not superuser. | Logged in as normal user.  | Template does not render admin menu. | ![screenshot](documentation/testing/defensive/profile.png) |
| Profile | Only authenticated users should have access to their profile. | Attempt to brute force the url while user is logged out.  | Access is prevented and user is redirected to login page. | ![screenshot](documentation/testing/defensive/anonymous-profile.png) |
| Product Details | When user manipulates html form the basket should be preserved with allowed values. | Attempt to manipulate html form values and add the product to the basket.  | Product is added to the basket with default allowed values. | ![screenshot](documentation/testing/defensive/product-details-form-hack.png) |
| Basket | When user manipulates html form the checkout form should be preserved with allowed values. | Attempt to manipulate html form values and proceed to checkout. | Checkout form is rendered with default allowed values. | ![screenshot](documentation/testing/defensive/basket-form-hack.png) |
| Checkout | When user manipulates html form on checkout the order should be preserved with allowed values. | Attempt to manipulate html form values and proceed to pay. | Order is placed with default allowed values. | ![screenshot](documentation/testing/defensive/checkout-form-hack.png) |
| Checkout | Form should not submit when required fields are missing. | Attempt to submit form with empty field.  | Error messages informs user and prevents form submission. | ![screenshot](documentation/testing/defensive/checkout-fields.png) |
| Checkout | When user manipulates html delivery date input to bypass flatpickr parameters, the view should catch this and prevent form submission. | Attempt to manipulate html delivery date form values and proceed to pay. | Website prevents form submission and informs user to select a valid date. | ![screenshot](documentation/testing/defensive/checkout-delivery-date-hack.png) |
| 404 | When a user navigates to a broken/non-existant url, the website should display a custom 404 page. | Attempt to navigate to a url that does not exist e.g. "https://bake-my-cake-b1b688b8e8e7.herokuapp.com/bout".  | Website dispalys custom 404 page. | ![screenshot](documentation/features/404.png) |

## Automated Testing

I have conducted a series of automated tests on my application.

> [!NOTE]  
> I fully acknowledge and understand that, in a real-world scenario, an extensive set of additional tests would be more comprehensive.

### Python (Unit Testing)

I have used Django's built-in unit testing framework to test the application functionality. In order to run the tests, I ran the following command in the terminal each time:

- `python manage.py test name-of-app`

To create the coverage report, I would then run the following commands:

- `pip3 install coverage`
- `pip3 freeze --local > requirements.txt`
- `coverage run --omit="*/site-packages/*,*/migrations/*,*/__init__.py,env.py,.env" manage.py test`
- `coverage report`

To see the HTML version of the reports, and find out whether some pieces of code were missing, I ran the following commands:

- `coverage html`
- `python -m http.server`

Below are the results from the full coverage report on my application that I've tested:

![screenshot](documentation/testing/automation/html-coverage.png)

#### Unit Test Issues

**Fixed Issues**

| Issue | Explanation | Solution | Screenshot |
| --- | --- | --- | --- |
| ValueError: Missing staticfiles manifest entry for 'images/favicon/apple-touch-icon.png' | Storages/staticfiles and emails must be set to default settings for tests | Override the static files storage backend in test settings to use the basic StaticFilesStorage | ![screenshot](documentation/testing/automation/test-backend-storage.png) |
| KeyError: category field | category is a ModelChoiceField, so it expects an integer PK of a Category instance, not the string "Birthday Cakes" |  "category": self.category.pk | ![screenshot](documentation/testing/automation/test-category.png) |
| Cloudinary Fields | Cloudinary fields expect an actual file upload, not an URL | Patch the field to be a standard SimpleUploadedFile for the purposes of form testing. | ![screenshot](documentation/testing/automation/test-cloudinary.png) |
| django.urls.exceptions.NoReverseMatch: Reverse for 'product_details' with arguments '('', 1)' not found | The product in my initial setUp function had no slug field. In my actual view this is auto-generated. | Add a slug manually in the testing environment. | ![screenshot](documentation/testing/automation/test-slug.png) |

**Known Issues**

> [!IMPORTANT]
To my knowledge there are no more known issues present in the unit tests.

## Bugs

### Fixed Bugs

[![GitHub issue custom search](https://img.shields.io/github/issues-search/Gary-Burke/bake_my_cake?query=is%3Aissue%20is%3Aclosed%20label%3Abug&label=Fixed%20Bugs&color=green)](https://www.github.com/Gary-Burke/bake_my_cake/issues?q=is%3Aissue+is%3Aclosed+label%3Abug)

I've used [GitHub Issues](https://www.github.com/Gary-Burke/bake_my_cake/issues) to track and manage bugs and issues during the development stages of my project.

All previously closed/fixed bugs can be tracked [here](https://www.github.com/Gary-Burke/bake_my_cake/issues?q=is%3Aissue+is%3Aclosed+label%3Abug).

![screenshot](documentation/gh/bugs.png)

### Unfixed Bugs

[![GitHub issue custom search](https://img.shields.io/github/issues-search/Gary-Burke/bake_my_cake?query=is%3Aissue%2Bis%3Aopen%2Blabel%3Abug&label=Unfixed%20Bugs&color=red)](https://www.github.com/Gary-Burke/bake_my_cake/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

Any remaining open issues can be tracked [here](https://www.github.com/Gary-Burke/bake_my_cake/issues?q=is%3Aissue+is%3Aopen+label%3Abug).

> [!IMPORTANT]
To my knowledge there are no remaining bugs present in this project.

### Known Issues

- The project is designed to be responsive from `375px` and upwards, in line with the material taught on the course LMS. Minor layout inconsistencies may occur on extra-wide (e.g. 4k/8k monitors), or smart-display devices (e.g. Nest Hub, Smart Watches, Gameboy Color, etc.), as these resolutions are outside the project’s scope, as taught by Code Institute.
- When validating HTML with a semantic `<section>` element, the validator warns about lacking a header `h2-h6`. This is acceptable.
- Validation errors on "signup.html" coming from the Django Allauth package.
- If a product is in your basket, but then gets deleted from the database, it throws errors from the session storage memory.
