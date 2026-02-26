from init import app,base,engine
import uvicorn
import asyncio
from routers.data_ingestion_routes import data_ingestion_routes
from routers.orders_route import orders_router
from utils.helper import update_order_status
from fastapi.middleware.cors import CORSMiddleware

app.include_router(router=data_ingestion_routes)
app.include_router(router=orders_router)
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_headers=['*'])

async def periodic_task():
    while True:
        update_order_status()
        await asyncio.sleep(60*5)  # 5 minutes

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_task())

if __name__=='__main__':
    base.metadata.create_all(bind=engine)
    uvicorn.run('main:app',reload=True)