import operator
import re

from graphite_data_record import NoDataError
from level import Level


class Alert(object):

    def __init__(self, alert_data, doc_url=None):
        self.name = alert_data['name']
        self.target = alert_data['target']
        self.warning = alert_data['warning']
        self.critical = alert_data['critical']
        self.from_ = alert_data.get('from', '-1min')
        if alert_data.get('exclude') is not None:
            self.exclude = set(re.compile(x) for x in alert_data['exclude'])
        else:
            self.exclude = set()
        self.check_method = alert_data.get('check_method', 'latest')
        self.notifiers = alert_data.get('notifiers', [])        
        self.notifiers += ['console']        
        self.ignore_no_data = alert_data.get('ignore_no_data', False)
        
        self.comparison_operator = self._determine_comparison_operator(self.warning, self.critical)
        self._doc_url = doc_url



    def documentation_url(self, target=None):
        if self._doc_url is None:
            return None
        template = self._doc_url + '/' + self.name
        if target is None:
            url = template
        else:
            url = template + '#' + target
        return url

    def _determine_comparison_operator(self, warn_value, crit_value):
        if warn_value > crit_value:
            return operator.le
        elif crit_value > warn_value:
            return operator.ge

    def check_record(self, record):
        for pattern in self.exclude:
            if pattern.search(record.target):
                return Level.NOMINAL, 'Excluded'

        try:            
            if self.check_method == 'latest':
                value = record.get_last_value()
            else:
                value = record.get_average()
        except NoDataError:
            return Level.NO_DATA, 'No data'
        if self.comparison_operator(value, self.critical):
            return Level.CRITICAL, value
        elif self.comparison_operator(value, self.warning):
            return Level.WARNING, value
        return Level.NOMINAL, value

    def value_for_level(self, level):
        if level == Level.CRITICAL:
            return self.critical
        elif level in (Level.WARNING, Level.NOMINAL):
            return self.warning
        else:
            return None



if __name__ == '__main__':
    print get_alerts()
