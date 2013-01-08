from django import forms
from django.utils.translation import ugettext_lazy as _
from cdr.forms import CdrSearchForm
from voip_report.models import VOIPCALL_DISPOSITION
from voip_report.constants import BILLED_STATUS_LIST


voip_call_disposition_list = []
voip_call_disposition_list.append(('all', 'ALL'))
for i in VOIPCALL_DISPOSITION:
    voip_call_disposition_list.append((i[0], i[1]))


class VoipSearchForm(CdrSearchForm):
    """
    VoIP call Report Search Parameters
    """
    billed = forms.ChoiceField(label=_('Billed'),
                               choices=list(BILLED_STATUS_LIST),
                               required=False,)
    status = forms.ChoiceField(label=_('Disposition'),
                               choices=voip_call_disposition_list,
                               required=False,)

    def __init__(self, *args, **kwargs):
        super(VoipSearchForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['from_date', 'to_date', 'billed', 'status']
