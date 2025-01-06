import requests
import json
import base64
import numpy as np
import cv2

def handler(environ, start_response):
    context = environ['fc.context']
    request_uri = environ['fc.request_uri']
    for k, v in environ.items():
        if k.startswith("HTTP_"):
            # process custom request headers
            pass

    # get request_body
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)

    # get request_method
    request_method = environ['REQUEST_METHOD']

    # get path info
    path_info = environ['PATH_INFO']
    if(path_info == "/avatar/"):
        
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return "alive"
    uuid = path_info[8:]
    print ('uuid: {}'.format(uuid))
    status = '200 OK'
    response_headers = [('Content-type', 'image/png')]
    start_response(status, response_headers)
    skinurl = "https://sessionserver.mojang.com/session/minecraft/profile/"+uuid.replace("-","")
    print ('skinurl: {}'.format(skinurl))
    r = requests.get(skinurl)
    if r.status_code == 200:
        resp = r.text
        print ('resp: {}'.format(resp))
        b64=json.loads(resp).get('properties')[0].get('value')
        url=json.loads(base64.b64decode(b64)).get('textures').get('SKIN').get('url')
    else: return "empty"
    imgdata = requests.get(url).content
    img=np.array(bytearray(imgdata),dtype=np.uint8)
    img=cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
    cropped=img[8:16,8:16]
    cropped=cv2.resize(cropped,(160,160),interpolation=cv2.INTER_NEAREST)
    print(img.shape)
    cv2.imwrite(uuid+'.png',cropped)
    return [open(uuid+'.png','rb').read()]
