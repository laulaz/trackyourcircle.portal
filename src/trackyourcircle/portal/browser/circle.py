from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import json

from zope import schema
from zope.i18n import translate

from plone import api
from zope.interface import Interface
from z3c.form import button
from z3c.form import form
from zope.interface import implementer
from z3c.form.interfaces import IFieldsAndContentProvidersForm
from z3c.form.contentprovider import ContentProviders
from zope.contentprovider.provider import ContentProviderBase
from plone.autoform.form import AutoExtensibleForm
from plone.formwidget.geolocation.field import GeolocationField

from trackyourcircle.portal import _


class FacetedGeoJSONPopup(BrowserView):
    index = ViewPageTemplateFile("circle-popup.pt")

    render = index


class IViewCircle(Interface):
    pass


class ISearchCircle(Interface):
    """ Define form fields """

    city = schema.TextLine(
        title=_('label_city', default=u'City'),
        required=True)

    location = schema.TextLine(
        title=_('label_location', default=u'Location'),
        required=False)


class IAddCircle(ISearchCircle):
    geolocation = GeolocationField(
        title=_('label_geolocation', default=u'Geolocation'),
        description=_('help_geolocation',
                      default=u'Click on the map to select a location, or '
                              u'use the text input to search by address.'),
        required=True)


class ViewHelp(ContentProviderBase):
    render = ViewPageTemplateFile("view-circle-help.pt")


class AddHelp(ContentProviderBase):
    render = ViewPageTemplateFile("add-circle-help.pt")


class SearchHelp(ContentProviderBase):
    render = ViewPageTemplateFile("search-circle-help.pt")


class JS(ContentProviderBase):
    render = ViewPageTemplateFile("add-circle-js.pt")


class SearchCircleMap(ContentProviderBase):
    render = ViewPageTemplateFile("circle-search-map.pt")

    @property
    def map_configuration(self):
        map_layers = api.portal.get_registry_record("geolocation.map_layers") or []
        config = {
            "fullscreencontrol": api.portal.get_registry_record(
                "geolocation.fullscreen_control", default=True
            ),
            "locatecontrol": api.portal.get_registry_record(
                "geolocation.locate_control", default=True
            ),
            "zoomcontrol": api.portal.get_registry_record(
                "geolocation.zoom_control", default=True
            ),
            "minimap": api.portal.get_registry_record(
                "geolocation.show_minimap", default=True
            ),
            "addmarker": api.portal.get_registry_record(
                "geolocation.show_add_marker", default=False
            ),
            "geosearch": api.portal.get_registry_record(
                "geolocation.show_geosearch", default=False
            ),
            "geosearch_provider": api.portal.get_registry_record(
                "geolocation.geosearch_provider", default=[]
            ),
            "default_map_layer": api.portal.get_registry_record(
                "geolocation.default_map_layer", default=[]
            ),
            "map_layers": [
                {"title": translate(_(l), context=self.request), "id": l}
                for l in map_layers
            ],
            "useCluster": False,
        }
        return json.dumps(config)


class SearchCircleResults(ContentProviderBase):
    render = ViewPageTemplateFile("circle-search-results.pt")

    def batch(self):
       return self.context.portal_catalog(portal_type='Circle')


@implementer(IFieldsAndContentProvidersForm)
class ViewCircle(AutoExtensibleForm, form.AddForm):

    schema = IViewCircle
    ignoreContext = True
    contentProviders = ContentProviders()
    contentProviders['longHelp'] = ViewHelp
    contentProviders['longHelp'].position = 0
    contentProviders['searchCircleResults'] = SearchCircleResults
    contentProviders['searchCircleResults'].position = 4
    contentProviders['searchCircleMap'] = SearchCircleMap
    contentProviders['searchCircleMap'].position = 5
    contentProviders['js'] = JS
    contentProviders['js'].position = 6

    @button.buttonAndHandler(_(u"Search Circle"))
    def handleSearch(self, action):
        self.request.response.redirect(self.context.absolute_url() + '/search-circles')

    @button.buttonAndHandler(_(u"Add Circle"))
    def handleAdd(self, action):
        self.request.response.redirect(self.context.absolute_url() + '/search-circles')


@implementer(IFieldsAndContentProvidersForm)
class SearchCircle(AutoExtensibleForm, form.AddForm):

    schema = ISearchCircle
    ignoreContext = True
    contentProviders = ContentProviders()
    contentProviders['longHelp'] = SearchHelp
    contentProviders['longHelp'].position = 0
    contentProviders['searchCircleResults'] = SearchCircleResults
    contentProviders['searchCircleResults'].position = 4
    contentProviders['searchCircleMap'] = SearchCircleMap
    contentProviders['searchCircleMap'].position = 5
    contentProviders['js'] = JS
    contentProviders['js'].position = 6

    def update(self):
        super(SearchCircle, self).update()

    def updateWidgets(self, prefix=None):
        super(SearchCircle, self).updateWidgets(prefix)

    @button.buttonAndHandler(_(u"Search"))
    def handleSearch(self, action):
        pass

    @button.buttonAndHandler(_(u"Add missing Circle"))
    def handleAddMissing(self, action):
        data, errors = self.extractData()
        city = data['city']
        location = data['location']
        url = ( self.context.absolute_url() +
            '/add-circle?form.widgets.city=%s&form.widgets.location=%s' % (city, location)
        )
        self.request.response.redirect(url)
 
    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        self.request.response.redirect(self.context.absolute_url() + '/view-circles')


@implementer(IFieldsAndContentProvidersForm)
class AddCircle(AutoExtensibleForm, form.Form):
    allow_prefill_from_GET_request = True

    schema = IAddCircle
    ignoreContext = True
    contentProviders = ContentProviders()
    contentProviders['longHelp'] = AddHelp
    contentProviders['longHelp'].position = 0
    contentProviders['searchCircleResults'] = SearchCircleResults
    contentProviders['searchCircleResults'].position = 5
    contentProviders['js'] = JS
    contentProviders['js'].position = -1

    def update(self):
        super(AddCircle, self).update()

    def updateWidgets(self, prefix=None):
        super(AddCircle, self).updateWidgets(prefix)

    @button.buttonAndHandler(_(u"Save"))
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        title = data['city']
        if data['location']:
            title += " - " + data['location']
        circle = api.content.create(
            self.context, 
            "Circle", title=title, geolocation=data['geolocation'])
        api.content.transition(circle, 'publish')

        self.request.response.redirect(self.context.absolute_url() + '/view-circles')

    @button.buttonAndHandler(_(u"Search again"))
    def handleSearch(self, action):
        pass

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        self.request.response.redirect(self.context.absolute_url() + '/view-circles')

