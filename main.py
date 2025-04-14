#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth

app = FastAPI()

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các origin, bạn có thể thay thế "*" bằng URL cụ thể nếu muốn hạn chế
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

# Tạo bảng trong cơ sở dữ liệu (nếu chưa có)
Base.metadata.create_all(bind=engine)

# Thêm các router vào ứng dụng FastAPI
app.include_router(auth.router)

# Các route khác (nếu có)
@app.get("/")
def read_root():
    return {"message": "Welcome to the API! API is running!"}

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
