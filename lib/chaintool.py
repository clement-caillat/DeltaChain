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
                # Compare transaction raw hash with merkleroot 
                print(f"{Fore.GREEN}Block {blk.split('.')[0]} is valid{Fore.RESET}")
            else:
                print(f"{Fore.RED}Block {blk.split('.')[0]} is not valid{Fore.RESET}")