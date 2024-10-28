import time

def task(task_num, duration):
    print(f"started {task_num}")
    time.sleep(duration)
    print(f"ended {task_num}")

def main():
    begin = time.time()
    task1 = (1, 3)
    task2 = (2, 2)
    task3 = (3, 1)

    task(*task1)
    task(*task2)
    task(*task3)
    end = time.time()

    print(f"Task time is {end - begin}")

main()


# async
import asyncio

#async함수
async def async_task(task_num, duration):
    print(f"started {task_num}")
    await asyncio.sleep(duration)
    print(f"ended {task_num}") 

async def main():
    task1 = asyncio.create_task(async_task(1,3))
    task2 = asyncio.create_task(async_task(2,2))
    task3 = asyncio.create_task(async_task(3,1))
                                
    await task1
    await task2
    await task3

async def gather_main():
    await asyncio.gather(
        async_task(1,3),
        async_task(2,2),
        async_task(3,1),
    )

begin = time.time()
#asyncio.run(main())
end = time.time()

print(f"Async time is {end - begin}")

#fetch
import requests
import aiohttp

def fetch(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response

def main():
    urls = []
    for url in urls:
        response = fetch(url)

if __name__ == "__main__":
    main()
    
#####
async def afetch(url, session):
    response = await session.get(url)

    if response.status_code == 200:
        #do something here

    await response.release()

async def main():
    session = aiohttp.ClientSession()

    tasks = [afetch(url, session) for url in urls]

    result = await asyncio.gather(*tasks)

    await session.close()

if _name__ == "_main__":
    asyncio.run(main())
