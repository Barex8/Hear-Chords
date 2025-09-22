class Note:
    duration = 0
    wave = None

    def __init__(self,duration,wave,octave,name):
        self.duration = duration
        self.wave = wave
        self.octave = octave
        self.name = name
