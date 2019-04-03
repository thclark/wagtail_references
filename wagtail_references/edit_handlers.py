from django.template.loader import render_to_string

from wagtail.admin.compare import ForeignObjectComparison
from wagtail.admin.edit_handlers import BaseChooserPanel


class ReferenceChooserPanel(BaseChooserPanel):
    object_type_name = "reference"

    # def widget_overrides(self):
    #     TODO reinstate if widget needs to be overridden - see how the wagtailimages widget works
    #     from .widgets import AdminReferenceChooser
    #     return {self.field_name: AdminReferenceChooser}

    def get_comparison_class(self):
        return ReferenceFieldComparison


class ReferenceFieldComparison(ForeignObjectComparison):
    def htmldiff(self):
        reference_a, reference_b = self.get_objects()

        return render_to_string("wagtail_references/widgets/compare.html", {
            'reference_a': reference_a,
            'reference_b': reference_b,
        })
