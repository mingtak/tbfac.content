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

# Interface class; used to define content-type schema.

class IJury(form.Schema, IImageScaleTraversable):
    """
    TBFAC Jury Type
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/jury.xml to define the content type
    # and add directives here as necessary.
    
    #form.model("models/jury.xml")

    title = schema.TextLine(
        title=_(u"Name"),
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    category = schema.Choice(
        title=_(u'Award Category'),
        values=[_(u'Visual Arts'), _(u'Performing Arts'), _(u'Uncatrgorized')],
        required=True,
    )

    form.primary('bio')
    bio = RichText(
        title=_(u"Bio"),
        required=False,
    )

    form.primary('photo')
    photo = NamedImage(
        title=_(u"Photo"),
        description=_(u"Upload Photo"),
        required=False,
    )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Jury(dexterity.Item):
    grok.implements(IJury)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# jury_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IJury)
    grok.require('zope2.View')
    grok.name('view')

