from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.memoize.instance import memoize
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from redturtle.utils import msgFactory as _


class UpdateSecuritySettings(BrowserView):
    """
    Use this view to update security settings per portal type.
    Standard way to do that pass through ZMI but update the whole
    site objects
    """

    template = ViewPageTemplateFile('update_security_settings.pt')

    def __call__(self):
        """
        update security settings per type
        """
        opt = {}

        if 'update' not in self.request:
            return self.template()

        portal_type = self.request['portal_type']

        if not portal_type:
            msg = _(u"No portal type selected! Please correct!")
            return self.template(**self.get_info(msg, u'error'))

        status = self.update_security_settings(portal_type)

        return self.template(**status)

    def get_info(self, msg, msg_type):
        return dict(msg=msg,
                    msg_type=msg_type,
                    msg_type_value=_(msg_type))

    def update_security_settings(self, portal_type):
        pwf = getToolByName(self.context, 'portal_workflow')
        pc = getToolByName(self.context, 'portal_catalog')
        wf = self.context.portal_workflow.getWorkflowsFor(portal_type)
        pt_title = translate(portal_type, domain='plone', context=self.request)
        if len(wf) != 1:
            msg = _(u"Unable to detect correct workflow for %s" % pt_title)
            return self.get_info(msg, u'error')

        brains = pc(portal_type=portal_type)
        if not brains:
            msg = _(u"No brains found for %s" % pt_title)
            return self.get_info(msg, u'warning')

        count = 0
        for brain in brains:
            count += 1
            obj = brain.getObject()
            wf[0].updateRoleMappingsFor(obj)
            if not count % 500:
                commit()
                self.context.plone_log('Committed %s' % str(count))

        msg = _(u"Process ends with the update of %s %s object(s)"
                % (len(brains), pt_title))
        return self.get_info(msg, u'info')

    @memoize
    def get_all_types(self):
        """
        Take from plone vocabulary all available tyes
        """
        vocab_factory = getUtility(IVocabularyFactory,
                        name="plone.app.vocabularies.ReallyUserFriendlyTypes")
        types = []
        for v in vocab_factory(self.context):
            if v.title:
                title = translate(v.title,
                                  context=self.request)
            else:
                title = translate(v.token,
                                  domain='plone',
                                  context=self.request)
            types.append(dict(id=v.value, title=title))

        def _key(v):
            return v['title']

        types.sort(key=_key)
        types.insert(0, dict(id='',
                     title=translate('-- select a type --',
                                     domain='redturtle.utils',
                                     context=self.request)))
        return types
