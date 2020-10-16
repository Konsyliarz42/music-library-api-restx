class Song():
    def __init__(self, band_name, album_name, nr, title):
        self.band_name  = band_name
        self.album_name = album_name
        self.nr         = nr
        self.title      = title

    def __repr__(self):
        return f"{self.band_name} - {self.title}"

    
    @property
    def serialize(self):
        return  {
                    'band_name':    self.band_name,
                    'album_name':   self.album_name,
                    'title':        self.title,
                    'nr':           self.nr
                }

