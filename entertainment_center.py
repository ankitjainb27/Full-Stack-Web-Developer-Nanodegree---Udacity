import media
import fresh_tomatoes


Avengers = media.Movie("Age of Ultron", "https://image.tmdb.org/t/p/w185/nveEFHidaEXZCG7zhfTc26hVqSu.jpg",
                       "https://www.youtube.com/watch?v=tmeOjFno6Do", 2015)
Birdman = media.Movie("Birdman", "https://image.tmdb.org/t/p/w185/zJF4JKbaYUhKFWbwY4u5WpvgvER.jpg",
                      "https://www.youtube.com/watch?v=uJfLoE6hanc", 2014)
Godzilla = media.Movie("Godzilla", "https://image.tmdb.org/t/p/w185/szVwkB4H5yyOJBVuQ432b9boO0N.jpg",
                       "https://www.youtube.com/watch?v=I-EEqJ9HyTk", 2014)
Jurassic_World = media.Movie("Jurassic World", "https://image.tmdb.org/t/p/w185/ce9vGDMexoihZ8ta3Zt60k4FChb.jpg",
                             "https://www.youtube.com/watch?v=RFinNxS5KN4", 2015)

movies = [Avengers, Birdman, Godzilla, Jurassic_World]
fresh_tomatoes.open_movies_page(movies)