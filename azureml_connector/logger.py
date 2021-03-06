from azureml.core import Run

def log_metric(name, value):
    run = Run.get_context()
    if "OfflineRun" not in run.id:
        run.log(name, value)

def log_image(name, path=None, plot=None, description=''):
    run = Run.get_context()
    if "OfflineRun" not in run.id:
        run.log_image(name, path, plot, description)
