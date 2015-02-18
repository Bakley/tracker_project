from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin, JSONResponseMixin
from django.contrib.gis.geos import GEOSGeometry
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from geojson import FeatureCollection

from .forms import IncidentForm, AreaOfInterestForm
from .models import Incident, AreaOfInterest


class IncidentListOnSuccessMixin(object):
    def get_success_url(self):
        return reverse_lazy('tracker:incident-list')


class AreaOfInterestListOnSuccessMixin(object):
    def get_success_url(self):
        return reverse_lazy('tracker:area-of-interest-list')


class IncidentListView(LoginRequiredMixin, ListView):
    queryset = Incident.objects.all().order_by('-created')
incident_list = IncidentListView.as_view()


class IncidentDetailView(LoginRequiredMixin, DetailView):
    model = Incident
incident_detail = IncidentDetailView.as_view()


class IncidentCreateView(LoginRequiredMixin, IncidentListOnSuccessMixin, CreateView):
    model = Incident
    form_class = IncidentForm

    def form_valid(self, form):
        form.instance.location = GEOSGeometry(form.cleaned_data['location_geojson'])

        return super(IncidentCreateView, self).form_valid(form)
incident_create = IncidentCreateView.as_view()


class IncidentUpdateView(LoginRequiredMixin, IncidentListOnSuccessMixin, UpdateView):
    model = Incident
    form_class = IncidentForm

    def get_initial(self):
        initial = super(IncidentUpdateView, self).get_initial()

        initial['location_geojson'] = self.get_object().location.geojson

        return initial

    def form_valid(self, form):
        form.instance.location = GEOSGeometry(form.cleaned_data['location_geojson'])

        return super(IncidentUpdateView, self).form_valid(form)
incident_update = IncidentUpdateView.as_view()


class IncidentDeleteView(LoginRequiredMixin, IncidentListOnSuccessMixin, DeleteView):
    model = Incident
incident_delete = IncidentDeleteView.as_view()


class AreaOfInterestListView(LoginRequiredMixin, ListView):
    model = AreaOfInterest
area_of_interest_list = AreaOfInterestListView.as_view()


class AreaOfInterestDetailView(LoginRequiredMixin, DetailView):
    model = AreaOfInterest
area_of_interest_detail = AreaOfInterestDetailView.as_view()


class AreaOfInterestCreateView(LoginRequiredMixin, AreaOfInterestListOnSuccessMixin, CreateView):
    model = AreaOfInterest
    form_class = AreaOfInterestForm

    def form_valid(self, form):
        form.instance.polygon = GEOSGeometry(form.cleaned_data['polygon_geojson'])

        return super(AreaOfInterestCreateView, self).form_valid(form)
area_of_interest_create = AreaOfInterestCreateView.as_view()


class AreaOfInterestUpdateView(LoginRequiredMixin, AreaOfInterestListOnSuccessMixin, UpdateView):
    model = AreaOfInterest
    form_class = AreaOfInterestForm

    def get_initial(self):
        initial = super(AreaOfInterestUpdateView, self).get_initial()

        initial['polygon_geojson'] = self.get_object().polygon.geojson

        return initial

    def form_valid(self, form):
        form.instance.polygon = GEOSGeometry(form.cleaned_data['polygon_geojson'])

        return super(AreaOfInterestUpdateView, self).form_valid(form)
area_of_interest_update = AreaOfInterestUpdateView.as_view()


class AreaOfInterestDeleteView(LoginRequiredMixin, AreaOfInterestListOnSuccessMixin, DeleteView):
    model = AreaOfInterest
area_of_interest_delete = AreaOfInterestDeleteView.as_view()


class IncidentFeatureCollectionView(LoginRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        features = [incident.geojson_feature for incident in Incident.objects.filter(closed=False)]
        feature_collection = FeatureCollection(features)

        return self.render_json_response(feature_collection)
incident_feature_collection = IncidentFeatureCollectionView.as_view()


class AreaOfInterestFeatureCollectionView(LoginRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        features = [
            area_of_interest.geojson_feature for area_of_interest in AreaOfInterest.objects.all()
        ]
        feature_collection = FeatureCollection(features)

        return self.render_json_response(feature_collection)
area_of_interest_feature_collection = AreaOfInterestFeatureCollectionView.as_view()