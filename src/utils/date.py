from datetime import datetime, timedelta

get_yesterday_date = lambda: (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
