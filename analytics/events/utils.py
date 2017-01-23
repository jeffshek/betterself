import pandas as pd

SOURCE_COLUMN_NAME = 'Source'
QUANTITY_COLUMN_NAME = 'Quantity'
SUPPLEMENT_COLUMN_NAME = 'Supplement'
TIME_COLUMN_NAME = 'Time'

SupplementEventColumnMapping = {
    'source': SOURCE_COLUMN_NAME,
    'supplement__name': SUPPLEMENT_COLUMN_NAME,
    'quantity': QUANTITY_COLUMN_NAME,
    'time': TIME_COLUMN_NAME,
}


class SupplementEventsDataframeBuilder(object):
    """
    Builds a pandas dataframe from a SupplementEvent queryset ... once we get to a dataframe
    analytics are just super easy to work with and we can do a lot of complex analysis on top of it
    """

    def __init__(self, queryset):
        queryset = queryset.select_related('supplement')
        self.queryset = queryset
        values_columns = SupplementEventColumnMapping.keys()
        self.values = self.queryset.values(*values_columns)

    def build_dataframe(self):
        # Am I really a programmer or just a lego assembler?
        # Pandas makes my life at least 20 times easier.
        # Easiest one liner ever.
        df = pd.DataFrame.from_records(self.values, index='time')

        # make the columns and labels prettier
        df = df.rename(columns=SupplementEventColumnMapping)
        df.index.name = TIME_COLUMN_NAME

        return df

    def build_dataframe_grouped_daily(self):
        df = self.build_dataframe()
        # can't really aggregate source (str) over a day, so drop it
        # otherwise we see BCAABCAABCAABCAABCAABCAABCAABCAABCAABCAA
        df = df.drop(SOURCE_COLUMN_NAME, axis=1)

        # first group by Supplement, ie. so that
        # BCAA / Creatine are separately. Then resample
        # the index to a Daily amount and sum it
        daily_df = df.groupby('Supplement').resample('D').sum()

        return daily_df

    # def build_flattened_daily_dataframe(self):
    #     """
    #     Construct a dataframe that's index is daily with the columns
    #     being all the different Supplements that were taken.
    #
    #     This is the bread / butter of what powers a lot of the initial
    #     analytics
    #     """
    #     df = self.build_dataframe()
    #     df = df.drop(SOURCE_COLUMN_NAME, axis=1)
    #     # TODO - not quite done yet
    #     return df
