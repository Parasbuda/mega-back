import datetime
import nepali_datetime


def bs_date(dateObj):
    year_ad = dateObj.year
    month_ad = dateObj.month
    day_ad = dateObj.day
    date_ad_obj = datetime.date(year_ad, month_ad, day_ad)
    date_bs = nepali_datetime.date.from_datetime_date(date_ad_obj)
    return date_bs
