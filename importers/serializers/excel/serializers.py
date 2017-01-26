import pandas as pd
import pytz
import re
from decimal import Decimal
from django.db.models import Q
from numpy import dtype

from apis.betterself.v1.adapters import BetterSelfAPIAdapter
from events.models import SupplementEvent
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement


class ExcelFileSerializer(object):
    def __init__(self, file_path, user, ignore_columns=None, sheet=None):
        self.file_path = file_path
        # Sheet1 is default name for xlsx files
        self.sheet = sheet if sheet else 'Sheet1'

        ignore_columns = ignore_columns if ignore_columns else []
        self.ignore_columns = ignore_columns

        # use an adapter instead to create / query all the get / post API
        # seems like a huge pain considering we could just use native django save/create/query
        # but using this and making sure there are no bugs is better than having
        # real users face issues
        self.adapter = BetterSelfAPIAdapter(user)

    def get_sanitized_dataframe(self, date_column='Date'):
        # ExcelFile does not handle file_paths very well, use native Python open
        opened_file = open(self.file_path, 'rb')
        excel_file = pd.ExcelFile(opened_file)
        dataframe = excel_file.parse(self.sheet)

        # Sanitize so the inputs are correct and remove fluke days
        dataframe = self._sanitize_sheet(dataframe)
        dataframe = self._set_dataframe_index(dataframe, date_column)
        return dataframe

    @staticmethod
    def _sanitize_dataframe_values(dataframe):
        dataframe = dataframe.replace('T', 1)
        dataframe = dataframe.replace('t', 1)
        dataframe = dataframe.replace('True', 1)
        dataframe = dataframe.replace('true', 1)

        dataframe = dataframe.replace('F', 0)
        dataframe = dataframe.replace('f', 0)
        dataframe = dataframe.replace('False', 0)
        dataframe = dataframe.replace('false', 0)

        dataframe = dataframe.fillna(0)
        return dataframe

    @staticmethod
    def _set_dataframe_index(dataframe, date_column):
        dataframe = dataframe.set_index(dataframe[date_column])

        # drop duplicate since its now the index
        dataframe = dataframe.drop(date_column, axis=1)
        return dataframe

    def _sanitize_sheet(self, dataframe):
        dataframe = self.sanitize_dataframe_columns(dataframe, ignore_columns=self.ignore_columns)
        dataframe = self._sanitize_dataframe_values(dataframe)
        return dataframe

    @classmethod
    def _get_stripped_column_headers(cls, dataframe):
        """Return a k/v of crappy columns names without crappy spaces"""
        revised_columns = [item.strip() for item in dataframe.columns]
        updated_columns = dict(zip(dataframe.columns, revised_columns))

        return updated_columns

    @classmethod
    def sanitize_dataframe_columns(cls, dataframe, ignore_columns=None):
        ignore_columns = ignore_columns if ignore_columns else []

        revised_columns = cls._get_stripped_column_headers(dataframe)
        dataframe = dataframe.rename(columns=revised_columns)

        # for all the ignore columns (ie. non - supplement event stuff
        # disregard it)
        dataframe = dataframe.drop(ignore_columns, axis=1)

        return dataframe


