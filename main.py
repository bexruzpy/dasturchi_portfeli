from fastapi import FastAPI
from routers import auth, users, projects, skills, connections, public_profile

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(connections.router)
app.include_router(public_profile.router)
