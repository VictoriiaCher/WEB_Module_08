import redis
from redis_lru import RedisLRU

from pprint import pprint

from src.models import Quote
import connect

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def input_error(func):
    def wrapper(user_data):
        try:
            return func(user_data)
        except KeyError:
            return f'Wrong command or input data'

    return wrapper


@input_error
def handler(command: str):
    return COMMAND[command]


def main():
    while True:
        user_input = input("Enter the query in format [command:value]: ")
        command, user_data = handle_user_input(user_input)
        output = handler(command)(user_data)
        print(output)


@input_error
def handle_user_input(user_input: str) -> tuple:
    command, user_data = user_input.split(":")[0], user_input.split(":")[1:]
    return command, user_data


@cache
def find_to_name(name: list):  # name:Albert Einstein
    name = name[0].strip()
    quotes = Quote.objects()
    quote_list = []

    for quote in quotes:
        if quote.author.fullname == name:
            quote_list.append(quote.quote)
    return pprint(quote_list)


@cache
def find_to_tag(tag: list):
    result = Quote.objects(tags=tag[0])

    for quote in result:
        print(quote.quote)


@cache
def find_to_tags(tags: list):  # tags:live,life
    tags = tags[0].split(",")
    result = Quote.objects(tags__in=tags)

    for quote in result:
        print(quote.quote)


@input_error
def bye(*args):
    print("Goodbye!")
    return exit()


COMMAND = {
    "name": find_to_name,
    "tag": find_to_tag,
    "tags": find_to_tags,
    "exit": bye

}

if __name__ == "__main__":
    main()
