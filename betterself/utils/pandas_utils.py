import pandas as pd

from betterself.utils.date_utils import get_current_userdate


def get_complete_date_range_series_container(user, start_date, end_date):
    localized_index = pd.to_datetime([start_date, end_date])
    # create a series includes the parameter's start and end dates
    # do this to allow API requests for charts to be certain they are dealing with the same X axis
    series = pd.Series(index=localized_index).asfreq('D').tz_localize(user.pytz_timezone)
    return series


def force_start_end_date_to_series(user, series, start_date, end_date):
    # because you mess this up a bit working with dataframes
    assert type(series) == pd.Series

    # if the series contains any results outside the start and end date ... those should be definitely excluded
    series = series[start_date:end_date]

    series_container = get_complete_date_range_series_container(user, start_date, end_date)

    # now take the index of valid results and put it in the container if it exists
    series_container.ix[series.index] = series
    return series_container


def force_start_end_data_to_dataframe(user, dataframe, start_date, end_date):
    assert type(dataframe) == pd.DataFrame

    # if dataframe contains any dates outside of start and end date ... exclude
    dataframe = dataframe[start_date:end_date].asfreq('D')

    index = pd.date_range(start=start_date, end=end_date, tz=user.pytz_timezone)

    # blank dataframe that we know for certain holds all the right dates
    dataframe_container = pd.DataFrame(index=index)

    # join the dataframe with an empty one that has all the right indices ... to return a dataframe with all the right
    # start and end dates
    normalized_dataframe = pd.DataFrame.join(dataframe_container, dataframe)

    # Pandas is like a fine edged sword, sometimes it cuts everything perfectly, other times you don't know it's
    # power and it claws at you and takes back the bamboo. For the record, problem is not the panda, but the trainer.
    assert dataframe_container.index.size == normalized_dataframe.index.size

    return normalized_dataframe


def get_empty_timezone_aware_series_containing_index_of_today(user):
    # dataframes dont concat well with different timezones ... so we always need to have a series of a empty timezone
    # otherwise, a series without a timezone always will fail
    user_now = get_current_userdate(user)
    index = pd.DatetimeIndex(tz=user.pytz_timezone, freq='D', end=user_now, periods=1)
    return index
