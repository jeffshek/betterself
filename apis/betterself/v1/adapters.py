"""
This file inherits the spirit of an Amazon article I read a while back about
how much Amazon communicates via APIs of all their team / services ... it forces them
to make well-thought APIs. Since I have a bit of historical data from Excel that I'm
importing - I had two options. 1) Just use django's native methods (get_or_create, etc)
or 2) eat my own dog food and use post/puts to create the historical data. I've tested
1) and I know it works ... but I've decided to with option 2 since empirically a
battle-tested API will make the eventual iOS / Android apps much easier to develop.

https://plus.google.com/+RipRowan/posts/eVeouesvaVX Steve Yegge's Platform Rant
"""
import json

import logging
import requests

from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from django.conf import settings

logger = logging.getLogger(__name__)


class BetterSelfAPIAdapter(object):
    """
    Takes a user, retrieves the token and fetches RESTful endpoints for that user
    """

    def __init__(self, user):
        self.user = user
        self.api_token, _ = Token.objects.get_or_create(user=user)
        self.headers = {'Authorization': 'Token {}'.format(self.api_token.key)}

        # use to figure out how to prefix a resource endpoint
        # so it's either http://127.0.0.1:9000/ --- then api/v1/sleep, etc.
        self.domain = settings.API_ENDPOINT

    def fetch_resource_endpoint_url(self, resource):
        # just called fetch so no confusion with "get"
        url = reverse(resource.RESOURCE_NAME)
        return self.domain + url

    def _get_resource_response(self, resource, parameters=None):
        resource_endpoint = self.fetch_resource_endpoint_url(resource)
        # new_parameters = {'supplement_uuid': 'ba869beb-92cc-47ae-81d5-19f27e17b5e4'}
        # there is an issue here when fetching here that datetime won't work correctly with UTC
        # i'm not sure how to fix this just yet ....
        response = requests.get(resource_endpoint, params=parameters, headers=self.headers)

        return response

    def get_resource_data(self, resource, parameters=None):
        response = self._get_resource_response(resource, parameters)
        data = json.loads(response.text)
        return data

    def get_or_create_resource(self, resource, parameters=None, defaults=None):
        """
        TODO - This is being depreciated! Instead make sure that all resources that accept POST do the correct
        update_or_create.
        """
        if not parameters:
            parameters = []

        if not defaults:
            defaults = []

        if defaults:
            # if defaults are passed, try to get this resource based on the defaults this is prevent scenarios where
            # we are trying to get a resource based on optional fields so the get will say we have no record where row
            # with defaults A and optional argument B exist, but the check should really be JUST for the defaults
            # (what will fail when trying to enter in the database)
            get_parameters = {k: v for k, v in parameters.items() if k in defaults}
            data = self.get_resource_data(resource, get_parameters)

        else:
            data = self.get_resource_data(resource, parameters)

        if len(data) > 1:
            raise ValueError('Expected one object ... got two! {}'.format(data))
        elif len(data) == 1:
            serialized_data = data[0]
        elif not data:
            serialized_data = self.post_resource_data(resource, parameters)
        else:
            raise ValueError('Unexpected Resource Entity')

        return serialized_data

    def _post_resource_response(self, resource, parameters):
        resource_endpoint = self.fetch_resource_endpoint_url(resource)
        response = requests.post(resource_endpoint, data=parameters, headers=self.headers)
        return response

    def post_resource_data(self, resource, parameters):
        response = self._post_resource_response(resource, parameters)

        # some embarrassing testing to see why post requests are not working
        # if response.status_code >= 400:
        #     logger.error(response.text)

        data = json.loads(response.text)
        return data
