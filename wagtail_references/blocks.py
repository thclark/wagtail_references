from django.utils.functional import cached_property

from wagtail.core.blocks import ChooserBlock

# from .shortcuts import get_rendition_or_not_found


class ReferenceChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from wagtail_references import get_reference_model
        return get_reference_model()

    # @cached_property
    # def widget(self):
    #     from wagtail_references.widgets import AdminReferenceChooser
    #     return AdminReferenceChooser

    # def render_basic(self, value, context=None):
    #     if value:
    #                 return get_rendition_or_not_found(value, 'original').img_tag()
    #             else:
    #         return ''

    class Meta:
        icon = "list-ol"
