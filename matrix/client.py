import nio

class client:
    pass

async def login(homeserver, name, password):
    if not homeserver.startswith("https://") or homeserver.startswith("http://"):
        homeserver = "https://" + homeserver
    if not name.startswith('@'):
        name = '@' + name
    _client = nio.AsyncClient(homeserver, name)

    print(await _client.login(password))
    return _client


async def message(client, room, text):
    content = {
        "body": text,
        "msgtype": 'm.text'
    }
    await client.room_send(
        room,
        message_type="m.room.message",
        content=content
    )

async def start():
    pass
