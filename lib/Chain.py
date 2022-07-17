from ast import Return
from lib.Block import Block
import lib.chaintool, datetime, hashlib, socket, sys, json
from colorama import Fore

# RULES #
DIFFICULTY = 4
VERIFICATION_INTERVAL = 90
BLOCK_SIGNING_INTERVAL = 60
REWARD = 5
#########

class Chain:
    def __init__(self):
        self.CURRENT_BLOCK = Block(lib.chaintool.get_previous_hash())
        with open("reward_address.txt", 'r') as a:
            self.WALLET = a.read()

    def run(self):
        print("Running...")
        lib.chaintool.set_interval(lib.chaintool.verify, VERIFICATION_INTERVAL)
        lib.chaintool.set_interval(self.sign_block, BLOCK_SIGNING_INTERVAL)
        self.socket_handle()

    def socket_handle(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 9988))
        s.listen(1)
        
        while True:
            conn, addr = s.accept()
            rcv = conn.recv(1024)
            data = rcv.decode("utf-8")

            try:
                transaction = json.loads(data)
                status = self.add_transaction(transaction)
                conn.sendall(bytes(str(status), encoding="utf-8"))
            except:
                amount = str(self.get_wallet_amount(data))
                conn.sendall(bytes(amount, encoding="utf-8"))

            if data == 'stop':
                sys.exit(0)


    def add_transaction(self, transaction):
        if not int(transaction['amount']) > self.get_wallet_amount(transaction['sender']):
            if lib.chaintool.verify_transaction(transaction):
                print(f"{Fore.GREEN}Signature is valid{Fore.RESET}")
                self.CURRENT_BLOCK.add_transaction(transaction)
                return True
            else:
                print(f"{Fore.RED}Bad signature{Fore.RESET}")
        else:
            return False

    def sign_block(self):
        hash = self.CURRENT_BLOCK.sign_block()
        if hash != None:
            self.CURRENT_BLOCK = Block(hash)
            self.add_reward()
        

    def add_reward(self):
        date = datetime.datetime.now().timestamp()
        signature = "DELTACHAINREWARD"
        public_key = "DELTACHAINREWARD"
        sender = "DELTACHAINREWARD"
        amount = REWARD
        transaction_raw = f"{date}.{sender}.{public_key}.{amount}.{self.WALLET}"
        reward_transaction = {
            'date': date,
            'sender': sender, 
            'amount': amount, 
            'receiver': self.WALLET,
            'signature': signature, 
            'public_key': public_key, 
            'transaction_raw': transaction_raw,
            'transaction_hash': hashlib.sha256(transaction_raw.encode()).hexdigest()
        }
        self.CURRENT_BLOCK.add_transaction(reward_transaction)


    def get_wallet_amount(self, wallet):
        from lib.UTXO import UTXO

        utxo = UTXO(wallet)

        utxo.wallet_amount()
        # print(f"{utxo.WALLET} has a total of {utxo.AMOUNT} DLT")
        return utxo.AMOUNT