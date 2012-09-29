import operator

from yaml import load, dump


class Alert(object):

    def __init__(self, alert_data):
        self.name = alert_data['name']
        self.target = alert_data['target']
        self.warning = alert_data['warning']
        self.critical = alert_data['critical']

        self.comparison_operator = self._determine_comparison_operator(self.warning, self.critical)

    def _determine_comparison_operator(self, warn_value, crit_value):
        if warn_value > crit_value:
            return operator.le
        elif crit_value > warn_value:
            return operator.ge

    def check_value(self, value):
        if self.comparison_operator(value, self.critical):
            return 'CRITICAL'
        elif self.comparison_operator(value, self.warning):
            return 'WARNING'
        return None


def contents_of_file(filename):
    open_file = open(filename)
    contents = open_file.read()
    open_file.close()
    return contents


def get_alerts():

    alert_yml = contents_of_file('alerts.yml')
    alert_strings = load(alert_yml)
    alerts = []
    for alert_string in alert_strings['alerts']:
        alerts.append(Alert(alert_string))
    return alerts

if __name__ == '__main__':
    print get_alerts()