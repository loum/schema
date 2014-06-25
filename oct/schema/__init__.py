from datetime import datetime
from ming import Field
from ming.declarative import Document
from oct.session import SESSION


class BlogPost(Document):
    class __mongometa__:
        session = SESSION
        name = 'blog.posts'
        indexes = ['author.name', 'comments.author.name']

    _id = Field(str)
    title = Field(str)
    posted = Field(datetime, if_missing=datetime.utcnow())
    author = Field(dict(author=dict(username=str, display_name=str)))
    text = Field(str)
    comments = Field([dict(author=dict(username=str, display_name=str),
                      posted=datetime,
                      text=str)])


class BlogPoster(BlogPost):
    class __mongometa__:
        name = 'blog.poster'

    banana = Field(str)
