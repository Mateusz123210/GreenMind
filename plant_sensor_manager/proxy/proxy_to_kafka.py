import socket
import json
import time

from connectivity.kafka_connector import KafkaConnector

KAFKA_TOKEN = "1735684275820034ZWNFZGNXTlg2Vzl2T0xuUFNPa3JZZk9OcHpQUVlRb3JYOEpTa0RDeUJka1VsUDZ3"
KAFKA_CONNECTOR = KafkaConnector(
    "50.85.212.131:9092",
    command_callbacks={},
)

def send_to_broker(temperature, illumunance, moisture):
    json_data = {
            "token": KAFKA_TOKEN,
            "timestamp": time.time(),
            "temperature": float(temperature),
            "illuminance": int(illumunance),
            "moisture": int(moisture)      
    }
    KAFKA_CONNECTOR.send_one(bytes(str(json_data), "utf-8"))
    KAFKA_CONNECTOR.flush()

def receive_json(ip, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind to the specified IP and port
            s.bind((ip, port))
            s.listen(5)  # Allow up to 5 queued connections
            print(f"Listening for connections on {ip}:{port}...")

            while True:  # Continuously listen for connections
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    # Receive data
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        print("No data received, closing connection.")
                        continue
                    try:
                        # Parse the JSON data
                        json_data = json.loads(data)
                        print("Received JSON data:", json_data)
                        send_to_broker(json_data["temperature"], json_data["illuminance"], json_data["moisture"])
                        print("Data sent to broker.")
                    except json.JSONDecodeError:
                        print("Received invalid JSON.")
    except Exception as e:
        print(f"Error receiving JSON: {e}")

if __name__ == "__main__":
    receiver_ip = '192.168.7.1'  # Bind to all interfaces
    receiver_port = 5000     # Port to listen on
    receive_json(receiver_ip, receiver_port)
