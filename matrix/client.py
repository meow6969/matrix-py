import nio


async def login(homeserver, name, password):
    if not homeserver.startswith("https://") or homeserver.startswith("http://"):
        homeserver = "https://" + homeserver
    if not name.startswith('@'):
        name = '@' + name
    client = nio.AsyncClient(homeserver, name)

    print(await client.login(password))
    return client
