from prefect import flow, task

@task
def add(a: int, b: int) -> int:
    return a + b

@flow(name="demo-flow")
def demo_flow():
    x = add.submit(1, 2).result()
    print("Result:", x)

if __name__ == "__main__":
    demo_flow()
