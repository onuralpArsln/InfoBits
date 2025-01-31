import threading
import asyncio

def multithreading_race_condition():
    counter2 = 0

    def increment():
        nonlocal counter2
        for _ in range(10000):  
            counter2 = counter2 + 1

    threads = [threading.Thread(target=increment) for _ in range(3)]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Multithreading Final Counter: {counter2}")

async def asyncio_race_condition():
    counter3 = 0

    async def increment():
        nonlocal counter3
        for _ in range(10000):
            counter3 = counter3 + 1

    tasks = [asyncio.create_task(increment()) for _ in range(3)]
    
    await asyncio.gather(*tasks)
    
    print(f"Asyncio Final Counter: {counter3}")

def main():
    print("\nMultithreading Example:")
    multithreading_race_condition()

    print("\nAsyncio Example:")
    asyncio.run(asyncio_race_condition())

if __name__ == "__main__":
    main()