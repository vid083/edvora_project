import socketio, json
# from socketIO_client import SocketIO


sio = socketio.Client(logger=True, engineio_logger=True)  
url = 'http://0.0.0.0:8000'
isConnected = True

# Handshake
try:
    print('trying to connect')
    sio.connect('http://localhost:8000')
except:
    isConnected = False
if isConnected == True:  
    data = json.dumps({'eventid': '12345','application': 'MyApp','version': '1.0.0'})         
    sio.emit('manual_connection_parameter', data)
else:
    print("NO connection")
@sio.event
def connect(data):
    data = json.loads(data)
    print('\nConnect Confirm = ', data)
    
@sio.event
def start_list(data):
    data = json.loads(data)
    print('\nStart List = ', data)

@sio.event
def connect_error(data):
    print("The connection failed!")

sio.wait()