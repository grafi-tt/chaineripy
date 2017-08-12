from copy import copy

from IPython.core.display import display
from ipywidgets import HTML
from pandas import DataFrame

from chainer.training import extension
from chainer.training.extensions import log_report as log_report_module


class PrintReport(extension.Extension):

    """Trainer extension to print the accumulated results.
    This extension uses the log accumulated by a :class:`LogReport` extension
    to print specified entries of the log in a human-readable format.
    Args:
        entries (list of str): List of keys of observations to print.
        log_report (str or LogReport): Log report to accumulate the
            observations. This is either the name of a LogReport extensions
            registered to the trainer, or a LogReport instance to use
            internally.
        out: Stream to print the bar. Standard output is used by default.
    """

    def __init__(self, entries, log_report='LogReport'):
        self._entries = entries
        self._log_report = log_report

        self._default_row = dict((e, None) for e in entries)
        self._widget = HTML()
        self.count = 0
        self.update([])

    def initialize(self, trainer):
        display(self._widget)

    def __call__(self, trainer):
        log_report = self._log_report
        if isinstance(log_report, str):
            log_report = trainer.get_extension(log_report)
        elif isinstance(log_report, log_report_module.LogReport):
            log_report(trainer)  # update the log report
        else:
            raise TypeError('log report has a wrong type %s' %
                            type(log_report))

        self.update(log_report.log)

    @property
    def widget(self):
        return self._widget

    def update(self, log):
        df = DataFrame(columns=self._entries)

        for stat in log:
            stat = copy(stat)
            stat['epoch'] = int(stat['epoch'])
            stat['iteration'] = int(stat['iteration'])

            d = {}
            for k in self._entries:
                if k in stat:
                    d[k] = stat[k]
                else:
                    d[k] = None
            df = df.append(d, ignore_index=True)

        if 'epoch' in df:
            df['epoch'] = df['epoch'].astype(int)
        if 'iteration' in df:
            df['iteration'] = df['iteration'].astype(int)
        self._widget.value = df.to_html(index=False, na_rep='')

    def serialize(self, serializer):
        log_report = self._log_report
        if isinstance(log_report, log_report_module.LogReport):
            log_report.serialize(serializer['_log_report'])
