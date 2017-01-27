import numpy as np
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

VERY_PRODUCTIVE_TIME_LABEL = 'Very Productive Minutes'
PRODUCTIVE_TIME_LABEL = 'Productive Minutes'
NEUTRAL_TIME_LABEL = 'Neutral Minutes'
DISTRACTING_TIME_LABEL = 'Distracting Minutes'
VERY_DISTRACTING_TIME_LABEL = 'Very Distracting Minutes'
DATE_LABEL = 'Date'

ProductivityLogEventColumnMapping = {
    'source': SOURCE_COLUMN_NAME,
    'date': DATE_LABEL,
    'very_productive_time_minutes': VERY_PRODUCTIVE_TIME_LABEL,
    'productive_time_minutes': PRODUCTIVE_TIME_LABEL,
    'neutral_time_minutes': NEUTRAL_TIME_LABEL,
    'distracting_time_minutes': DISTRACTING_TIME_LABEL,
    'very_distracting_time_minutes': VERY_DISTRACTING_TIME_LABEL,

}


class DataFrameBuilder(object):
    def build_dataframe(self):
        # Am I really a programmer or just a lego assembler?
        # Pandas makes my life at least 20 times easier.
        df = pd.DataFrame.from_records(self.values, index=self.index_column)

        # make the columns and labels prettier
        df = df.rename(columns=self.column_mapping)
        df.index.name = TIME_COLUMN_NAME

        return df


class SupplementEventsDataframeBuilder(DataFrameBuilder):
    """
    Builds a pandas dataframe from a SupplementEvent queryset ... once we get to a dataframe
    analytics are just super easy to work with and we can do a lot of complex analysis on top of it
    """
    index_column = 'time'
    column_mapping = SupplementEventColumnMapping

    def __init__(self, queryset):
        queryset = queryset.select_related('supplement')
        self.queryset = queryset
        values_columns = self.column_mapping.keys()
        self.values = self.queryset.values(*values_columns)

    def build_flat_dataframe(self):
        """
        Return a flattened view of all the supplements that were taken
        """
        df = self.build_dataframe()

        # use a pivot_table and not a pivot because duplicates should be summed
        # should there be duplicates though? ie. would anyone ever record
        # taking two BCAAs at the same time??
        flat_df = df.pivot_table(
            index=df.index,
            values=QUANTITY_COLUMN_NAME,
            columns=SUPPLEMENT_COLUMN_NAME,
            aggfunc=np.sum
        )
        return flat_df


class ProductivityLogEventsDataframeBuilder(DataFrameBuilder):
    index_column = 'date'
    column_mapping = ProductivityLogEventColumnMapping

    def __init__(self, queryset):
        self.queryset = queryset
        values_columns = self.column_mapping.keys()
        self.values = self.queryset.values(*values_columns)

    def get_productive_timeseries(self):
        df = self.build_dataframe()

        # get a list of the columns that indicate productivity
        # in the future, potentially weight these differently
        productive_columns = [item for item in df.keys() if 'Productive' in item]
        productive_df = df[productive_columns]

        # now sum all the columns together to get a sum of collective periods
        productive_timeseries = productive_df.sum(axis=1)

        return productive_timeseries
