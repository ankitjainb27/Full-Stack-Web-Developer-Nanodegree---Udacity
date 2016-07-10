import webbrowser


# Model for the Movie Trailers
class Movie():
    """Movie is the model for Movie Trailer
    Attributes:
        title (str): Title of the movie.
        poster_image (str): link to poster of the movie
        trailer_youtube_url (str): link to the youtube trailer of the movie
        year (int): year in which the movie was released
    """
    def __init__(self, title, poster_image, trailer_youtube_url, year):
        self.title = title
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube_url
        self.year = year

    # function to show trailer in modal of bootstrap on the website itself
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
