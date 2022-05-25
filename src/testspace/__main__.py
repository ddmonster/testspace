

from sqlalchemy import true
import uvicorn
from testspace import app,config
from pathlib import Path

cur_dir = Path(__file__).parent
if __name__ == "__main__":
    uvicorn.run("testspace:app", reload = True)