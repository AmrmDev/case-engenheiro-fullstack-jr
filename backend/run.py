import sys
import os
from app.database import engine, Base

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
Base.metadata.create_all(bind=engine)


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
