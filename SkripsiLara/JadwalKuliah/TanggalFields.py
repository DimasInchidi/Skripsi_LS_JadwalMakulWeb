from django.utils.translation import ugettext as _
from django.db import models

DAY_OF_THE_WEEK = {
    '1': _(u'Senin'),
    '2': _(u'Selasa'),
    '3': _(u'Rabu'),
    '4': _(u'Kamis'),
    '5': _(u'Jumat'),
    '6': _(u'Sabtu'),
    '7': _(u'Minggu'),
}


class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length'] = 1
        super(DayOfTheWeekField, self).__init__(*args, **kwargs)
