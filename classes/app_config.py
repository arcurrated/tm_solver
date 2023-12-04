class AppConfig:
    selection_threshold: int
    
    def __init__(self, selection_threshold=10):
        self.selection_threshold = selection_threshold