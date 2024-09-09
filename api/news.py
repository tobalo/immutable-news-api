from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from db.config import get_database
from db.models.news import NewsArticle, NewsSubmission, NewsArticleResponse
from helpers.crawler import crawl_news
import logging
from math import ceil

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/submit")
async def submit_news(submission: NewsSubmission, database = Depends(get_database)):
    # Check if the article with the same URL already exists
    existing_article = await database.news_articles.find_one({"url": str(submission.url)})
    if existing_article:
        logger.info(f"Article with URL {submission.url} already exists in the database")
        return {"message": "Article already exists", "id": existing_article["_id"]}

    news_data = await crawl_news(str(submission.url), submission.dag_address)
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

@router.get("/", response_model=dict)
async def list_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    database = Depends(get_database)
):
    try:
        total_count = await database.news_articles.count_documents({})
        cursor = database.news_articles.find().skip(skip).limit(limit)
        articles = await cursor.to_list(length=limit)
        
        return {
            "items": [NewsArticleResponse(**article) for article in articles],
            "total": total_count,
            "page": ceil(skip / limit) + 1,
            "pages": ceil(total_count / limit)
        }
    except Exception as e:
        logger.error(f"Failed to retrieve news articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve news articles")

@router.get("/{article_id}", response_model=NewsArticleResponse)
async def get_news_article(article_id: str, database = Depends(get_database)):
    try:
        article = await database.news_articles.find_one({"_id": article_id})
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return NewsArticleResponse(**article)
    except Exception as e:
        logger.error(f"Failed to retrieve news article: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve news article")

@router.get("/constellation/{dag_address}", response_model=List[NewsArticleResponse])
async def get_news_by_constellation(
    dag_address: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    database = Depends(get_database)
):
    try:
        cursor = database.news_articles.find({"dag_address": dag_address}).skip(skip).limit(limit)
        articles = await cursor.to_list(length=limit)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found for this constellation")
        return [NewsArticleResponse(**article) for article in articles]
    except Exception as e:
        logger.error(f"Failed to retrieve news articles for constellation {dag_address}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve news articles")

@router.get("/all", response_model=List[NewsArticleResponse])
async def get_all_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    database = Depends(get_database)
):
    try:
        cursor = database.news_articles.find().skip(skip).limit(limit)
        articles = await cursor.to_list(length=limit)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        return [NewsArticleResponse(**article) for article in articles]
    except Exception as e:
        logger.error(f"Failed to retrieve all news articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve news articles")
