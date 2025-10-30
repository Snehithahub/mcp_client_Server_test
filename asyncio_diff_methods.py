import asyncio

async def sprints(num:int):
    print("Timer started-1")
    await asyncio.sleep(1)
    print("Timer done")
    
asyncio.run(sprints(1))


async def mains2():
    async def sprints(num:int):
        print("Timer started-2")
        await asyncio.sleep(3)
        print("Timer done")
    await sprints(1)    
    
asyncio.run(mains2())




async def mains():
    async def sprints(num:int):
        print("Timer started-3")
        await asyncio.sleep(num)
        print("Timer done")
    task_name=asyncio.gather(sprints(2),sprints(5),sprints(2))    
    # task_name=asyncio.create_task(sprints(2))    
    await task_name    
    
asyncio.run(mains())


# #just create_task case
async def main3():
    async def viva(student, time_taken):
        print(f"{student} starts thinking...")
        await asyncio.sleep(time_taken)
        print(f"{student} answers!")
    task1 = asyncio.create_task(viva("A", 3))
    task2 = asyncio.create_task(viva("B", 2))
    task3 = asyncio.create_task(viva("C", 1))
    await task1
    await task2
    await task3

asyncio.run(main3())



# #wait case
async def main():
    async def viva(student, time_taken):
        print(f"{student} starts...")
        await asyncio.sleep(time_taken)
        print(f"{student} done!")

    tasks = [
        asyncio.create_task(viva("A", 3)),
        asyncio.create_task(viva("B", 5)),
        asyncio.create_task(viva("c", 3)),
        asyncio.create_task(viva("D", 3)),
    ]
    done, pending = await asyncio.wait(tasks, timeout=4)
    print("Done:", [t.get_name() for t in done])
    print("Pending:", [t.get_name() for t in pending])

asyncio.run(main())

# #shield case
async def main4():
    async def viva(student):
        try:
            print(f"{student} started (protected)")
            await asyncio.sleep(5)
            print(f"{student} done")
        except asyncio.CancelledError:
            print(f"{student} got cancelled")

    task = asyncio.create_task(viva("A"))  
    try:
        await asyncio.wait_for(asyncio.shield(task), timeout=2)  
        
    except asyncio.TimeoutError:
        print("Main cancelled but shield protected the viva")
    

asyncio.run(main4())


# #semaphore case
async def main5():
    sem = asyncio.Semaphore(2)
    async def viva(student, time_taken):
        async with sem:
            print(f"{student} entered viva room")
            await asyncio.sleep(time_taken)
            print(f"{student} finished viva")

    await asyncio.gather(*(viva(s, i) for s, i in [("A",3), ("B",2), ("C",1), ("D",2)]))

asyncio.run(main5())

# #queue case

async def main6():
    async def producer(queue):
        for i in range(5):
            await asyncio.sleep(1)
            await queue.put(f"Student-{i}")
            print(f"Produced Student-{i}")
        await queue.put(None)

    async def consumer(queue):
        while True:
            student = await queue.get()
            if student is None:
                break
            print(f"Consuming {student}")
            await asyncio.sleep(2)

    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))

asyncio.run(main6())



# #lock case
lock = asyncio.Lock()
score = 0
async def main8():
    async def viva(student):
        global score
        async with lock:
            temp = score
            await asyncio.sleep(1)
            score = temp + 1
            print(f"{student} increased score to {score}")

    await asyncio.gather(*(viva(s) for s in ["A", "B", "C"]))

asyncio.run(main8())




#timeout case
async def main7():
    async def viva(student):
        await asyncio.sleep(5)
        print(f"{student} finished")

    try:
        async with asyncio.timeout(2):
            await viva("A")
    except asyncio.TimeoutError:
        print("A took too long!")

asyncio.run(main7())
