import dtlpy as dl
import logging
from logging_utils import logginger
logger = logging.getLogger(name=__name__)
from importlib import import_module


class LocalTrialConnector():

    def __init__(self):
        self.logger = logginger(__name__)

    def run(self, devices, model_specs, hp_values):
        cls = getattr(import_module('.adapter', 'zoo.' + model_specs['name']), 'AdapterModel')

        adapter = cls()
        adapter.trial_init(devices, model_specs, hp_values)
        if hasattr(adapter, 'reformat'):
            adapter.reformat()
        if hasattr(adapter, 'data_loader'):
            adapter.data_loader()
        if hasattr(adapter, 'preprocess'):
            adapter.preprocess()
        if hasattr(adapter, 'build'):
            adapter.build()
        self.logger.info('commencing training . . . ')
        adapter.train()
        self.logger.info('training finished')
        checkpoint = adapter.get_checkpoint()
        if type(checkpoint['metrics']['val_accuracy']) is not float:
            raise Exception(
                'adapter, get_best_metrics method must return dict with only python floats. '
                'Not numpy floats or any other objects like that')
        return checkpoint