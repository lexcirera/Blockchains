from flask import Flask, request, jsonify

# Create a Flask app
app = Flask(__name__)

# Create a blockchain
blockchain = []

# Create a new block
def create_block(data):
    block = {
        "index": len(blockchain) + 1,
        "timestamp": Date.now(),
        "data": data,
        "previous_hash": blockchain[-1]["hash"] if len(blockchain) > 0 else None,
        "hash": None,  # TODO: Calculate the hash of the block
    }
    return block

# Add a new block to the blockchain
@app.route("/add-block", methods=["POST"])
def add_block():
    data = request.get_json()
    block = create_block(data)
    blockchain.append(block)
    return jsonify(block)

# Get the current state of the blockchain
@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain)

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
