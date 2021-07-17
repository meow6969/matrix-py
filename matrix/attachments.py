import os
import magic
import aiofiles.os


async def send_attachment(client, room_id, image):
    """Send image to room.

    Arguments:
    ---------
    client : Client
    room_id : str
    image : str, file name of image

    This is a working example for a JPG image.
        "content": {
            "body": "someimage.jpg",
            "info": {
                "size": 5420,
                "mimetype": "image/jpeg",
                "thumbnail_info": {
                    "w": 100,
                    "h": 100,
                    "mimetype": "image/jpeg",
                    "size": 2106
                },
                "w": 100,
                "h": 100,
                "thumbnail_url": "mxc://example.com/SomeStrangeThumbnailUriKey"
            },
            "msgtype": "m.image",
            "url": "mxc://example.com/SomeStrangeUriKey"
        }

    """
    # get the type of media
    mime_type = magic.from_file(image, mime=True)  # e.g. "image/jpeg"
    media_type = mime_type.split('/')[0]
    # print(media_type)
    # get the name of the image for the body argument
    image_name = image.split('/')[len(image.split('/')) - 1]
    # check if the file is a video or image, and if not wont make a thumbnail for it
    do_thumb = True
    if media_type != 'video' and media_type != 'image':
        do_thumb = False
    # get the size of the file in bytes
    file_stat = await aiofiles.os.stat(image)
    # fill in stuff
    height = 0
    width = 0
    thumb_type = 'other'
    # if the file is a video or picture
    if do_thumb:
        # get the dimensions of the file
        meow = os.popen(
            f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height '
            f'-of csv=s=x:p=0 "{image}"').read()  # this returns a intxint string thingy for example "420x69"

        meowe = meow.split('x')
        width = meowe[0]
        height2 = meowe[1]
        # make a thumbnail for the file
        os.system(f'ffmpeg -i "{image}" -hide_banner -loglevel error -frames:v 1 -y "./temp/{image_name}.png"')
        # get the file type of the thumbnail
        thumb_type = magic.from_file(f'./temp/{image_name}.png', mime=True)
        # make sure the height variable is only numbers
        height = ''
        for m in height2:
            if m in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                height += m

        # first do an upload of image, then send URI of upload to room
        thumb_stat = await aiofiles.os.stat(f'./temp/{image_name}.png')
        async with aiofiles.open(f'./temp/{image_name}.png', "r+b") as f:
            resp2, maybe_keys2 = await client.upload(
                f,
                content_type=thumb_type,  # image/jpeg
                filename=os.path.basename(f'./temp/{image_name}.png'),
                filesize=thumb_stat.st_size)

    async with aiofiles.open(image, "r+b") as f:
        resp, maybe_keys = await client.upload(
            f,
            content_type=mime_type,  # image/jpeg
            filename=os.path.basename(image),
            filesize=file_stat.st_size)

    if do_thumb:
        content = {
            "body": os.path.basename(image),  # descriptive title
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
                "thumbnail_info": {
                    "h": height,
                    "mimetype": thumb_type,
                    "size": 76925,
                    "w": width
                },
                "w": width,  # width in pixel
                "h": height,  # height in pixel
                "thumbnail_url": resp2.content_uri,  # TODO
            },
            "msgtype": f"m.{media_type}",
            "url": resp.content_uri,
        }
    else:
        content = {
            "body": os.path.basename(image),  # descriptive title
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
            },
            "msgtype": f"m.{media_type}",
            "url": resp.content_uri,
        }
    # print(media_type)

    try:
        await client.room_send(
            room_id,
            message_type="m.room.message",
            content=content
        )
        # print("Image was sent successfully")
    except Exception as e:
        print(f"Image send of file {image} failed.\nError: {e}")
