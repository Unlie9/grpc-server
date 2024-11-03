import typing as t
from fastapi import Depends, FastAPI, status, HTTPException, Security, Query
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from clients import grpc_todo_client
from protos import todo_pb2
from google.protobuf.json_format import MessageToDict
from grpc.aio._call import AioRpcError
from google.protobuf import empty_pb2


app = FastAPI()


@app.get("/")
async def ping():
    return {"ping": True}


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    name: str,
    completed: bool,
    day: int= Query(ge=1),
    client: t.Any = Depends(grpc_todo_client)
) -> JSONResponse:
    
    try:
        todo = await client.CreateTodo(
            todo_pb2.CreateTodoRequest(
                name=name,
                completed=completed,
                day=day,
            ), timeout=5
        )
    except AioRpcError as e:
        raise HTTPException(status_code=400, detail=e.details())

    return JSONResponse(MessageToDict(todo))

@app.put("/{id:int}", status_code=status.HTTP_200_OK)
async def update_todo(
    id: int,
    name: str,
    completed: bool,
    client: t.Any = Depends(grpc_todo_client)
):
    todo = await client.UpdateTodo(
        todo_pb2.UpdateTodoRequest(
            id=id,
            name=name,
            completed=completed,
        )
    )
    return JSONResponse(MessageToDict(todo))

@app.get("/todo-list")
async def get_todo(client: t.Any = Depends(grpc_todo_client)) -> JSONResponse:
    try:
        list = await client.GetTodo(todo_pb2.GetTodoRequest())
        return JSONResponse(MessageToDict(list))
    except NotImplementedError:
        print("Error")
    except AioRpcError as e:
        raise HTTPException(status_code=404, detail=e.details())
