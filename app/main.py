from fastapi import FastAPI, status, HTTPException
import uvicorn
import os
import time

from app.models.models import Group

app = FastAPI()

group_set = set()


@app.get("/", status_code=200)
async def read_root():
    return "Welcome to Swisscom test site!"


@app.get("/timeout/")
async def read_timeout():
    time.sleep(6)
    return "Welcome to timeout after 6 sec!"


@app.post("/v1/group/", status_code=status.HTTP_201_CREATED)
async def create_group(
        create_group: Group
):
    if create_group.groupId in group_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request. Perhaps the object exists."
        )
    else:
        group_set.add(create_group.groupId)
    return {"message": "Group created"}


@app.delete("/v1/group/", status_code=status.HTTP_200_OK)
async def delete_group(
    delete_group: Group
):
    if delete_group.groupId in group_set:
        group_set.remove(delete_group.groupId)
        return {"message": "Group deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request. Perhaps the object doesn't exists."
        )


@app.get("/v1/group/{groupId}", status_code=status.HTTP_200_OK)
async def get_group(groupId: str):
    if groupId in group_set:
        return Group(groupId=groupId)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object doesn't exist."
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('NODE_PORT')))