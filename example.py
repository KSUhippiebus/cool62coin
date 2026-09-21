import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        """Returns the SHA-256 hash of the block contents."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """Simple Proof of Work (PoW) mechanism."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.compute_hash()


class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.unconfirmed_transactions = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        """Generates the initial block of the chain."""
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_new_transaction(self, transaction):
        """Adds a pending transaction to the mempool."""
        self.unconfirmed_transactions.append(transaction)

    def mine_pending_transactions(self):
        """Packages pending transactions, mines the block, and appends it."""
        if not self.unconfirmed_transactions:
            return False

        last_block = self.chain[-1]
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            previous_hash=last_block.hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.unconfirmed_transactions = []  # Reset mempool
        return True

    def is_chain_valid(self):
        """Validates the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Rule 1: Verify the stored block hash matches computed contents
            if current.hash != current.compute_hash():
                return False
            # Rule 2: Verify the cryptographic link between blocks
            if current.previous_hash != previous.hash:
                return False
        return True
