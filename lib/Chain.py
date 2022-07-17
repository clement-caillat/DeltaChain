from lib.Block import Block
import lib.chaintool

# RULES #
DIFFICULTY = 4
#########

class Chain:
    def __init__(self):
        self.CURRENT_BLOCK = Block(lib.chaintool.get_previous_hash())

    def run():
        print("Running")

    def add_transaction(self, transaction):
        self.CURRENT_BLOCK.add_transaction(transaction)

    def sign_block(self):
        hash = self.CURRENT_BLOCK.sign_block()
        self.CURRENT_BLOCK = Block(hash)