import json
from datetime import date, timedelta
from django.db.models import Count
from .models import DeliveryDate

MIN_DATE = 3
MAX_DATE = 120
CAPACITY = 5


def get_dates():
    """
    Function to determine fully booked dates in the database.
    Send min date, max date and dates not allowed to the view.
    The view passes this data to the template and is used by
    jQuery to update the flatpickr calendar.
    """

    today = date.today()
    year = date.today().year
    min_date_val = today + timedelta(days=MIN_DATE)
    max_date_val = today + timedelta(days=MAX_DATE)

    # Find dates within the selectable window that have reached capacity
    # Used Claude.ai for this solution of full_dates
    full_dates = (
        DeliveryDate.objects.filter(
            date__gte=min_date_val,
            date__lte=max_date_val,
        )
        .annotate(order_count=Count("orders_date"))
        .filter(order_count__gte=CAPACITY)
        .values_list("date", flat=True)
    )

    # A list for all days not available to customers
    # starting the string with all the fully booked days
    dates_not_allowed_list = [d.strftime("%Y-%m-%d") for d in full_dates]

    # Add Sundays
    current = min_date_val
    while current <= max_date_val:
        if current.weekday() == 6:  # 6 = Sunday
            dates_not_allowed_list.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    # Festive Seasons / Holidays like Christmas and New Years
    holidays = [
        f"{year}-12-25", f"{year}-12-26", f"{year}-12-31", f"{year+1}-01-01"
    ]

    dates_not_allowed_list.extend(holidays)

    # Convert list to set to remove duplicates then convert back to list
    # in order to convert to json string with json.dumps for template/jQuery
    dates_not_allowed = json.dumps(list(set(dates_not_allowed_list)))

    return {
        "min_date": MIN_DATE,
        "max_date": MAX_DATE,
        "dates_not_allowed": dates_not_allowed,
    }
