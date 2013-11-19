from ..level import Level


class ConsoleNotifier(object):
    """ this is just a dummy notifier for debug purposes """
    
    name = 'console'
    
    def __init__(self, storage):
        self._storage = storage

    def notify(self, alert_key, level, description, html_description):
        domain = 'Console'
        notified = self._storage.is_locked_for_domain_and_key(domain, alert_key)
        if level == Level.NOMINAL and notified:
            print "RESOLVED: >>>>", alert_key, level, description
            self._storage.remove_lock_for_domain_and_key(domain, alert_key)
        elif level in (Level.WARNING, Level.CRITICAL, Level.NO_DATA) and not notified:
            print "ALERT: >>>>", alert_key, level, description
            self._storage.set_lock_for_domain_and_key(domain, alert_key)
