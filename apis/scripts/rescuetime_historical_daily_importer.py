import requests
from django.conf import settings

# No nesting allowed!
# Really annoying aspect of runscript is it only runs from app/scripts folder

RT_API_KEY = settings.RESCUETIME_API_KEY
RT_API_URL = 'https://www.rescuetime.com/anapi/daily_summary_feed'
# RT_API_URL = 'https://www.rescuetime.com/anapi/data'


def run(*args):
    # Used as a simple way to see your own scores from RescueTime
    # and do aggregate analysis on it

    parameters = {
        'key': RT_API_KEY,
    }

    result = requests.get(RT_API_URL, data=parameters)

    print('Date | Percentage | Productive Time | Distracting Time')

    json_data = result.json()
    json_data.reverse()

    for detail in json_data:
        detail_date = detail['date']

        # this API is surprisingly easy to use.
        detail_very_productive_time = detail['very_productive_duration_formatted']
        all_distracting_time = detail['all_distracting_duration_formatted']
        productive_percentage = detail['all_productive_percentage']

        print ('{date} | {percentage} | {productive_time} | {distracting_time}'.format(
            date=detail_date,
            percentage=productive_percentage,
            productive_time=detail_very_productive_time,
            distracting_time=all_distracting_time
        ))
