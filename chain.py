import hashlib
import json
import time


class Block:

    def __init__(self, index, data, previous_hash, nonce=0, timestamp=None):
        # Set the basic properties
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce

        # If no timestamp is given, use the current time
        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

        # Compute and store this block's hash
        self.hash = self.compute_hash()

    def compute_hash(self):

        # Put the important fields into a dictionary
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }

        # Turn the dictionary into a JSON string
        # sort_keys=True makes the JSON ordering consistent
        block_string = json.dumps(block_content, sort_keys=True, ensure_ascii=False)

        # Encode to bytes and run SHA-256
        hash_object = hashlib.sha256(block_string.encode("utf-8"))
        return hash_object.hexdigest()

    def to_dict(self):
        
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }


class Chain:

    def __init__(self, genesis_data="Genesis Block"):
        # The chain is just a Python list of Block objects
        self.chain = []

        # When we create a new Chain, we immediately create
        # the first block (the "genesis" block)
        self.create_genesis_block(genesis_data)

    def create_genesis_block(self, data):
        genesis_block = Block(
            index=0,
            data=data,
            previous_hash="0"
        )
        self.chain.append(genesis_block)
        return genesis_block

    def add_block(self, data):
        last_block = self.chain[-1]          # the most recent block
        new_index = last_block.index + 1     # next index

        new_block = Block(
            index=new_index,
            data=data,
            previous_hash=last_block.hash
        )

        self.chain.append(new_block)
        return new_block

    def last_block(self):
        return self.chain[-1]

    def __len__(self):
        return len(self.chain)

    def is_valid(self):
        # Chains with 0 or 1 block are automatically valid
        if len(self.chain) <= 1:
            return True

        # Start from block 1 (the second block) and compare with previous
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check that the link is correct
            if current.previous_hash != previous.hash:
                return False

            # Recompute the hash and compare
            if current.hash != current.compute_hash():
                return False

        # If all checks passed, the chain is valid
        return True

    def to_list(self):
        return [block.to_dict() for block in self.chain]