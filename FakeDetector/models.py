from django.db import models


# Create your models here.

class Articles():
    id = str
    name = str
    author = str
    title = str
    description = str
    url = str
    published_at = str
    prediction = bool
    urlToImage = str
