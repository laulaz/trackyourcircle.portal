from zope.interface import implementer
from plone.dexterity.content import Item 
from collective.geolocationbehavior.geolocation import IGeolocatable

from .interfaces import ICircle
from .interfaces import ICircleDate


@implementer(ICircle)
class Circle(Item):
    """Convenience subclass for ``Circle`` portal type
    """
