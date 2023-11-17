from fastapi import HTTPException,Depends
from httpx import AsyncClient
from fastapi import APIRouter

router = APIRouter()

async def get_bearer_token():
    return "your lichess api"

@router.get("/top-players")
async def top_players(bearer_token: str = Depends(get_bearer_token)):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = f"https://lichess.org/api/player/top/50/bullet"
    async with AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            return data
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")
