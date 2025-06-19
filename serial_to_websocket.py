
import serial
import asyncio
import websockets

# === CONFIGURATION ===
SERIAL_PORT = "COM3"     # Change this to match your Arduino port
BAUD_RATE = 9600
WS_PORT = 8765

# === WebSocket clients set ===
clients = set()

async def serial_reader():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"✅ Connected to {SERIAL_PORT}")
        while True:
            line = ser.readline().decode("utf-8").strip()
            if line:
                print("Serial:", line)
                await broadcast(line)
            await asyncio.sleep(0.1)

async def broadcast(message):
    if clients:
        await asyncio.wait([client.send(message) for client in clients])

async def handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

async def main():
    ws_server = websockets.serve(handler, "localhost", WS_PORT)
    await asyncio.gather(ws_server, serial_reader())

# === Start server ===
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped")
