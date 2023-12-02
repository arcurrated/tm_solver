class AppConfig:
    selectionThreshold: int
    
    def __init__(self, selectionThreshold=10):
        self.selectionThreshold = selectionThreshold