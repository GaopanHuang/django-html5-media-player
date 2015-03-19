from django.shortcuts import render
import os
from yattag import Doc
from django.contrib.auth.decorators import login_required
from models import MediaServer

def display_directory(path, server, doc):
    tag = doc.tag
    text = doc.text
    if os.path.isdir(path):
        cssid = path[len(server.directory_path):]
        doc.asis('<label for="'+cssid+'">')
        text(os.path.basename(path))
        doc.asis('</label>')
        doc.asis('<input type="checkbox" id="'+cssid+'">')
        with tag('ul', klass='collapsibleList'):
            for x in sorted(os.listdir(path)):
                with tag('li'):
                    display_directory(os.path.join(path,x), server, doc)
    else:
        url_paths = {'V':'/media_player/video/',
                     'A':'/media_player/audio/'}
        urlpath = url_paths[server.media_type] + server.name + path[len(server.directory_path):]
        with tag('a', href=urlpath):
            text(os.path.splitext(os.path.basename(path))[0])

@login_required
def media_player(request, media_src=''):
    doc, tag, text = Doc().tagtext()
    types = {'video':'V', 'audio':'A'}
    requested_type = media_src.split('/')[0]
    media_servers = MediaServer.objects.filter(media_type=types[requested_type])
    image_src = ''
    if len(media_src.split('/')) >= 2:
        requested_server = media_src.split('/')[1]
    else:
        requested_server = ''
    for server in media_servers:
        if server.name == requested_server:
            media_src = server.server_url + media_src[len(requested_type + '/' + requested_server):]
            parent_dir = server.directory_path + os.path.split(media_src)[0][len(server.server_url):]
            for item in os.listdir(parent_dir):
                if os.path.splitext(item)[1].lower() in ['.jpg','.png']:
                    image_src = os.path.join(os.path.split(media_src)[0],item)
        display_directory(server.directory_path, server, doc)
    context = { 'medialisting':doc.getvalue(), 
                'mediasource':media_src, 
                'mediatype':requested_type, 
                'imagesource':image_src,
              }
    return render(request, 'media_player/media_player.html', context)
