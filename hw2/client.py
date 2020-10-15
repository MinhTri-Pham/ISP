import asyncio
import websockets
import os
from hashlib import sha256


async def pake():
    
    # Constants
    EMAIL = "your.email@epfl.ch"
    PASSWORD = "correct horse battery staple"
    N = int("EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D60089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3")
    g = 2
    
    uri = ws://127.0.0.1:5000
    async with websockets.connect(uri) as websocket:
        await websocket.send(EMAIL.encode())
        salt_utf8_hex = await websocket.recv() 
        salt = int(salt_utf8_hex, 16)

        a = int.from_bytes(os.urandom(32), byteorder=sys.byteorder)
        A = pow(g,a,N)
        A_uft8_hex = format(A, "x").encode()
        await websocket.send(A_uft8_hex)
        
        B_utf8_hex = await websocket.recv()
        B = int(B_utf8_hex, 16)
        
        # u = H(A || B)
        h_u = sha256()
        h_U.update(A_uft8_hex)
        h_U.update(B_uft8_hex)
        u_utf8_hex = h_u.hexdigest()
        u = int(u_utf8_hex, 16)

        # email_psw = H(U || ":" || PASSWORD)
        h_email_psw = sha256()
        h_email_psw.update(EMAIL.encode())
        h_email_psw.update(":".encode())
        h_email_psw.update(PASSWORD.encode())
        email_psw_utf8_hex = h_email_psw.hexdigest()

        # x = H(salt || email_psw)
        h_x = sha256()
        h_x.update(salt_utf8_hex)
        h_x.update(email_psw_utf8_hex)
        x_utf8_hex = h_x.hexdigest()
        x = int(x_utf8_hex, 16)

        # secret S
        S =  pow(B - pow(g, x, N), a + (u * x), N)
        S_uft8_hex = format(A, "x").encode()

        # Validate by sending H(A || B || S)
        h_result = sha256()
        h_result.update(A_uft8_hex)
        h_result.update(B_uft8_hex)
        h_result.update(S_uft8_hex)
        result_utf8_hex = h_result.hexdigest()

        await websocket.send(result_utf8_hex)




        
