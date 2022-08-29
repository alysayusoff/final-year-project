import json
import os
import sys
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import *

class CompilerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['query_string'].decode("utf-8").replace('username=', '')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_type = self.scope['url_route']['kwargs']['room_type']
        groupname = self.room_type + self.room_name
        self.room_group_name = 'chat_%s' % groupname
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        receive_type = data['receive_type']
        # user enters room
        if (receive_type == 'enter'):
            username = data['username']
            message = data['message']

            participants = await self.get_participants(self.room_name, self.room_type)

            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'update_users',
                'participants': participants,
                'username': username,
                'message': message
            })
        # user exits room
        if (receive_type == 'exit'):
            username = data['username']
            message = data['message']

            participants = await self.remove_user_from_room(self.user, self.room_name, self.room_type)

            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'update_users',
                'participants': participants,
                'username': username,
                'message': message
            })
        # user sends a message
        if (receive_type == 'chat'):
            username = data['username']
            message = data['message']

            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat',
                'username': username,
                'message': message
            })
        # user types on compiler/compiles code
        if (receive_type == 'compiler'):
            runCode = data['runCode']
            code = data['code']

            if (runCode == False):
                await self.channel_layer.group_send(self.room_group_name, {
                    'type' : 'compiler',
                    'code' : code,
                    'runCode' : runCode
                })
            else:
                file = self.room_name + '_compiled.txt'
                try:
                    original_stdout = sys.stdout
                    sys.stdout = open(file, 'w')
                    exec(code)
                    sys.stdout.close()
                    sys.stdout = original_stdout
                    output = open(file, 'r').read()
                    os.remove(file)
                except Exception as e:
                    sys.stdout = original_stdout
                    output = str(e)

                await self.channel_layer.group_send(self.room_group_name, {
                    'type' : 'compiler',
                    'code' : code,
                    'output' : output,
                    'runCode' : runCode
                })

    async def update_users(self, event):
        participants = event['participants']
        username = event['username']
        message = event['message']

        await self.send(text_data=json.dumps({
            'receive_type': 'update_users',
            'participants': participants,
            'username': username,
            'message': message
        }))

    async def chat(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'receive_type': 'chat',
            'username': username, 
            'message': message
        }))

    async def compiler(self, event):
        code = event['code']
        runCode = event['runCode']

        if (runCode == False):
            await self.send(text_data=json.dumps({
                'receive_type': 'compiler',
                'code' : code,
                'runCode' : runCode
            }))
        else:
            output = event['output']
            await self.send(text_data=json.dumps({
                'receive_type': 'compiler',
                'code' : code,
                'output' : output,
                'runCode' : runCode
            }))

    @sync_to_async
    def get_participants(self, room_name, room_type):
        try:
            return list(Room.objects.get(room_name=room_name, type=room_type).get_participants().values('username'))
        except Exception as e:
            print("@sync_to_async get_participants() threw an error:", e)

    @sync_to_async
    def remove_user_from_room(self, username, room_name, room_type):
        try:
            # delete user
            room = Room.objects.get(room_name=room_name, type=room_type)
            Participant.objects.get(username=username, room=room).delete()
            # check the number of participants in a room, if zero, delete room
            if (room.get_number_of_participants() == 0):
                room.delete()
            # if not, return participants
            else:
                return list(room.get_participants().values('username'))
        except Exception as e:
            print("@sync_to_async remove_user_from_room() threw an error:", e)
        