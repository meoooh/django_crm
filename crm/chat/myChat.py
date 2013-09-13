# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080.
"""
import tornado.ioloop
import tornado.web

import sockjs.tornado
import os
import sys

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '..') )
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_crm.settings'
from crm.models import *
import simplejson
from django.contrib.sessions.models import Session
from crm.utility import printException


def getUser(s):
    # import ipdb;ipdb.set_trace()
    try:
        session = Session.objects.get(session_key=s)
        uid = session.get_decoded().get('_auth_user_id')
        return User.objects.get(pk=uid)
    except:
        printException(sys.exc_info())
        print "\n\n\n\ngetUser except!!\n\n\n\n"
        print "\n\n\n\ns: "+s+"\n\n\n\n"
        # exit()


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()
    room = dict()

    def on_open(self, info):
        # import ipdb;ipdb.set_trace()
        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
        # Broadcast message
        # import ipdb;ipdb.set_trace()
        message = simplejson.loads(message)  # ['join',{'join': roomId}]
        sess = self.session.conn_info.cookies['sessionid'].value

        if message[0] == 'msg':  # 채팅시 ['msg',{'roomId': roomId, 'msg':'바보'}]
            message = message[1]
            try:
                user = getUser(sess)
                chatRoom = ChatRoom.objects.get(pk=message['roomId'])
            except:
                printException(sys.exc_info())
                print "\n\ncrm.chat.myChat.py except1\n\n"

            try:
                chatMessage = ChatMessage.objects.create(
                    message=message['msg'],
                    writer=user,
                    room=chatRoom,
                )
            except:
                printException(sys.exc_info())
                print "\n\ncrm.chat.myChat.py except2\n\n"

            ret = []  # ['msg']
            ret.append('msg')
            ret.append({})
            ret[1]['id'] = chatMessage.writer.username
            ret[1]['name'] = chatMessage.writer.get_profile().name
            ret[1]['msg'] = chatMessage.message
            ret[1]['date'] = chatMessage.date.isoformat()
            ret[1]['pk'] = chatMessage.pk

            self.broadcast(self.room[message['roomId']], simplejson.dumps(ret))
        elif message[0] == 'read':
            # import ipdb;ipdb.set_trace()
            message = message[1]

            try:
                user = getUser(sess)
            except:
                printException(sys.exc_info())
                print "\n\ncrm.chat.myChat.py except3\n\n"

            chatMessage = ChatMessage.objects.get(pk=message['msgPk'])
            chatMessage.isRead.add(user)
        elif message[0] == 'typing':
            # import ipdb;ipdb.set_trace()
            roomId = message[1]['roomId']

            ret = ['typing', getUser(sess).get_profile().name]

            self.broadcast(self.room[roomId], simplejson.dumps(ret))
        elif message[0] == 'noti':  # JSON 형식: ['noti', ['msg', {'roomId': roomId}]]
            # import ipdb;ipdb.set_trace()
            # message = message[1]

            if message[1][0] == 'msg':
            # if message[0] == 'msg':
                # message = message[0]

                try:
                    chatRoom = ChatRoom.objects.get(pk=message[1][1]['roomId'])
                except:
                    print "\n\ncrm.chat.myChat.py except4\n\n"
                    printException(sys.exc_info())
                    print "\n\ncrm.chat.myChat.py except5\n\n"
                    return

                users = chatRoom.participants.all()

                for u in self.participants:
                    if getUser(u.session.conn_info.cookies['sessionid'].value) in users:
                        u.send(simplejson.dumps(message))
            elif message[1][0] == 'mail':
                pass
            else:
                pass
        elif message[0] == 'join':  # 입장시 ['join',{'join': roomId}]
            # import ipdb;ipdb.set_trace()
            roomId = message[1]['join']

            if not self.room.get(roomId, False):
                self.room[roomId] = set()
            self.room[roomId].add(self)
        else:
            print "\n\nmyChat.py on_message else6\n\n"

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        # print "클로즈!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        self.participants.remove(self)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # import ipdb;ipdb.set_trace()
    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')

    # 2. Create Tornado application
    app = tornado.web.Application(
        [(r"/", IndexHandler)] + ChatRouter.urls
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(7070)
    
    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
