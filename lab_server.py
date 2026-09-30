# lab_server.py (FIXED & VERIFIED)
import socket
import threading

def handle_client(conn, addr):
    print(f"\n[+] Connection from {addr}")
    
    # 1. Read the raw HTTP headers
    request_data = b""
    while b"\r\n\r\n" not in request_data:
        request_data += conn.recv(1024)
        
    headers, _, body_start = request_data.partition(b"\r\n\r\n")
    print("[*] Received Headers:")
    print(headers.decode('utf-8', errors='ignore'))

    # Extract Content-Length
    cl = 0
    for line in headers.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            cl = int(line.split(b":")[1].strip())

    # 2. FRONT-END SIMULATION: Read exactly 'Content-Length' bytes
    print(f"\n[*] [FRONT-END] Using Content-Length: {cl}")
    
    fe_body = body_start
    while len(fe_body) < cl:
        fe_body += conn.recv(1024)
        
    fe_processed_body = fe_body[:cl]
    remaining_in_buffer = fe_body[cl:]
    
    print(f"[FRONT-END] Processed {len(fe_processed_body)} bytes. Request complete.")
    print(f"[FRONT-END] Raw bytes processed by FE: {fe_processed_body}")

    # 3. BACK-END SIMULATION: The backend receives the ENTIRE stream the front-end sent it.
    # In a real proxy, the front-end forwards the headers + the CL bytes to the backend.
    backend_stream = fe_processed_body + remaining_in_buffer
    
    print(f"\n[*] [BACK-END] Received stream for body parsing:")
    print(repr(backend_stream))

    # Back-end uses Transfer-Encoding: chunked
    if b"transfer-encoding: chunked" in headers.lower():
        print("[BACK-END] Using Transfer-Encoding: chunked to parse body...")
        
        # Find the chunk terminator
        chunk_end = backend_stream.find(b"0\r\n\r\n")
        if chunk_end != -1:
            print("[BACK-END] Found chunk terminator '0\\r\\n\\r\\n'. Body parsing complete.")
            
            # Everything AFTER the chunk terminator is treated as the NEXT request
            next_request = backend_stream[chunk_end + 5:]
            
            if next_request.strip():
                print("\n" + "="*70)
                print(" DESYNC DETECTED! ")
                print("The Back-end parsed the chunked body, and treated the leftover")
                print("bytes as a BRAND NEW HTTP Request!")
                print("="*70)
                print(next_request.decode('utf-8', errors='ignore'))
                print("="*70 + "\n")
                
                # Send response for the smuggled request
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 24\r\n\r\nSmuggled request processed!")
            else:
                print("[BACK-END] No extra bytes after chunk terminator. Clean request.")
        else:
            print("[BACK-END] Waiting for more data or chunk terminator not found.")
    else:
        print("[BACK-END] No TE: chunked found. Standard processing.")

    # Send response for the first request
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 23\r\n\r\nFirst request processed!")
    conn.close()

def start_lab():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8881))
    server.listen(5)
    print("[*] CL.TE Desync Lab listening on http://127.0.0.1:8881")
    
    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == "__main__":
    start_lab()