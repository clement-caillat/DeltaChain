import datetime, lib.chaintool, json, os
import hashlib

class Block:
    def __init__(self, PREVIOUS_HASH):
        self.BLOCK_NUMBER = len(os.listdir("ledger"))
        self.PREVIOUS_HASH = PREVIOUS_HASH
        self.PENDING_TRANSACTIONS = []
        self.RAW_TRANSACTIONS = ""

    def add_transaction(self, transaction):
        self.PENDING_TRANSACTIONS.append(transaction)
        self.RAW_TRANSACTIONS += transaction["compressed"] + "."

        # print("Raw : " + self.RAW_TRANSACTIONS)
        # print(self.PENDING_TRANSACTIONS)

    def sign_block(self):
        from lib.Chain import DIFFICULTY
        block_order = str(self.BLOCK_NUMBER) + 'x'
        date = datetime.datetime.now().timestamp()
        transactions = self.PENDING_TRANSACTIONS
        raw_transactions = self.RAW_TRANSACTIONS[:-1]
        merkleroot = hashlib.sha256(raw_transactions.encode()).hexdigest()
        previous_hash = self.PREVIOUS_HASH
        reward = 10
        raw = f"{block_order}/{date}/{raw_transactions}/{previous_hash}/{reward}"

        hash = lib.chaintool.mine(raw)

        data = {
            'block_order': block_order + '0' * DIFFICULTY,
            'date': date,
            'transactions': transactions,
            'compressed': raw_transactions,
            'merkleroot': merkleroot,
            'reward': reward,
            'raw': raw,
            'previous_hash': previous_hash,
            'hash': hash
        }

        block_id = block_order + hash
        with open(f"ledger/{block_id}.blk", "w") as b:
            json.dump(data, b)
        return hash