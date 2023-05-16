import os
import yake
import openai
from imagekitio.client import ImageKit
from werkzeug.utils import secure_filename
from newscatcherapi import NewsCatcherApiClient


TOPICS = [
    "news", "sport", "tech", "world",
    "finance", "politics", "business", "economics",
    "entertainment", "beauty", "travel", "music",
    "food", "science", "gaming", "energy"
]


# Environment variables
ACCESS_PRIVATE_KEY = os.getenv('IMAGEKIT_PRIVATE_KEY')
ACCESS_PUBLIC_KEY = os.getenv('IMAGEKIT_PUBLIC_KEY')
ACCESS_URL_ENDPOINT = os.getenv('IMAGEKIT_URL_ENDPOINT')
NEWSCATCHER_API_KEY = os.getenv('NEWSCATCHER_API_KEY')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')


# initialize ImageKit
imagekit = ImageKit(
    private_key=ACCESS_PRIVATE_KEY,
    public_key=ACCESS_PUBLIC_KEY,
    url_endpoint=ACCESS_URL_ENDPOINT
)


def upload_file(file: str, file_name: str) -> dict:
    """
    Upload file to ImageKit
    """
    response = imagekit.upload_file(
        file=file,
        file_name=file_name
    )

    return response


def secure_file(file: str) -> dict:
    """
    Secure filename and get file info
    """
    filename = secure_filename(file.filename)
    filetype = file.content_type

    # save file locally
    file.save(filename)
    filesize = os.stat(filename).st_size

    return {
        "filename": filename,
        "filetype": filetype,
        "filesize": filesize
    }


# initialize NewsCatcher API
newscatcherapi = NewsCatcherApiClient(x_api_key=NEWSCATCHER_API_KEY)


def get_news_sources(topic: str = None) -> dict:
    """
    Get news sources given a topic
    """
    return newscatcherapi.get_sources(
        topic=topic,
        lang="en"
    )


def get_news(q: str, topic: str, sources: list, page: int = 1, limit: int = 100) -> dict:
    """
    Get news given a query, topic, sources, page and limit
    """
    return newscatcherapi.get_search(
        q=q,
        topic=topic,
        sources=sources,
        page=page,
        page_size=limit
    )


# Not required anymore

# initialize YAKE keyword extractor
# kw_extractor = yake.KeywordExtractor()

# def get_keywords(text: str, max_keywords: int = 10):
#     """
#     Get keywords from text
#     """
#     keywords = kw_extractor.extract_keywords(text)
#     return [keyword for keyword, score in keywords[:max_keywords]]


# configure OpenAI API
openai.api_key = OPEN_AI_API_KEY


def get_bullet_points(text: str, max_bullet_points: int = 5) -> str:
    """
    Get bullet points from text
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Please turn this article into {0} bullet points:\n\n{1}".format(
                    max_bullet_points, text
                )
            }
        ],
    )

    return response.choices[0].message.content
