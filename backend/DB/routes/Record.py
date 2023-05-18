from typing import Optional
import uuid
from datetime import date
from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    idnumber: int
    birthday: str
    phone: int
    exday: str
    image: str
    rsimage:str
    label: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Learn FARM Stack",
                "idnumber": 123456,
                "birthday": "07/10/2001",
                "phone":    123456,
                "exday": "07/10/2001",
                "image": "",
                "rsimage":"",
                "label":""
            }
        }


class UpdateTaskModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    idnumber: Optional[int]
    birthday: Optional[str]
    exday: Optional[str]
    image: Optional[str]
    rsimage:Optional[str]
    label : Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Learn FARM Stack",
                "idnumber": 123456,
                "birthday": "07/10/2001",
                "phone":    123456,
                "exday": "07/10/2001",
                "image": "",
                "rsimage":"",
                "label" :""
            }
        }

from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.get("/allrecord/", response_description="List all Record")
async def list_tasks(request: Request):
    tasks = []
    for doc in await request.app.mongodb["Record"].find().to_list(length=100):
        tasks.append(doc)
    return tasks


@router.get("/record/{id}", response_description="Get a single Record")
async def show_task(id: str, request: Request):
    if (task := await request.app.mongodb["Record"].find_one({"_id": id})) is not None:
        return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.post("/addrecord/", response_description="Add new Record")
async def create_task(request: Request, task: TaskModel = Body(...)):
    task = jsonable_encoder(task)
    new_task = await request.app.mongodb["Record"].insert_one(task)
    created_task = await request.app.mongodb["Record"].find_one(
        {"_id": new_task.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)


@router.put("/updaterecord/{id}", response_description="Update a Record")
async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
    task = {k: v for k, v in task.dict().items() if v is not None}

    if len(task) >= 1:
        update_result = await request.app.mongodb["Record"].update_one(
            {"_id": id}, {"$set": task}
        )

        if update_result.modified_count == 1:
            if (
                updated_task := await request.app.mongodb["Record"].find_one({"_id": id})
            ) is not None:
                return updated_task

    if (
        existing_task := await request.app.mongodb["Record"].find_one({"_id": id})
    ) is not None:
        return existing_task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/deleterecord/{id}", response_description="Delete Task")
async def delete_task(id: str, request: Request):
    delete_result = await request.app.mongodb["Record"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")