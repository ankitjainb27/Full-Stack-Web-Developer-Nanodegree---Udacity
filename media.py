import webbrowser


# Model for the Movie Trailers
class Movie():
    def __init__(self, title, poster_image, trailer_youtube_url, year):
        self.title = title
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube_url
        self.year = year

    # function to show trailer in modal of bootstrap on the website itself
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
