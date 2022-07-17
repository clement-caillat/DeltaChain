import hashlib, os, json
from colorama import Fore


def mine(raw):
    nonce = 0
    from lib.Chain import DIFFICULTY
    while True:
        hash = hashlib.sha256((raw + str(nonce)).encode()).hexdigest()
        if hash[:DIFFICULTY] == '0' * DIFFICULTY:
            print("Found : " + hash)
            return hash
        print(hash, end="\r")
        nonce += 1

def get_previous_hash():
    files = os.listdir("ledger")

    if len(files) == 0:
        return "000066f223d9853a62c61dd2a92968194480483623342d12a762cd7612c0cc50"
    else:
        last_blk = sorted(files)[len(files) - 1]
        return last_blk.split("x")[1].split('.')[0]

def verify():
    block_not_valid = False
    blk_list = os.listdir("ledger")
    for blk in blk_list[::-1]:
        with open(f"ledger/{blk}", 'r') as b:
            block = json.load(b)
            prev_hash = block["previous_hash"]
            if blk_list.index(blk) != 0:
                pre_block_hash = blk_list[blk_list.index(blk) - 1].split('x')[1].split('.')[0]
            else:
                pre_block_hash = "000066f223d9853a62c61dd2a92968194480483623342d12a762cd7612c0cc50" 
            
            if prev_hash == pre_block_hash: 
                if verify_block_data(blk) == False:
                    block_not_valid = True
            else:
                    block_not_valid = True

            if block_not_valid == False:
                # print(f"{Fore.GREEN}Block {blk.split('.')[0]} is valid{Fore.RESET}", end="\r")
                pass
            else:
                print(f"{Fore.RED}Block {blk.split('.')[0]} is not valid{Fore.RESET}", end="\r")



def verify_block_data(blk):
    with open(f"ledger/{blk}", 'r') as b:
        block = json.load(b)

        # Verifying transactions
        block_transactions = block["transactions"]
        transaction_block_raw = verify_transactions(block_transactions)
        if  transaction_block_raw == False:
            return False

        # Verifying block transactions data
        if transaction_block_raw[:-1] != block['transaction_block_raw']:
            return False

        # Verifying block data
        block_raw = f"{block['block_order']}/{block['date']}/{block['transaction_block_raw']}/{block['previous_hash']}/{block['reward']}"

        if block_raw != block['block_raw']:
            return False
            
    return True

def verify_transactions(transactions):
    transaction_block_raw = ""
    for transaction in transactions:
        raw = f"{transaction['date']}.{transaction['sender']}.{transaction['public_key']}.{transaction['amount']}.{transaction['receiver']}"
        raw_hash = hashlib.sha256(raw.encode())

        if raw != transaction['transaction_raw']:
            return False
        
        if raw_hash.hexdigest() != transaction['transaction_hash']:
            return False

        transaction_block_raw += transaction["transaction_raw"] + "."
    
    return transaction_block_raw


import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def verify_transaction(transaction):
    from ecdsa import VerifyingKey
    public_key = VerifyingKey.from_string(bytes.fromhex(transaction["public_key"]))
    signature = bytes.fromhex(transaction["signature"])

    try:
        public_key.verify(signature, transaction["transaction_raw"].encode())
        return True
    except:
        return False