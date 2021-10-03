'''
MIT License

Copyright (c) 2021 Nikolaos Bazigos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

https://github.com/sourcecode347/Bitcoin-cli_Solo_Miner/
'''

from hashlib import sha256
import time as t
import subprocess
import json,sys
import threading,os
global begin
begin = t.time()
def executeCMD(cmd):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc.stdout.read() + proc.stderr.read()
        output3 = stdout_value.decode("utf-8","ignore")
        return(output3)
    except:
        pass
        return False
        
def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()
    
MAX_NONCE=100000
def mine(block_number,transaction,previous_hash,prefix_zeros):
    prefix_str='0'*prefix_zeros
    #print(prefix_str)
    for nonce in range(MAX_NONCE):
        text= str(block_number) + transaction + previous_hash + str(nonce)
        hash = SHA256(text)
        if hash.startswith(prefix_str):
            print("Bitcoin mined with nonce value :",nonce)
            print("Bitcoin mined hash :",hash)
            executeCMD("bitcoin-cli submitblock "+hash)
            return hash
        nonce+=1
    seconds = t.time() - begin
    print("Could not find a hash in the given range of upto", MAX_NONCE , "in "+str(seconds)+" Seconds")
    hashrate = MAX_NONCE / seconds
    print ( "HashRate : "+('%.2f' % (hashrate/1024) )+" KHs")

while True:
    a = executeCMD("bitcoin-cli getchaintips")
    a = json.loads(a)
    print("Height : "+str(a[0]['height']))
    height = a[0]['height']
    print("hash : "+str(a[0]['hash']))
    hash = a[0]['hash']
    print("branchlen : "+str(a[0]['branchlen']))
    branchlen = a[0]['branchlen']
    status = a[0]['status']
    print("status : "+str(a[0]['status']))
    if status == "active":
        a = executeCMD("bitcoin-cli getblock "+hash)
        a = json.loads(a)
        #print(a)

    txcounter = 0
    txhashes = []
    for x in a["tx"]:
        n=x
        txcounter+=1
        if txcounter%2==1:
            transactions = ""
            n+=" -> "
            transactions+=n
        else:
            transactions+=n
            txhashes.append(transactions)
        if txcounter==2:
            breaker=1
            #break
        
    print(int(a["height"])+1)
    print(a["hash"])
    print(txhashes[0])
    for x in txhashes:
        print(x)
        begin=t.time()
        mine(int(a["height"])+1,x,a["hash"],19)

