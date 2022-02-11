
from importlib import reload
import uvicorn
from testspace import app

if __name__ == "__main__":
    uvicorn.run(app)