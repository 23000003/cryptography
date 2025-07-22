from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Static PEM keys as multiline strings
PUBLIC_KEY = '''
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDv/LnAoDkyewwjwqwgi9VSg51F
+tUJ8cGwL6Rqdf5ZXrRCHI1KLjOxdFbzB81YjS76cOzezQRz2vuYDo7OvLfYSjFI
fmukUxN+EliKkg0TwswylVroLBW9OKN70Zd62dc+gfkA3Vu8cDoRKzz6BKpo4yDo
0D3FOsbNEj80opjmtQIDAQAB
'''

PRIVATE_KEY = '''
MIICXAIBAAKBgQDv/LnAoDkyewwjwqwgi9VSg51F+tUJ8cGwL6Rqdf5ZXrRCHI1K
LjOxdFbzB81YjS76cOzezQRz2vuYDo7OvLfYSjFIfmukUxN+EliKkg0TwswylVro
LBW9OKN70Zd62dc+gfkA3Vu8cDoRKzz6BKpo4yDo0D3FOsbNEj80opjmtQIDAQAB
AoGADuZtDgWkp3q2TT4X+8lSzFW5nQ+uzHhDI1JB7g43ZYsYvAYTy6hEs17ayyoP
2NCjOw9p1Yd7IEpXVqCIw1M6QsfGdshy1NStsGpDHQYBBd8XiT8cWUaT/nmq5dEs
i0wOITMZePLgI5/5pD4M6DIEJKskM+Rzlo47AiyRchL6pqECQQD+XAZNCl6R5wjI
DrqW4v6Vw8mhdaPnQhPexmhHa1f9D7sA32A2H2N8M3dUDOwuG+DJhPkjVaQtFvT8
mjDjSZTdAkEA8Yj4hncF/WnLTDSXmiWfpNwYwjfpjOj8e4/5rWHF1jWZMgl0l1AS
Otna2dIbXp64dqsInITJTIDSQpbxuhrvuQJBAN9Ee6toLLa5KzYf55zGR13Ca9wz
3NkDYVmsop/+E0/oXOdZK6SWTMcajeXTKgUXJ2r8M4vWgrOpcQXBeqQnVGkCQDYX
e7j5bOD80Wemm5EM/fy4wd61ENvazbiKXNske17msAFRtsewSfTeFzIS6Mg++Yax
9QLAhihY7T22ejo4kBkCQBdg2yKHQrmG+njGfLsdQG9MARFlnOfohoBFQTYdtrmf
5JRNfwtPiis2YaoM2gP7z2qaunYbibDV5SYmtdD8GK0=
'''

def encrypt_rsa(data: bytes) -> bytes:
    print("Yessir")
    key = RSA.import_key(base64.b64decode(PUBLIC_KEY))
    print("START: 1")
    cipher = PKCS1_OAEP.new(key)
    print("2")
    encrypted = cipher.encrypt(data)  # bytes
    print("3")
    return encrypted

def decrypt_rsa(data: bytes) -> bytes:
    key = RSA.import_key(base64.b64decode(PRIVATE_KEY))
    cipher = PKCS1_OAEP.new(key)
    decrypted = cipher.decrypt(data)
    return decrypted