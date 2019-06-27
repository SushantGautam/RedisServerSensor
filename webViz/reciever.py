#from encryption import alice_pub_key
#from decryption import bobs_priv_key
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os
import pickle
#from sender import send_encrypted_msg
#Curve parameters for secp256k1
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) # This is our generator point.
Pcurve =  2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 # Number of points in the field
Acurve = 0
Bcurve = 7

bob_privatekey = 75576454881951377302765104918215909046440976706689486541183925775737282153848

def modinv(a,n=Pcurve): #Extended Euclidean Algorithm/'division' in elliptic curves
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        ratio = int(high/low)
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def ECadd(a,b): #This is called point addition. Not true addition, invented for EC. Could have been called anything.
    LamAdd = ((b[1]-a[1]) * modinv(b[0]-a[0],Pcurve)) % Pcurve
    x = (LamAdd*LamAdd-a[0]-b[0]) % Pcurve
    y = (LamAdd*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def ECdouble(a): # This is called point doubling, also invented for EC.
    Lam = ((3*a[0]*a[0]+Acurve) * modinv((2*a[1]),Pcurve)) % Pcurve
    x = (Lam*Lam-2*a[0]) % Pcurve
    y = (Lam*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def EccMultiply(GenPoint,ScalarHex): #Double & add. Not true multiplication
    if ScalarHex == 0 or ScalarHex >= N: raise Exception("Invalid Scalar/Private Key")
    ScalarBin = str(bin(ScalarHex))[2:]
    Q=GenPoint
    for i in range (1, len(ScalarBin)): # This is invented EC multiplication.
        Q=ECdouble(Q) # print "DUB", Q[0]; print
        if ScalarBin[i] == "1":
            Q=ECadd(Q,GenPoint) # print "ADD", Q[0]; print
    return (Q)

bob_publickey = EccMultiply(GPoint, bob_privatekey)
#print("Bob's public key: ", bob_publickey)
pub_key = bob_publickey
pickle.dump(pub_key, open('tuple1.dump', 'wb'))

#alice_pub_key = pickle.load(open('tuple.dump', 'rb'))
alice_pub_key = (104708700033902801570712199838589259307201711250985035511778105476236474264250, 113769056377150786946624739198808117917271265178649255546484016340893843263606)
print('alice public key:', alice_pub_key)

#bobs shared key
bob_sharedkey = EccMultiply(alice_pub_key, bob_privatekey)
print("Bob's shared secret key: ", bob_sharedkey)
#Convert the x & y components to bytes of length 32
x_component = bob_sharedkey[0]
#print('x-comp:', x_component)
y_component = bob_sharedkey[1]
#print('y-comp:', y_component)
    #Create a SHA3_256 class
sha3_key = SHA256.new()
    #Update the hash object with x_component
sha3_key.update(b'x_component')
    #Concatenate the y_component with x_component in the hash object
sha3_key.update(b'y_component')
    #Derive the key
secret_key = sha3_key.digest()
#print('Printing shared key', secret_key)
#print('length:', len(secret_key))

#decrypt message
def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

#decrypt file
def decrypt_file(file_name, key):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = decrypt(ciphertext, key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

key = secret_key
#decrypted_data = decrypt(send_encrypted_msg() , key)
#def decrypteddata(data):
#    decrypted_data = decrypt(data , key)
#    return decrypted_data
#print('decrypted data:', decrypted_data)
def decrypteddata(data):
    decrypted_data = decrypt(data , key)
    return decrypted_data
#decrypt_file('test.txt.enc', key)
