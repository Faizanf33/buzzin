from project import db
from datetime import datetime


class CommonModel(db.Model):
    """
    CommonModel is an abstract class that contains the common fields
    """
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)


class SurrogatePK(object):
    """
    A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class.
    """
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None
