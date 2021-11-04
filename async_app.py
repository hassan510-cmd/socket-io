import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': './public/'
})

client_count=0
room_1=0
room_2=0
async def task(sid):
    await sio.sleep(5)
    result= await sio.call('sub',{'numbers':[10,5]},to=sid)
    print(f'task done with {result}')

@sio.event
async def connect(sid, environ):
    print(sid, 'connected')
    global client_count
    global room_1
    global room_2
    # username=environ.get('HTTP_X_USERNAME')
    # print(f'username : {username}')
    # if not username:
    #     return False
    username = environ.get('HTTP_X_USERNAME')
    print('username:', username)
    if not username:
        pass
    # async with sio.session(sid) as session:
    #     session['username']=username
    # await sio.emit('user_join',username)
    async with sio.session(sid) as session:
        session['username'] = username
    await sio.emit('user_joined', username)
    client_count+=1
    sio.start_background_task(task,sid)
    await sio.emit('client_count',client_count)
    if client_count>2:
        sio.enter_room(sid,'room2')
        room_2+=1
        await sio.emit('room_count',f"room_2:#{room_2}",to='room2')
    else:
        sio.enter_room(sid,'room1')
        room_1+=1
        await sio.emit('room_count',f"room_1:#{room_1}",to='room1')


@sio.event
async def disconnect(sid):
    global client_count
    global room_1
    global room_2
    client_count-=1
    print(sid, 'disconnected')
    await sio.emit('client_count', client_count)
    if 'room_1' in sio.rooms(sid):
        room_1-=1
        await sio.emit('room_count', f"room_1:#{room_1}", to='room1')
    else:
        room_2-=1
        await sio.emit('room_count', f"room_2:#{room_2}", to='room2')
    # async with sio.session(sid) as session:
    #    await sio.emit('user_left',session['username'])
    async with sio.session(sid) as session:
        await sio.emit('user_left', session['username'])
@sio.event
async def sum_data(sid,data):
    sum_result=sum(data['nums'])
    await sio.emit('sum_result',{'result':sum_result},to=sid)
@sio.event
async def mul_data(sid,data):
    sum_result=sum(data['nums'])
    return sum_result