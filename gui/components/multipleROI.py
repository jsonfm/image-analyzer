from .ROI import ROI

class multipleROI:
    def __init__(self, n=10, prefix="Label"):
        self.items = {f"{prefix} {i + 1}": ROI()  for i in range(n)}