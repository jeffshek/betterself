from apis.betterself.v1.utils.views import UserQuerysetFilterMixin, BaseGenericListCreateAPIViewV1


class SupplementEventSerializer(BaseGenericListCreateAPIViewV1, UserQuerysetFilterMixin):
    pass
