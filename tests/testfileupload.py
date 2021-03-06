import asyncio
import os
from nio import AsyncClient, MatrixRoom, RoomMessageText
import matrix
import json
import can


async def gamer(client):
    await matrix.message(client, "!VgklaNdKhnLIVsWfwr:matrix.org", 'startng test')

    for i in os.listdir('./teststuff'):
        print(i)

        await matrix.send_attachment(client, "!VgklaNdKhnLIVsWfwr:matrix.org", f'{os.getcwd()}/teststuff/{i}')


async def main() -> None:
    m = json.load(open('credentials.json'))
    client = await matrix.login(m['homeserver'], m['name'], m['password'])
    # "Logged in as @alice:example.org device id: RANDOMDID"

    # If you made a new room and haven't joined as that user, you can use
    # await client.join("your-room-id")

    # await client.room_send(
    #    # Watch out! If you join an old room you'll see lots of old messages
    #    room_id="!DlFkejMVdqOcXazTVB:matrix.org",
    #    message_type="m.room.message",
    #    content={
    #        "msgtype": "m.text",
    #        "body": "Hello world!"
    #    }
    # )
    await gamer(client)

    await client.sync_forever(timeout=30000)  # milliseconds


listener = can.Listener()
try:
    listener.on_message_received(asyncio.get_event_loop().run_until_complete(main()))
except KeyboardInterrupt:
    pass

