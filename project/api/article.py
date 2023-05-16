import logging
from flask import jsonify, request, Blueprint

from project import db
from project.api.authentications import authenticate
from project.api.validators import email_validator, field_type_validator, required_validator
from project.api.utils import get_bullet_points, get_news, get_news_sources, TOPICS

from project.models import Role, User, Article, Keyword


article_blueprint = Blueprint('article', __name__, template_folder='templates')
logger = logging.getLogger(__name__)


@article_blueprint.route('/article/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': True,
        'message': 'Article is running.'
    }), 200


@article_blueprint.route('/article/topics', methods=['GET'])
@authenticate
def get_topics(user_id: int):
    """Get all topics"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        response_object["status"] = True
        response_object["message"] = "Topics retrieved successfully."
        response_object["data"] = TOPICS

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@article_blueprint.route('/article/sources', methods=['GET'])
@authenticate
def get_sources(user_id: int):
    """Get all sources"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        # list of topics separated by comma
        topics = request.args.get('topics', None)

        sources = []
        if topics:
            for topic in topics.split(','):
                sources.extend(get_news_sources(topic.strip())['sources'])
        else:
            sources = get_news_sources(topics)['sources']

        response_object["status"] = True
        response_object["message"] = "Sources retrieved successfully."
        response_object["data"] = sources

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@article_blueprint.route('/article/list', methods=['GET'])
@authenticate
def get_all_articles(user_id: int):
    """Get all articles"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        admin = User.query.filter_by(id=user_id, role=Role.ADMIN).first()

        if not admin:
            response_object['message'] = 'Unauthorized access.'
            return jsonify(response_object), 401

        articles = Article.query.all()

        response_object["status"] = True
        response_object["message"] = "Articles retrieved successfully."
        response_object["data"] = [article.to_dict() for article in articles]

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@article_blueprint.route('/article/get/<article_id>', methods=['GET'])
@authenticate
def get_single_article(user_id: int, article_id: int):
    """Get single article"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        article = Article.query.filter_by(
            id=article_id, user_id=user_id).first()

        if not article:
            response_object['message'] = 'Article not found.'
            return jsonify(response_object), 404

        response_object["status"] = True
        response_object["message"] = "Article retrieved successfully."
        response_object["data"] = article.to_dict()

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@article_blueprint.route('/article/get/<page>/<limit>', methods=['GET'])
@authenticate
def get_articles(user_id: int, page: int, limit: int):
    """Get articles"""
    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        articles = Article.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=limit, error_out=False)
        response_object["status"] = True
        response_object["message"] = "Articles retrieved successfully."
        response_object["data"] = [article.to_dict()
                                   for article in articles.items]
        response_object["total"] = articles.total
        response_object["pages"] = articles.pages
        response_object["page"] = articles.page
        response_object["has_next"] = articles.has_next
        response_object["has_prev"] = articles.has_prev

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400


@article_blueprint.route('/article/get/<page>/<limit>/<keyword>', methods=['GET'])
@authenticate
def get_articles_by_keyword(user_id: int, page: int, limit: int, keyword: str):
    """Get articles by keyword"""

    response_object = {
        'status': False,
        'message': 'Invalid payload.'
    }

    try:
        articles = Article.query.filter(
            Article.user_id == user_id, Article.keywords.contains(keyword)).paginate(
            page=page, per_page=limit, error_out=False)
        response_object["status"] = True
        response_object["message"] = "Articles retrieved successfully."
        response_object["data"] = [article.to_dict()
                                   for article in articles.items]
        response_object["total"] = articles.total
        response_object["pages"] = articles.pages
        response_object["page"] = articles.page
        response_object["has_next"] = articles.has_next
        response_object["has_prev"] = articles.has_prev

        return jsonify(response_object), 200

    except Exception as e:
        logger.error(e)
        response_object['message'] = 'Try again: ' + str(e)
        return jsonify(response_object), 400
