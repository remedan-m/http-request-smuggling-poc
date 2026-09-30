# HTTP CL.TE Request Smuggling Lab & POC

A lightweight, educational Python-based simulation of an HTTP Request Smuggling (CL.TE Desync) vulnerability. This project demonstrates how parsing discrepancies between a front-end proxy and a back-end server can lead to request desynchronization.

## Disclaimer
This code is provided strictly for **educational and research purposes**. It is designed to run in a local, isolated environment. Do not use this against any systems you do not own or have explicit permission to test.

## How It Works
1. `lab_server.py`: Simulates a vulnerable architecture where the front-end strictly honors `Content-Length`, but the back-end strictly honors `Transfer-Encoding: chunked`.
2. `poc_smuggler.py`: Crafts and sends a raw TCP payload where the `Content-Length` only covers the chunked terminator (`0\r\n\r\n`), leaving the smuggled request in the TCP buffer for the back-end to process as a new request.

## Usage
1. Start the lab server: `python3 lab_server.py`
2. In a separate terminal, run the POC: `python3 poc_smuggler.py`
3. Observe the terminal output to see the front-end/back-end parsing divergence and the successful desync.

## Learn More
This lab was built to deepen understanding of low-level HTTP mechanics, RFC 7230 compliance, and advanced web application security testing. 