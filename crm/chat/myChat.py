# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080.
"""
import tornado.ioloop
import tornado.web

import sockjs.tornado
import os
import sys

sys.path.append('/root/django_crm')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_crm.settings'
from crm.models import *
import simplejson
from django.contrib.sessions.models import Session
from crm.utility import printException


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        # import ipdb;ipdb.set_trace()
        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
        # Broadcast message
        # import ipdb;ipdb.set_trace()
        message = simplejson.loads(message)
        try:
            # 세션값으로 User 얻기(이부분 mysql로 하면 에러난다...)
            session_key = self.session.conn_info.cookies['sessionid'].value
            
            ##### 에러방지를 위한 임시코드 시작 ###
            User.objects.create(username='tmp')
            User.objects.get(username='tmp').delete()
            ##### 에러방지를 위한 임시코드 끝 ###

            session = Session.objects.get(session_key=session_key)  # 여기서 세션값을 가져오지 못하는 에러가 있음... 그런데 db insert 작업후에는 정상적으로 가져옴...
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
            # 참조
            # https://www.facebook.com/groups/django/permalink/518594774843693/
            # https://www.facebook.com/groups/django/permalink/529096727126831/
            # http://scottbarnham.com/blog/2008/12/04/get-user-from-session-key-in-django/

            chatRoom = ChatRoom.objects.get(pk=message['roomId'])
        except:
            print
            print
            print self.session.conn_info.cookies['sessionid'].value
            printException(sys.exc_info())
            print "crm.chat.myChat.py except!!!!!!!!!!!!!!!!!!!!!!!!!"
            print
            print
            print
            print
            print
            print
            return

        try:
            chatMessage = ChatMessage.objects.create(
                message=message['msg'],
                writer=user,
                room=chatRoom,
            )
        except:
            return

        ret = {}
        ret['id'] = chatMessage.writer.username
        ret['name'] = chatMessage.writer.get_profile().name
        ret['msg'] = chatMessage.message
        ret['date'] = chatMessage.date.isoformat()

        self.broadcast(self.participants, simplejson.dumps(ret))

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
