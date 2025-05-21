# -*- coding: utf-8 -*-
import logging
import json
import urllib.request
import base64

logger = logging.getLogger()

def handler(event, context):
    # 解析 event 中的查询参数
    event_data = json.loads(event)
    params = event_data.get('queryParameters', {})
    player_name = params.get('name', None)

    if not player_name:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Missing player name parameter'})
        }

    try:
        # 获取玩家 UUID
        with urllib.request.urlopen(f'https://api.mojang.com/users/profiles/minecraft/{player_name}') as response:
            uuid_data = json.loads(response.read())
            player_uuid = uuid_data['id']

        # 获取玩家皮肤 URL
        with urllib.request.urlopen(f'https://sessionserver.mojang.com/session/minecraft/profile/{player_uuid}') as response:
            profile_data = json.loads(response.read())

        # 解析 properties 中的 textures 数据
        properties = profile_data.get('properties', [])
        textures_data = None

        for prop in properties:
            if prop.get('name') == 'textures':
                textures_data = json.loads(base64.b64decode(prop.get('value')).decode())
                break

        if textures_data and 'textures' in textures_data and 'SKIN' in textures_data['textures']:
            skin_url = textures_data['textures']['SKIN']['url']
        else:
            raise Exception("Skin URL not found in textures data")

        # 下载皮肤图片
        with urllib.request.urlopen(skin_url) as skin_response:
            skin_image = skin_response.read()

        # 返回皮肤图片作为响应
        return {
            'isBase64Encoded': True,
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png'
            },
            'body': base64.b64encode(skin_image).decode('utf-8')
        }
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Internal server error'})
        }
