#Import the necessary libraries
import hashlib
import datetime

# Create the blockchain class
class Blockchain:

    # Initialize the blockchain
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_genesis_block()

    # Create the genesis block
    def create_genesis_block(self):
        block = {
            'index': 0,
            'previous_hash': 0,
            'timestamp': datetime.datetime.now(),
            'data': 'Genesis Block',
            'hash': self.create_hash(0, 0, [], datetime.datetime.now())
        }
        self.chain.append(block)

    # Create a new block
    def create_block(self, data):
        previous_block = self.get_last_block()
        index = previous_block['index'] + 1
        previous_hash = previous_block['hash']
        timestamp = datetime.datetime.now()
        hash = self.create_hash(index, previous_hash, self.transactions, timestamp)
        block = {
            'index': index,
            'previous_hash': previous_hash,
            'timestamp': timestamp,
            'data': data,
            'hash': hash
        }
        self.transactions = []
        self.chain.append(block)
        return block

    # Create a hash
    def create_hash(self, index, previous_hash, transactions, timestamp):
        block_string = str(index) + str(previous_hash) + str(transactions) + str(timestamp)
        block_hash = hashlib.sha256(block_string.encode())
        return block_hash.hexdigest()

    # Get the last block
    def get_last_block(self):
        return self.chain[-1]

    # Add a new transaction
    def add_transaction(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        self.transactions.append(transaction)
        return self.get_last_block()['index'] + 1

    # Calculate the proof of work
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    # Check if the proof is valid
    def valid_proof(self, last_proof, proof):
        guess = str(last_proof) + str(proof)
        guess_hash = hashlib.sha256(guess.encode()).hexdigest()
        return guess_hash[:4] == '0000'

    # Check if the blockchain is valid
    def check_chain(self):
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i-1]
            current_block = self.chain[i]
            if current_block['previous_hash'] != self.create_hash(previous_block['index'], previous_block['previous_hash'], previous_block['transactions'], previous_block['timestamp']):
                return False
        return True



# Create the wallet class
class Wallet:

    # Initialize the wallet
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.balance = 0

    # Get the balance
    def get_balance(self):
        return self.balance

    # Send money
    def send_money(self, sender, receiver, amount):
        if self.balance >= amount:
            self.blockchain.add_transaction(sender, receiver, amount)
            self.balance -= amount
            return True
        else:
            return False

# Initialize the blockchain
blockchain = Blockchain()

# Initialize the wallet
wallet = Wallet(blockchain)

# Send money
wallet.send_money('Alice', 'Bob', 10)

# Check the balance
print(wallet.get_balance())