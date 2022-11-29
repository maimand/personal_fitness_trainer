from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.student import router as StudentRouter
from routes.super_admin import router as SuperAdminRouter
from routes.user import router as UserRouter
from routes.exercises import router as ExercisesRouter
from routes.logs import router as LogsRouter
from routes.diet import router as DietRouter

app = FastAPI()

token_listener = JWTBearer()

add_pagination(app)

@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
app.include_router(SuperAdminRouter, tags=["Super Admin"], prefix="/super-admin",)
app.include_router(UserRouter, tags=["Users"], prefix="/user", )
app.include_router(ExercisesRouter, tags=["Exercises"], prefix="/exercises", )
app.include_router(DietRouter, tags=["Diet"], prefix="/diet", )
app.include_router(LogsRouter, tags=["Logs"], prefix="/logs", )
