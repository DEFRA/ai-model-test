from logging import getLogger

from fastapi import APIRouter, HTTPException, Query

from app.utils.vectorstore_client import VectorStoreClient

logger = getLogger(__name__)

router = APIRouter()

urls = ["https://www.gov.uk/find-funding-for-land-or-farms/clig3-manage-grassland-with-very-low-nutrient-inputs"]

@router.get("/data/search")
async def search_data(query: str = Query(..., description="The query string for similarity search"), k: int = Query(1, description="Number of results to return")):
    """
    Perform a similarity search using the provided query string.
    """
    try:
        client = VectorStoreClient()
        results = client.similarity_search(query=query, k=k)
        logger.info(f"Similarity search results for query '{query}': {results}")

        return {
            "status": "success",
            "query": query,
            "results": results
        }

    except Exception as e:
        logger.exception("Failed to perform similarity search")
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/data/setup")
async def setup_data():
    try:
        client = VectorStoreClient()
        client.load_documents(urls)

        results = client.similarity_search(query="SFI Payments", k=1)
        logger.info(f"Similarity search results: {results}")

        return {
            "status": "success",
        }

    except Exception as e:
        logger.exception("Failed to setup data")
        raise HTTPException(status_code=500, detail=str(e)) from e