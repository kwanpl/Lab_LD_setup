import asyncio

async def asynchronous_function():
    print("Start")
    await asyncio.sleep(20)  # Non-blocking wait
    print("End")

asyncio.run(asynchronous_function())
