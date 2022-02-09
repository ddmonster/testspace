
import uvicorn
from testspace import create_app
if __name__ == "__main__":
    uvicorn.run(create_app())