class BaseController:
    """Base Controller describing common storage for Controllers at this session"""
    def __init__(self, task_storage):
        self.task_storage = task_storage
