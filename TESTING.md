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