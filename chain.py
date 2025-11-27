"""Simple blockchain Chain and Block classes for the supply-chain project.

This module provides a minimal Block dataclass and a Chain class that
represents a sequence of blocks.

Key features:
- Block: stores index, timestamp, data, previous_hash, nonce and hash
- Chain: manages blocks, creates a genesis block, appends blocks, and
  validates the chain integrity.


"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Block:
    # A minimal block container.

    # Attributes:
    #     index: position in the chain (0 for genesis)
    #     timestamp: unix timestamp when block was created
    #     data: arbitrary payload (e.g., a dict describing a shipment)
    #     previous_hash: hex string of previous block's hash
    #     nonce: integer reserved for proofs (default 0)
    #     hash: computed SHA-256 hash of the block contents (set on init)
    index: int
    timestamp: float
    data: Any
    previous_hash: str
    nonce: int = 0
    hash: str = field(init=False)

    def __post_init__(self) -> None:
        # compute the block hash right after initialization
        self.hash = self.compute_hash()

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict representation of the block (useful for JSON).

        Note: `hash` is included to make serialization round-trip-friendly.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    def compute_hash(self) -> str:
        # Compute SHA-256 hash of the block contents (deterministic).

        # We convert the important fields to JSON with sorted keys to ensure
        # the same input always produces the same hash.
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_content, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()
    
        #The block string converts the block_content into a text string in JSON format. 
        #We then encode this string to a UTF-8 byte representation before passing it to the SHA-256 hashing function.
        #This ensures that the hash is computed based on the exact byte sequence of the block's content.


class Chain:
    # Represents a simple blockchain (a sequence of linked blocks).

    # Usage:
    #     chain = Chain()
    #     chain.add_block({"gtin": "...", "serial": "..."})
    #     assert chain.is_valid()
    # Genesis block is created automatically on initialization.
    # Initializes the Chain with a genesis block.
    # So we know the chain always has at least one block.
    # See https://en.wikipedia.org/wiki/Blockchain

    def __init__(self, genesis_data: Any = "Genesis Block") -> None:
        self.chain: List[Block] = []
        self.create_genesis_block(genesis_data)

    def create_genesis_block(self, data: Any) -> Block:
        # Create and append the genesis (first) block.
        # The genesis block has index 0 and a previous_hash of '0'.

        genesis = Block(index=0, timestamp=time.time(), data=data, previous_hash="0")
        self.chain.append(genesis)
        return genesis

    def add_block(self, data: Any) -> Block:
        """Create a new Block with `data`, append it to the chain, and return it."""
        last = self.chain[-1]
        new_block = Block(index=last.index + 1, timestamp=time.time(), data=data, previous_hash=last.hash)
        self.chain.append(new_block)
        return new_block

    def __len__(self) -> int:
        return len(self.chain)

    def last_block(self) -> Block:
        return self.chain[-1]

    def is_valid(self) -> bool:
        # Validate the integrity of the chain.

        # Checks performed:
        # - Each block's stored `previous_hash` matches the previous block's computed `hash`.
        # - Each block's stored `hash` equals a freshly computed hash of its contents.

        # Returns True if the chain is valid, False otherwise.
        if not self.chain:
            return True

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # check previous link
            if current.previous_hash != previous.hash:
                return False

            # check block's hash integrity (detects tampering with data)
            if current.hash != current.compute_hash():
                return False

        return True

    def to_list(self) -> List[Dict[str, Any]]:
        """Return the chain as a list of dictionaries (serializable)."""
        return [b.to_dict() for b in self.chain]


__all__ = ["Block", "Chain"]
