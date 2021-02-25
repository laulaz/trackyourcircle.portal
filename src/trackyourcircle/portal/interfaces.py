# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
import zope.schema


class ITrackYourCirclePortalLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICircle(Interface):
    """Explicit marker interface for Circle
    """