class ExcelSupplementFileSerializer(ExcelFileSerializer):
    """Take a raw historical excel of supplements, clean and save it"""

    TEMPLATE_SAVE_MODEL = SupplementEvent
    SUPPLEMENT_UUID_CACHE = {}  # use it to match any supplement_name to a product
    source = 'user_excel'

    @staticmethod
    def _get_measurement_and_quantity_from_name(name):
        # figure out that Advil (200mg) means 200 mg
        result = {
            # throw a default quantity of 1 since that's that model has stored as default
            'quantity': 1,
        }

        name_no_spaces = name.replace(' ', '')
        # so for a value like Advil (200mg) anything with a parenthesis means
        # it stores some type of meta information we want to extract. if
        # we can't find anything like that, scrap it.
        regex_match_with_parenthesis = re.search('(?<=\()\w+', name_no_spaces)
        if not regex_match_with_parenthesis:
            return result

        regex_match_with_parenthesis = regex_match_with_parenthesis.group(0)
        quantity = re.search('\d+', regex_match_with_parenthesis)
        if quantity:
            result['quantity'] = int(quantity.group(0))

        measurement = re.search('[a-z]+', regex_match_with_parenthesis)
        if measurement:
            measurement_name = measurement.group(0)
            measurement_query = Measurement.objects.filter(
                Q(short_name=measurement_name) | Q(name=measurement_name))
            if measurement_query.exists():
                result['measurement_uuid'] = measurement_query[0].uuid

        return result

    @staticmethod
    def _parse_ingredient_from_column_entry(column_name):
        regex_match = re.search('^[A-Za-z0-9 ]+', column_name)

        # this cleans up situations where you had Theanine (150mg)
        first_match = regex_match.group(0)

        # this fixes situations where you had 'Theanine '
        first_match = first_match.strip()
        return first_match

    def _create_supplements_from_dataframe(self, dataframe):
        # problem with flat data structures is it's hard to transverse hierarchy
        # when you have no idea what users will input, so we're going to
        # create everything if it doesn't exist and then let a user rename
        # on the site

        for column_name in dataframe:
            # go from Tyrosine (500mg) to Tyrosine
            ingredient_name_parsed = self._parse_ingredient_from_column_entry(column_name)

            parameters = {'name': ingredient_name_parsed}

            ingredient = self.adapter.get_or_create_resource(Ingredient, parameters)
            ingredient_uuid = ingredient['uuid']

            ingredient_comp_parameters = self._get_measurement_and_quantity_from_name(column_name)
            ingredient_comp_parameters['ingredient_uuid'] = ingredient_uuid
            ingredient_composition = self.adapter.get_or_create_resource(
                IngredientComposition, ingredient_comp_parameters)

            # serializer is cool enough to take list or item
            parameters['ingredient_compositions_uuids'] = ingredient_composition['uuid']

            supplement = self.adapter.get_or_create_resource(Supplement, parameters)

            # add to cache, so don't have to deal with flattening to search
            # when saving individual events
            self.SUPPLEMENT_UUID_CACHE[column_name] = supplement['uuid']

    def save_results(self, dataframe):

        self._create_supplements_from_dataframe(dataframe)

        # events should only consist of numeric values, ie. 1 serving of caffeine ...
        dataframe_dtypes_dict = dataframe.dtypes.to_dict()
        valid_dataframe_columns = [k for k, v in dataframe_dtypes_dict.items() if v == dtype('float64')]

        valid_dataframe = dataframe[valid_dataframe_columns]

        for index, event in valid_dataframe.iterrows():
            for supplement_name, quantity in event.iteritems():
                # don't include any zero events
                if quantity == Decimal(0):
                    continue

                supplement_uuid = self.SUPPLEMENT_UUID_CACHE[supplement_name]

                time = index

                # localize and make as UTC time
                user_timezone = pytz.timezone(self.adapter.user.timezone)
                localized_time = user_timezone.localize(time)

                supplement_event_parameters = {
                    'supplement_uuid': supplement_uuid,
                    'time': localized_time,
                    'source': self.source,
                    'quantity': quantity
                }

                self.adapter.get_or_create_resource(SupplementEvent, supplement_event_parameters)


class ExcelProductiveFileSerializer(ExcelFileSerializer):
    source = 'user_excel'

    def save_results(self, dataframe):
        # productivity (at least from RescueTime) is only measured in minutes, so these are automatically
        # typecasted to int64
        dataframe_dtypes_dict = dataframe.dtypes.to_dict()
        valid_dataframe_columns = [k for k, v in dataframe_dtypes_dict.items() if v == dtype('int64')]
        valid_dataframe = dataframe[valid_dataframe_columns]

        distracting_time_col_key = 'Distracting Time (Minutes)'
        productive_time_col_key = 'Productivity Time (Minutes)'

        print(valid_dataframe[distracting_time_col_key])
        print(valid_dataframe[productive_time_col_key])
