import jwt
import time
from datetime import datetime, timedelta

from enum import Enum
from flask import current_app

from project import bcrypt, db
from project.models import CommonModel, SurrogatePK


class Role(Enum):
    """
    Role model:
    - ADMIN: admin role
    - USER: user role
    """
    ADMIN = 0
    USER = 1


class User(CommonModel, SurrogatePK):
    """
    User model:
    - firstname: firstname of the user
    - lastname: lastname of the user
    - username: username of the user
    - email: email of the user
    - password: password of the user
    - profile_image: profile picture of the user
    - role: role of the user
    """
    __tablename__ = "users"

    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(256), nullable=True)
    role = db.Column(db.Enum(Role), default=Role.USER)

    is_active = db.Column(db.Boolean, default=True)
    is_suspended = db.Column(db.Boolean, default=False)

    def __init__(self, firstname: str, lastname: str, email: str, password: str, profile_image: str = None, **kwargs):
        """Create instance."""
        username = self.get_username(email)

        db.Model.__init__(
            self,
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            profile_image=profile_image,
            **kwargs
        )

        self.set_password(password)

    def get_username(self, email: str):
        """Create username."""
        return email.split("@")[0]

    def set_password(self, password: str):
        """Set password."""
        self.password = bcrypt.generate_password_hash(
            password,
            current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")

    def check_password(self, value: str):
        """Check password."""
        return bcrypt.check_password_hash(
            self.password,
            value.encode("utf-8")
        )

    def encode_auth_token(self, user_id: int):
        """
        Generates the Auth Token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str):
        """
        Decodes the auth token
        """
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def get_reset_password_token(self, expires_in: int = 600):
        """
        Generate a reset password token.
        """
        return jwt.encode(
            {
                "reset_password": self.id,
                "exp": time.time() + expires_in  # by default, the token expires in 10 minutes
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token: str):
        """
        Verify a reset password token.
        """
        try:
            id = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )["reset_password"]

        except:
            return None

        return User.query.get(id)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)

    def to_dict(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "email": self.email,
            "profile_image": self.profile_image,
            "role": self.role.name,
            "is_active": self.is_active,
            "is_suspended": self.is_suspended,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Subscription(Enum):
    """
    UserSubscription model:
    - FREE: free subscription (default - $0/month)
    - BASIC: basic subscription ($10/month)
    - STANDARD: standard subscription ($20/month)
    - PREMIUM: premium subscription ($35/month)
    """
    FREE = 0
    BASIC = 10
    STANDARD = 20
    PREMIUM = 35


class UserSubscription(CommonModel, SurrogatePK):
    """
    UserSubscription model:
    - user_id: id of the user
    - subscription: subscription of the user
    - start_date: start date of the subscription
    - end_date: end date of the subscription
    """
    __tablename__ = "user_subscriptions"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subscription = db.Column(db.Enum(Subscription), default=Subscription.FREE)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id: int, subscription: Subscription, start_date: datetime, end_date: datetime, **kwargs):
        db.Model.__init__(self, user_id=user_id, subscription=subscription,
                          start_date=start_date, end_date=end_date, **kwargs)

    def __repr__(self):
        return "<UserSubscription | {0} | {1} >".format(self.user_id, self.subscription)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subscription": self.subscription.name,
            "start_date": self.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": self.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class BlacklistToken(CommonModel, SurrogatePK):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token: str):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token: str):
        """
        Check whether auth token has been blacklisted
        """
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
