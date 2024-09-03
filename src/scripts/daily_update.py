import asyncio
from time import time

from ..config.logging import info
from ..data.pipeline import execute_data_pipelines
from ..models.train_models import train_all_models

async def time_function(func, *args, **kwargs):
    start_time = time()
    result = await func(*args, **kwargs)
    end_time = time()
    duration = end_time - start_time
    info(f'{func.__name__} completed. Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)')
    return result

async def daily_update():
    execute_data_pipelines()
    await time_function(train_all_models)

if __name__ == '__main__':
    asyncio.run(daily_update())
