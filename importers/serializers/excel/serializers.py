import pandas as pd
import pytz
import re
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

    @classmethod
    def _sanitize_sheet(cls, dataframe):
        dataframe = cls.sanitize_dataframe_columns(dataframe)
        dataframe = cls._sanitize_dataframe_values(dataframe)
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

        for column in ignore_columns:
            dataframe = dataframe.drop(column, axis=1)

        return dataframe


class ExcelSupplementFileSerializer(ExcelFileSerializer):
    """Take a raw historical excel of supplements, clean and save it"""

    TEMPLATE_SAVE_MODEL = SupplementEvent
    SUPPLEMENT_CACHE = {}  # use it to match any supplement_name to a product

    @staticmethod
    def get_measurement_and_quantity_from_name(name):
        # figure out that Advil (200mg) means 200 mg
        result = {
            'measurement': None,
        }

        # make my regex life easier
        name_no_spaces = name.replace(' ', '')
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
                result['measurement'] = measurement_query[0]

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
            ingredient_parsed = self._parse_ingredient_from_column_entry(column_name)

            ingredient, _ = Ingredient.objects.get_or_create(
                name=ingredient_parsed,
                user=self.user
            )

            ingredient_comp_details = self.get_measurement_and_quantity_from_name(column_name)

            ingredient_comp, _ = IngredientComposition.objects.get_or_create(
                ingredient=ingredient, user=self.user, **ingredient_comp_details)

            supplement, _ = Supplement.objects.get_or_create(
                name=ingredient_parsed,
                user=self.user
            )

            supplement.ingredient_composition = [ingredient_comp]
            supplement.save()

            # add to cache, so don't have to deal with flattening to search
            # when saving individual events
            self.SUPPLEMENT_CACHE[column_name] = supplement

    def save_results(self, dataframe):
        # potentially consider making this into its own DataframeImporter file
        # kind of seems like it should, but also kind of feels like overkill
        source = 'user_excel'

        self._create_supplements_from_dataframe(dataframe)

        # events should only consist of numeric values, ie. 1 serving of caffeine ...
        dataframe_dtypes_dict = dataframe.dtypes.to_dict()
        valid_dataframe_columns = [k for k, v in dataframe_dtypes_dict.items() if v == dtype('float64')]

        valid_dataframe = dataframe[valid_dataframe_columns]

        for index, event in valid_dataframe.iterrows():
            for supplement_name, quantity in event.iteritems():
                supplement = self.SUPPLEMENT_CACHE[supplement_name]

                time = index

                # localize and make as UTC time
                time = pytz.utc.localize(time, pytz.UTC)

                self.TEMPLATE_SAVE_MODEL.objects.get_or_create(
                    user=self.user,
                    supplement=supplement,
                    time=time,
                    quantity=quantity,
                    source=source
                )
