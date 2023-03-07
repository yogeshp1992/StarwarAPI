"""
We either want to created multiple processes

** OR **

We want to create multiple threads to achieve the same task


"""


import requests
import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        print(f"[ INFO ] total time to execute :: {end}")
        return result

    return wrapper


"""

thread-1  https://swapi.dev/api/people/1
thread-2  https://swapi.dev/api/people/2
thread-3  https://swapi.dev/api/people/3
...
...
thread-10  https://swapi.dev/api/people/10

"""


@timeit
def main():

    final = []
    for i in range(1, 5):
        magic_url = f"https://swapi.dev/api/people/{i}"
        response = requests.get(magic_url)    # HTTP GET request - IO operation
        data = response.json()
        char_name = data.get("name")
        final.append(char_name)

    print(final)


if __name__ == "__main__":
    main()