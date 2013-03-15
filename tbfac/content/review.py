from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from tbfac.content import MessageFactory as _
from tbfac.content.info import IInfo
from Products.CMFCore.utils import getToolByName


# Interface class; used to define content-type schema.

class IReview(form.Schema, IImageScaleTraversable):
    """
    TBFAC Review Type
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/activityreview.xml to define the content type
    # and add directives here as necessary.
    
    #form.model("models/activityreview.xml")

    info_ref = RelationList(
        title=_(u"Referenced Info"),
        description=_(u"If no referenced Info items to select, please manually fill them in the next field."),
        value_type=RelationChoice(
            source=ObjPathSourceBinder(
                object_provides=IInfo.__identifier__,
            ),
        ),
        required=False,
    )

    info_rvw = schema.TextLine(
        title=_(u"Reviewed Info"),
        description=_(u"Use comma to separate multiple Info data."),
        required=False,
    )

    text = RichText(
        title=_(u"Body"),
        required=False,
    )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Review(dexterity.Item):
    grok.implements(IReview)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# review_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IReview)
    grok.require('zope2.View')
    grok.name('view')

    def toLocalizedTime(self, time, long_format=None, time_only=None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        return util.ulocalized_time(time, long_format, time_only, self.context, domain='plonelocales')

    def relatedInfos(self):
        infos = []
        if self.context.info_ref is not None:
            for ref in self.context.info_ref:
                obj = ref.to_object
                infos.append({
                    'title': obj.title,
                })
        return infos

    def creator(self):
        return self.context.Creator()

    def author(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.creator())

    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()

