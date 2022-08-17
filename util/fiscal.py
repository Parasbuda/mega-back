import datetime
import nepali_datetime


def get_financial_year_ad(dateObj):

    year_ad = dateObj.year
    month_ad = dateObj.month
    day_ad = dateObj.day
    date_ad_obj = datetime.date(year_ad, month_ad, day_ad)

    current_year = date_ad_obj.year

    financial_year_date = str(current_year) + "-04-01"
    financial_year_date_obj = datetime.datetime.strptime(
        financial_year_date, "%Y-%m-%d"
    ).date()
    if date_ad_obj < financial_year_date_obj:
        return str(current_year - 1) + "/" + str(current_year)
    else:
        return str(current_year) + "/" + str(current_year + 1)


def get_financial_year_bs(dateObj):
    year_ad = dateObj.year
    month_ad = dateObj.month
    day_ad = dateObj.day
    date_ad_obj = datetime.date(year_ad, month_ad, day_ad)
    nepali_date = nepali_datetime.date.from_datetime_date(date_ad_obj)
    nepali_year = nepali_date.year
    fiscal_year_nepali = str(nepali_year) + "-4-01"
    fiscal_year_nepali_obj = nepali_datetime.datetime.strptime(
        fiscal_year_nepali, "%Y-%m-%d"
    ).date()
    if nepali_date < fiscal_year_nepali_obj:
        return str(nepali_year - 1) + "/" + str(nepali_year)
    else:
        return str(nepali_year) + "/" + str(nepali_year + 1)
