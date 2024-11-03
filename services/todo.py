from grpc import aio, StatusCode

from protos import todo_pb2
from protos import todo_pb2_grpc
from model.todo import Todo


class TodoService(todo_pb2_grpc.TodoServiceServicer):
    async def CreateTodo(self, request, context):
        if not (0 <= request.day <= 7):
            context.set_code(StatusCode.INVALID_ARGUMENT)
            context.set_details('0<= day <=7')
            return todo_pb2.CreateTodoResponse()
        todo = await Todo.insert(
            Todo(name=request.name, completed=request.completed, day=request.day)
        )
        print("CreateTodo", )
        return todo_pb2.CreateTodoResponse(todo=todo[0])
    
    async def UpdateTodo(self, request, context):
        todo = await Todo.select().where(Todo.id == request.id).first()
        return todo_pb2.UpdateTodoResponse(todo=todo)
    
    async def DeleteTodo(self, request, context):
        await Todo.delete.where(Todo.id == request.id).first()
        return todo_pb2.DeleteTodoResponse(success=True)
    
    async def GetTodo(self, request, context):
        todo = await Todo.select()
        print("Getting todo list")
        return todo_pb2.GetTodoResponse(todos=todo)
    
    async def RetrieveTodo(self, request, context):
        todo = await Todo.delete.where(Todo.id == request.id).first()
        return todo_pb2.RetrieveTodoResponse(todo=todo)


async def run(address):
    await Todo.create_table(if_not_exists=True)
    server = aio.server()
    todo_pb2_grpc.add_TodoServiceServicer_to_server(
        TodoService(), server
    )
    server.add_insecure_port(address=address)
    print(f"Todo service is running -> (address: {address})")
    await server.start()
    await server.wait_for_termination()
