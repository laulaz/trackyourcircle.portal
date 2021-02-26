from plone.dexterity.content import Item
from zope.interface import implementer

from .interfaces import ICircle


@implementer(ICircle)
class Circle(Item):
    """Convenience subclass for ``Circle`` portal type
    """
