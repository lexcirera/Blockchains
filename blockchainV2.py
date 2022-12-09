#Import the required libraries
import hashlib
import json
import binascii
import requests
import base64

#Define a class for a Blockchain
class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.wallet = {}
        self.user_db = {}
        self.create_block(proof=1, previous_hash=1)

    #Define a function to create a new block in the blockchain
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        #Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    #Define a function to add a new transaction to the blockchain
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    #Define a function to generate a SHA-256 hash of a block
    @staticmethod
    def hash(block):
        #We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    #Define a function to return the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]

    #Define a function to validate a new proof of work
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    #Define a function to validate a proof
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    #Define a function to add a new node to the node set
    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    #Define a function to validate the blockchain
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            #Validate the hash of the block
            if block['previous_hash'] != self.hash(last_block):
                return False

            #Validate the proof of work
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    #Define a function to resolve conflicts
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        #We're only looking for chains longer than ours
        max_length = len(self.chain)

        #Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                #Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        #Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    #Define a function to create a wallet
    def create_wallet(self):
        #Generate a random 32-byte private key
        private_key = binascii.hexlify(os.urandom(32)).decode('ascii')
        #Generate the public key from the private key
        public_key = self.generate_public_key(private_key)
        #Generate the wallet address from the public key
        wallet_address = self.generate_wallet_address(public_key)
        #Add the wallet to the wallet dictionary
        self.wallet[wallet_address] = private_key
        return wallet_address

    #Define a function to generate a public key from a private key
    def generate_public_key(self, private_key):
        private_key_bytes = binascii.unhexlify(private_key)
        public_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        public_key_bytes = public_key.to_string()
        public_key_hex = binascii.hexlify(public_key_bytes).decode('ascii')
        return public_key_hex

    #Define a function to generate a wallet address from a public key
    def generate_wallet_address(self, public_key):
        public_key_bytes = binascii.unhexlify(public_key)
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        network_byte = b'\x00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_digest
        sha256_bpk = hashlib.sha256(network_bitcoin_public_key)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_bpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_bpk_digest = sha256_2_bpk.digest()
        checksum = sha256_2_bpk_digest[:4]
        binary_address = network_bitcoin_public_key + checksum
        wallet_address = base64.b58encode(binary_address)
        return wallet_address.decode('ascii')

    #Define a function to add a user to the user database
    def add_user(self, user_id, wallet_address):
        self.user_db[user_id] = wallet_address

    #Define a function to get the wallet address for a user
    def get_wallet_address(self, user_id):
        return self.user_db[user_id]