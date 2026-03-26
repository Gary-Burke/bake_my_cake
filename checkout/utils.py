import json
from datetime import date, timedelta
from django.db.models import Count
from .models import DeliveryDate

MIN_DATE = 3
MAX_DATE = 90
CAPACITY = 5


def get_dates():
    """
    Function to determine fully booked dates in the database
    Send min date, max date and dates not allowed, e.g. fully booked dates
    to the view. The view passes this to HTML and is used by JS to update
    flatpickr calendar
    """

    today = date.today()
    min_date_val = today + timedelta(days=MIN_DATE)
    max_date_val = today + timedelta(days=MAX_DATE)

    # Find dates within the selectable window that have reached capacity
    # Used Claude.ai for this solution
    full_dates = (
        DeliveryDate.objects.filter(
            date__gte=min_date_val,
            date__lte=max_date_val,
        )
        .annotate(order_count=Count("orders_date"))
        .filter(order_count__gte=CAPACITY)
        .values_list("date", flat=True)
    )

    dates_not_allowed = json.dumps(
        [d.strftime("%Y-%m-%d") for d in full_dates]
    )

    return {
        "min_date": MIN_DATE,
        "max_date": MAX_DATE,
        "dates_not_allowed": dates_not_allowed,
    }
