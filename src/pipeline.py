from src import extract, transform, load


def run():
    print("Step 1/3: extract")
    extract.run()
    print("Step 2/3: transform")
    transform.run()
    print("Step 3/3: load")
    load.run()
    print("Pipeline finished")


if __name__ == "__main__":
    run()