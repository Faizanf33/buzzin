from datetime import datetime

from project import db
from project.models.user_model import User, CommonModel, SurrogatePK

class Article(CommonModel, SurrogatePK):
    """
    Article model:
    - title: title of the article
    - slug: slug of the article (title in lowercase and with dashes)
    - source: source of the article
    - author: author of the article
    - date: date of the article
    - summary: summary of the article
    - keywords: keywords of the article (comma separated)
    - link: link of the article
    - image_url: image url of the article

    - user_id: id of the user who created the article
    """
    __tablename__ = "articles"

    title = db.Column(db.String(256), nullable=False)
    source = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(256), nullable=True)
    image_url = db.Column(db.String(256), nullable=True)
    keywords = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, title: str, source: str, author: str, date: datetime, keywords: str, user_id: int, **kwargs):
        slug = title.lower().replace(" ", "-")
        # convert date to datetime object
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        keywords = str(keywords) if keywords else None
        db.Model.__init__(self, title=title, slug=slug, source=source,
                          author=author, date=date, keywords=keywords, user_id=user_id, **kwargs)

    def __repr__(self):
        return "<Article | {0} | {1} >".format(self.title, self.source)

    def __str__(self):
        return self.title

    def get_keywords(self):
        return eval(self.keywords) if self.keywords else []

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "slug": self.slug,
            "source": self.source,
            "author": self.author,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": self.summary,
            "link": self.link,
            "image_url": self.image_url,
            "keywords": eval(self.keywords) if self.keywords else [],
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Keyword(CommonModel, SurrogatePK):
    """
    Keyword model:
    - name: name of the keyword
    - user_id: id of the user
    """
    __tablename__ = "keywords"

    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, name: str, user_id: int, **kwargs):
        db.Model.__init__(self, name=name, user_id=user_id, **kwargs)

    def __repr__(self):
        return "<Keyword | {0} >".format(self.name)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class Source(CommonModel, SurrogatePK):
    """
    Source model:
    - name: name of the source
    - user_id: id of the user
    """
    __tablename__ = "sources"

    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, name: str, user_id: int, **kwargs):
        db.Model.__init__(self, name=name, user_id=user_id, **kwargs)

    def __repr__(self):
        return "<Source | {0} >".format(self.name)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Topic(CommonModel, SurrogatePK):
    """
    Topic model:
    - name: name of the topic
    - user_id: id of the user
    """
    __tablename__ = "topics"

    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, name: str, user_id: int, **kwargs):
        db.Model.__init__(self, name=name, user_id=user_id, **kwargs)

    def __repr__(self):
        return "<Topic | {0} >".format(self.name)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
