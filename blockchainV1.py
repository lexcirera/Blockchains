import hashlib
import time

class Block:
  def __init__(self, index, timestamp, data, prev_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.prev_hash = prev_hash
    self.hash = self.calculate_hash()

  def calculate_hash(self):
    block_string = f"{self.index}{self.timestamp}{self.data}{self.prev_hash}"
    return hashlib.sha256(block_string.encode()).hexdigest()

  def mine_block(self, difficulty):
    while self.hash[:difficulty] != "0" * difficulty:
      self.hash = self.calculate_hash()

    print(f"Block mined: {self.hash}")


class Blockchain:
  def __init__(self):
    self.chain = [self.create_genesis_block()]
    self.difficulty = 4
    self.pending_transactions = []

  def create_genesis_block(self):
    return Block(0, time.time(), "Genesis Block", "0")

  def add_block(self, new_block):
    new_block.prev_hash = self.chain[-1].hash
    new_block.mine_block(self.difficulty)
    self.chain.append(new_block)

  def mine_pending_transactions(self, mining_reward_address):
    new_block = Block(len(self.chain), time.time(), self.pending_transactions, self.chain[-1].hash)
    new_block.mine_block(self.difficulty)
    self.chain.append(new_block)
    self.pending_transactions = [{"from": "mining_reward", "to": mining_reward_address, "amount": 1}]

  def is_valid_chain(self, chain):
    if chain[0] != self.create_genesis_block():
      return False

    for i in range(1, len(chain)):
      block = chain[i]
      prev_block = chain[i - 1]

      if block.hash != block.calculate_hash():
        return False

      if block.prev_hash != prev_block.hash:
        return False

    return True

  def resolve_conflicts(self):
    longest_chain = None
    max_length = len(self.chain)

    for node in self.nodes:
      response = requests.get(f"http://{node}/get_chain")
      if response.status_code == 200:
        length = response.json()["length"]
        chain = response.json()["chain"]
        if length > max_length and self.is_valid_chain(chain):
          max_length = length
          longest_chain = chain

    if longest_chain:
      self.chain = longest_chain
      return True

    return False
