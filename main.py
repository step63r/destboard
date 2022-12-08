import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BaseSettings
from typing import Any, Dict, List, Union

from lib.waveshare_epd import epd7in5_V2
from DestBoardTable import DestBoardTable


class Settings(BaseSettings):
    """
    Settings format.

    Parameters
    ----------
    BaseSettings : BaseSettings
        pydantic model class
    """
    table_row: int = 6
    table_column: int = 2
    margin_width: int = 5
    margin_height: int = 5
    padding_left: int = 5
    padding_top: int = 5
    cell_name_ratio: float = 0.3

    class Config:
        env_file = '.env', 'prod.env', 'stg.env', 'dev.env'
        env_file_encoding = 'utf-8'


class PostItem(BaseModel):
    """
    HTTP PUT request body format.

    Parameters
    ----------
    BaseModel : BaseModel
        pydantic model class.
    """
    name: Union[str, None] = None
    status: Union[str, None] = None
    present: Union[bool, None] = None


settings = Settings(_env_file='dev.env', _env_file_encoding='utf-8')
app = FastAPI()
epd = epd7in5_V2.EPD()

# configure CORS.
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["X-Requested-With", "X-HTTP-Method-Override", "Content-Type", "Accept"]
)

table = DestBoardTable(
        epd.width, epd.height,
        settings.margin_width, settings.margin_height,
        settings.padding_left, settings.padding_top,
        settings.table_row, settings.table_column, settings.cell_name_ratio,
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 36,
        './table.json')


@app.on_event("startup")
async def startup_event():
    epd.init()
    epd.Clear()
    epd.display(epd.getbuffer(table.Himage))


@app.on_event("shutdown")
async def shutdown_event():
    epd.init()
    epd.Clear()
    epd.sleep()


@app.post("/{row}/{column}")
async def set(row: int, column: int, item: PostItem):
    if not item.name is None:
        table.set_name(column, row, item.name)
    if not item.status is None:
        table.set_status(column, row, item.status)
    if not item.present is None:
        table.set_present(column, row, item.present)
    
    epd.display(epd.getbuffer(table.Himage))
    return {"status": "update success."}


@app.get("/{row}/{column}")
async def get(row: int, column: int) -> Dict[str, Any]:
    return {
        "name": table.get_name(column, row),
        "status": table.get_status(column, row),
        "present": table.get_present(column, row)}

@app.get("/")
async def root() -> List[List[Dict[str, Any]]]:
    return table.get_all()

if __name__ == '__main__':
    # start http server
    uvicorn.run(app)
