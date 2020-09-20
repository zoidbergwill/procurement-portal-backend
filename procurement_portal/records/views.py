from django.views import generic
from rest_framework import generics as drf_generics
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PurchaseRecordSerializer
from . import models
from .filters import FullTextSearchFilter, FacetFieldFilter
from django.db.models import F


class Index(generic.TemplateView):
    template_name = "records/index.html"


class PurchaseRecordView(drf_generics.ListAPIView):
    queryset = models.PurchaseRecord.objects.filter(
        dataset_version=F("dataset_version__dataset__current_version")
    )
    serializer_class = PurchaseRecordSerializer
    filter_backends = [FullTextSearchFilter, FacetFieldFilter]
    facet_filter_fields = [
        "buyer_name",
        "implementation_location_district_municipality",
        "implementation_location_local_municipality",
        "implementation_location_facility",
        "implementation_location_other",
        "dataset_version__dataset__name",
    ]
    full_text_filter_fields = [
        "supplier_full_text",
        "directors_full_text",
        "description_full_text",
        "procurement_method_full_text",
    ]

    def __init__(self, *args, **kwargs):
        super(PurchaseRecordView, self).__init__(*args, **kwargs)
        self.facets = {}

    def list(self, request, *args, **kwargs):
        result = super(PurchaseRecordView, self).list(request, *args, **kwargs)
        result.data["meta"] = {"facets": self.facets}
        return result
