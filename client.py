"""
Practical Byzantine Fault Tolerance (PBFT) Quorum Validator.
Zero external dependencies, standard library only.
"""

import hashlib
from typing import Dict, List, Any, Optional

class PBFTQuorumValidatorClient:
    """
    Validates 3-phase PBFT consensus (Pre-Prepare, Prepare, Commit):
    - Tolerates f malicious/faulty agents in a 3f+1 total agent swarm
    - Validates quorum threshold: 2f + 1 matching cryptographic digests
    """

    def __init__(self, total_nodes: int = 4):
        self.total_nodes = total_nodes
        self.max_faulty = (total_nodes - 1) // 3
        self.quorum_size = 2 * self.max_faulty + 1
        self.prepared_messages = {} # digest -> set of sender_ids
        self.committed_messages = {} # digest -> set of sender_ids

    def compute_digest(self, message: str) -> str:
        """Computes SHA-256 digest of payload."""
        return hashlib.sha256(message.encode("utf-8")).hexdigest()

    def add_prepare(self, sender_id: str, message: str) -> Dict[str, Any]:
        """Records prepare vote and verifies 2f+1 prepare quorum."""
        digest = self.compute_digest(message)
        if digest not in self.prepared_messages:
            self.prepared_messages[digest] = set()
        
        self.prepared_messages[digest].add(sender_id)
        count = len(self.prepared_messages[digest])
        is_prepared = count >= self.quorum_size

        return {
            "digest": digest[:12] + "...",
            "prepare_votes": count,
            "quorum_required": self.quorum_size,
            "is_prepared": is_prepared
        }

    def add_commit(self, sender_id: str, message: str) -> Dict[str, Any]:
        """Records commit vote and verifies 2f+1 commit quorum."""
        digest = self.compute_digest(message)
        if digest not in self.committed_messages:
            self.committed_messages[digest] = set()

        self.committed_messages[digest].add(sender_id)
        count = len(self.committed_messages[digest])
        is_committed = count >= self.quorum_size

        return {
            "digest": digest[:12] + "...",
            "commit_votes": count,
            "quorum_required": self.quorum_size,
            "is_committed": is_committed
        }
