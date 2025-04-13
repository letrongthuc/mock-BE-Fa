from fastapi import FastAPI
from database import Base, engine
from routers import auth

app = FastAPI()

# Tạo bảng trong cơ sở dữ liệu (nếu chưa có)
Base.metadata.create_all(bind=engine)

# Thêm các router vào ứng dụng FastAPI
app.include_router(auth.router)

# Các route khác (nếu có)
@app.get("/")
def read_root():
    return {"message": "Welcome to the API! API is running!"}
