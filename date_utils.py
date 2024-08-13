from datetime import datetime, timedelta
import calendar

get_yesterday_date = lambda: (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def six_months_ago_monday():
    today = datetime.today()
    six_months_ago = today - timedelta(days=6*30)
    first_of_month = six_months_ago.replace(day=1)
    days_until_monday = (calendar.MONDAY - first_of_month.weekday() + 7) % 7
    next_monday = first_of_month + timedelta(days=days_until_monday)
    return next_monday.strftime('%Y-%m-%d')