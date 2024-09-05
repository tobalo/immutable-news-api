import logging
from typing import Union, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from bson import ObjectId
import newspaper
from datetime import datetime
import asyncio
from db.config import get_database, close_mongodb_connection
from db.models.news import NewsArticle, NewsSubmission, NewsArticleResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Event handlers for startup and shutdown
@app.on_event("startup")
async def startup_db_client():
    await get_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongodb_connection()

async def crawl_news(url: str):
    try:
        logger.info(f"Starting to crawl URL: {url}")
        
        article = newspaper.Article(url=url, language='en')
        article.download()
        article.parse()
        
        logger.info("Successfully downloaded and parsed the article")
        
        # Extract the required information
        title = article.title or "Unknown Title"
        content = article.text or "No content found"
        authors = ", ".join(article.authors) if article.authors else "Unknown"
        published_date = article.publish_date or datetime.now()
        
        logger.info(f"Title: {title}")
        logger.info(f"Authors: {authors}")
        logger.info(f"Published Date: {published_date}")
        logger.info(f"Content length: {len(content)} characters")
        
        # Additional information
        top_image = article.top_image
        videos = article.movies
        keywords = article.keywords
        summary = article.summary
        
        logger.info("Successfully extracted all fields")
        
        return NewsArticle(
            title=title,
            content=content,
            authors=authors,
            published_date=published_date,
            url=url,
            top_image=top_image,
            videos=videos,
            keywords=keywords,
            summary=summary
        )
    except Exception as e:
        logger.error(f"An error occurred while crawling: {str(e)}")
        return None

@app.get("/")
def read_root():
    return {"message": "Howdy from Texas by yeetum and intrana"}

@app.post("/news/submit")
async def submit_news(submission: NewsSubmission, database = Depends(get_database)):
    # Check if the article with the same URL already exists
    existing_article = await database.news_articles.find_one({"url": str(submission.url)})
    if existing_article:
        logger.info(f"Article with URL {submission.url} already exists in the database")
        return {"message": "Article already exists", "id": existing_article["_id"]}

    news_data = await crawl_news(str(submission.url))
    if news_data is None:
        raise HTTPException(status_code=400, detail="News is not crawlable")
    
    try:
        # Store the data in MongoDB
        result = await database.news_articles.insert_one(news_data.dict(by_alias=True))
        logger.info(f"Successfully stored news article with ID: {news_data.id}")
    except Exception as e:
        logger.error(f"Failed to store news article: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store news article")
    
    return {"message": "News article successfully crawled and stored", "id": news_data.id}

@app.get("/news", response_model=List[NewsArticleResponse])
async def list_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    database = Depends(get_database)
):
    try:
        cursor = database.news_articles.find().skip(skip).limit(limit)
        articles = await cursor.to_list(length=limit)
        return [NewsArticleResponse(**article) for article in articles]
    except Exception as e:
        logger.error(f"Failed to retrieve news articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve news articles")

@app.get("/news/{article_id}", response_model=NewsArticleResponse)
async def get_news_article(article_id: str, database = Depends(get_database)):
    try:
        article = await database.news_articles.find_one({"_id": article_id})
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return NewsArticleResponse(**article)
    except Exception as e:
        logger.error(f"Failed to retrieve news article: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve news article")