from watchdog.observers import Observer

class FileSyncObserver(Observer):
    """A specified Observer that override on_thread_stop method
    """

    def on_thread_stop(self):
        self.unschedule_all()

