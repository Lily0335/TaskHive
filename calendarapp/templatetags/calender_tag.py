import calendar
from datetime import date
from django import template

register = template.Library()

@register.filter
def month_calendar(current_date):
    year = current_date.year
    month = current_date.month
    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    return cal.monthdatescalendar(year, month)
