import re
import pandas as pd

from django.core.management import CommandError
from django.db.models import Q

from events.models import SupplementProductEventComposition
from supplements.models import Ingredient, IngredientComposition, SupplementProduct, MeasurementUnit


class ExcelFileSanitizer(object):
    IGNORE_COLUMNS = []

    def __init__(self, file_path, user, sheet=None):
        self.file_path = file_path
        # Sheet1 is default name for xlsx files
        self.sheet = sheet if sheet else 'Sheet1'
        self.user = user

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
        dataframe = dataframe.fillna(0)
        return dataframe

    @staticmethod
    def _set_dataframe_index(dataframe, date_column):
        dataframe = dataframe.set_index(dataframe[date_column])

        # drop duplicate since its now the index
        dataframe = dataframe.drop(date_column, axis=1)
        return dataframe

    def _sanitize_sheet(self, dataframe):
        dataframe = self._sanitize_dataframe_columns(dataframe)
        dataframe = self._sanitize_dataframe_values(dataframe)
        return dataframe

    @classmethod
    def _get_cleaned_column_headers(cls, dataframe):
        """Return a k/v of crappy columns names without crappy spaces"""
        revised_columns = [item.strip() for item in dataframe.columns]
        updated_columns = dict(zip(dataframe.columns, revised_columns))
        return updated_columns

    def _sanitize_dataframe_columns(self, dataframe):
        revised_columns = self._get_cleaned_column_headers(dataframe)
        dataframe = dataframe.rename(columns=revised_columns)

        for column in self.IGNORE_COLUMNS:
            dataframe = dataframe.drop(column, axis=1)

        return dataframe


class SupplementSanitizerTemplate(ExcelFileSanitizer):
    """Take a raw historical excel of supplements, clean and save it"""

    TEMPLATE_SAVE_MODEL = SupplementProductEventComposition
    SUPPLEMENT_PRODUCT_CACHE = {}  # use it to match any supplement_name to a product

    @staticmethod
    def get_measurement_unit_and_quantity_from_name(name):
        # figure out that Advil (200mg) means 200 mg
        result = {
            'measurement_unit': None,
            'quantity': None,
        }

        # make my regex life easier
        name_no_spaces = name.replace(" ", "")
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
            measurement_query = MeasurementUnit.objects.filter(Q(short_name=measurement_name) | Q(name=measurement_name))
            if measurement_query.exists():
                result['measurement_unit'] = measurement_query[0]

        return result

    def create_supplement_products_from_dataframe(self, dataframe):
        # problem with flat data structures is it's hard to transverse hierarchy
        # when you have no idea what users will input, so we're going to
        # create everything if it doesn't exist and then let a user rename
        # on the site

        # if you're putting more than 30 supplements from a spreadsheet
        # i don't trust you. this prevents user error from uploading
        # an absurd amount of supplements.
        if len(dataframe) > 30:
            raise CommandError("Too many columns inserted. Please contact an admin.")

        for supplement_name in dataframe:  # a list of dataframe columns
            ingredient = Ingredient.get_or_create(
                name=supplement_name,
                user=self.user
            )

            ingredient_comp_details = self.get_measurement_unit_and_quantity_from_name(supplement_name)
            ingredient_comp = IngredientComposition.get_or_create(
                ingredient=ingredient,
                user=self.user,
                **ingredient_comp_details
            )

            supplement = SupplementProduct.get_or_create(
                name=supplement_name,
                user=self.user
            )

            supplement.ingredient_composition = [ingredient_comp]
            supplement.save()

            # add to cache, so don't have to deal with flattening to search
            # when saving individual events
            self.SUPPLEMENT_PRODUCT_CACHE[supplement_name] = supplement

    def save_results(self, dataframe):
        self.create_supplement_products_from_dataframe(dataframe)
        for _, event in dataframe.iterrows():
            continue


# TD - Check Django default values for atomic transactions in 1.9
# - Is there a library to prevent sql injection?
