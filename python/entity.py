import numpy as np


class Entity:
    def __init__(self, obj,
                 position=[0., 0., 0.],
                 rotation=[0., 0., 0.],
                 scale=[1., 1., 1.]):
        self.obj = obj
        self.pos = position
        self.rotate = rotation
        self.scale = scale
