import logging
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request

from project import db
from project.models import (
    Role,
    User,
    Subscription,
    UserSubscription,
    Topic,
    Source,
    Keyword,
    Article
)

from project.api.authentications import authenticate
from project.api.validators import field_type_validator, required_validator
from project.api.utils import *

user_blueprint = Blueprint('user', __name__, template_folder='templates')

logger = logging.getLogger(__name__)


@user_blueprint.route('/user/list', methods=['GET'])
@authenticate
def get_all_users(user_id: int):
    """Get all users"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        admin = User.query.filter_by(id=user_id, role=Role.ADMIN).first()

        if not admin:
            response_object['message'] = 'Unauthorized access.'
            return jsonify(response_object), 401

        users = User.query.all()

        response_object["status"] = True
        response_object["message"] = "Users retrieved successfully."
        response_object["data"] = [user.to_dict() for user in users]

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@user_blueprint.route('/user/get/<user_id>', methods=['GET'])
@authenticate
def get_single_user(user_id: int):
    """Get single user"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        admin = User.query.filter_by(id=user_id, role=Role.ADMIN).first()

        if not admin:
            response_object['message'] = 'Unauthorized access.'
            return jsonify(response_object), 401

        user = User.query.filter_by(id=user_id).first()

        response_object["status"] = True
        response_object["message"] = "User retrieved successfully."
        response_object["data"] = user.to_dict()

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@user_blueprint.route('/user/get', methods=['GET'])
@authenticate
def get_user(user_id: int):
    """Get user"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        user = User.query.filter_by(id=user_id).first()

        response_object["status"] = True
        response_object["message"] = "User retrieved successfully."
        response_object["data"] = user.to_dict()

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@user_blueprint.route('/user/find', methods=['GET'])
@authenticate
def find_user(user_id: int):
    """Find user"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        admin = User.query.filter_by(id=user_id, role=Role.ADMIN).first()

        if not admin:
            response_object['message'] = 'Unauthorized access.'
            return jsonify(response_object), 401

        email = request.args.get('email')
        username = request.args.get('username')
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')

        user = User.query

        if email:
            user = user.filter_by(email=email)

        if username:
            user = user.filter_by(username=username)

        if firstname:
            user = user.filter_by(firstname=firstname)

        if lastname:
            user = user.filter_by(lastname=lastname)

        user = user.first()

        response_object["status"] = True
        response_object["message"] = "User retrieved successfully."
        response_object["data"] = user.to_dict()

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@user_blueprint.route('/user/setting', methods=['PATCH'])
@authenticate
def user_settings(user_id: int):
    """
    Add/Update User settings:
    - Subscription
    - Topic
    - Source
    - Keyword
    """
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    post_data = request.get_json()

    if not post_data:
        return jsonify(response_object), 400

    try:
        field_types = {
            "subscription": str, "topic": list,
            "source": list, "keyword": list
        }

        post_data = field_type_validator(post_data, field_types)

        subscription = post_data.get('subscription')
        subscription = str(subscription).upper() if subscription else None
        topics = post_data.get('topic')
        sources = post_data.get('source')
        keywords = post_data.get('keyword')

        # is_changed = False

        if subscription and subscription in Subscription.__members__:
            user_subscription = UserSubscription.query.filter_by(
                user_id=user_id
            ).first()

            if user_subscription.subscription != Subscription[subscription]:
                # is_changed = True

                user_subscription.update(
                    subscription=Subscription[subscription],
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=30)
                )

        if topics:
            # if Topic.query.filter(
            #     Topic.user_id == user_id,
            #     Topic.name.in_(topics)
            # ).count() != len(topics):
            #     is_changed = True

            Topic.query.filter_by(user_id=user_id).delete()

            topics = [topic.lower()
                      for topic in topics if topic.lower() in TOPICS]

            for topic in topics:
                Topic(user_id=user_id, name=topic).save()

        if sources:
            # if Source.query.filter(
            #     Source.user_id == user_id,
            #     Source.name.in_(sources)
            # ).count() != len(sources):
            #     is_changed = True

            Source.query.filter_by(user_id=user_id).delete()

            for source in sources:
                Source(user_id=user_id, name=source).save()

        if keywords:
            # if Keyword.query.filter(
            #     Keyword.user_id == user_id,
            #     Keyword.name.in_(keywords)
            # ).count() != len(keywords):
            #     is_changed = True

            Keyword.query.filter_by(user_id=user_id).delete()

            keywords = [keyword.lower() for keyword in keywords]

            for keyword in keywords:
                Keyword(user_id=user_id, name=keyword).save()

        if keywords and topics and sources:
            # remove all articles
            Article.query.filter_by(user_id=user_id).delete()

            for topic in topics:
                # join all keywords with AND and place in quotes for multi-word
                # keywords
                keywords = ' AND '.join(
                    [f'"{keyword}"' if ' ' in keyword else keyword for keyword in keywords]
                )

                articles = get_news(
                    q=keywords,
                    topic=topic,
                    sources=sources
                )

                if articles['status'] == 'ok':
                    for article in articles['articles']:
                        Article(
                            user_id=user_id,
                            title=article['title'],
                            source=article['clean_url'],
                            author=article['authors'],
                            date=article['published_date'],
                            summary=article['summary'],
                            link=article['link'],
                            image_url=article['media'],
                            keywords=get_keywords(article['excerpt'])
                        ).save()

        response_object["status"] = True
        response_object["message"] = "User settings updated successfully."
        # response_object["data"] = {
        #     "is_changed": is_changed
        # }

        return jsonify(response_object), 200

    except Exception as e:
        db.session.rollback()
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@user_blueprint.route('/user/setting', methods=['GET'])
@authenticate
def get_user_settings(user_id: int):
    """Get user settings"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        user_subscription = UserSubscription.query.filter_by(
            user_id=user_id
        ).first()

        topics = Topic.query.filter_by(user_id=user_id).all()
        sources = Source.query.filter_by(user_id=user_id).all()
        keywords = Keyword.query.filter_by(user_id=user_id).all()

        response_object["status"] = True
        response_object["message"] = "User settings retrieved successfully."
        response_object["data"] = {
            "subscription": user_subscription.to_dict(),
            "topics": [topic.to_dict() for topic in topics],
            "sources": [source.to_dict() for source in sources],
            "keywords": [keyword.to_dict() for keyword in keywords]
        }

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400
