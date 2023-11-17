
from fastapi import FastAPI, HTTPException, Depends, status
from httpx import AsyncClient

async def get_bearer_token():
    return "your lichess api"



async def fetch_rating_history(username: str, bearer_token: str = Depends(get_bearer_token)):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"pref": "Bullet"}
    url = f"https://lichess.org/api/user/{username}/rating-history?pref=%22Bullet%22"
    async with AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            print(response)
            response.raise_for_status() 
            data = response.json()
            print(data)
            return data
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")
