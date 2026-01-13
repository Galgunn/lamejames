class Animation():
    def __init__(self, images, frame_dur, loop=True):
        self.images = images
        self.frame_dur = frame_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.frame_dur, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.frame_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.frame_dur * len(self.images) - 1)
            if self.frame >= self.frame_dur * len(self.images) - 1:
                self.done = True

    def reset(self):
        self.frame = 0

    def img(self):
        return self.images[int(self.frame / self.frame_dur)]