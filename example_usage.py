"""
Demonstration of genpark-byzantine-fault-tolerant-quorum-validator-skill
"""

from client import PBFTQuorumValidatorClient

def main():
    # 4 agent network (f=1 allowed traitor, quorum=3)
    pbft = PBFTQuorumValidatorClient(total_nodes=4)
    print(f"Network Nodes: 4 | Max Byzantine Faults Allowed: {pbft.max_faulty} | Quorum Size: {pbft.quorum_size}")

    tx_proposal = "TRANSFER 100 TOKEN FROM ALICE TO BOB"

    # Peer 1 prepares
    p1 = pbft.add_prepare("node_1", tx_proposal)
    print("Vote 1 (Prepare):", p1["is_prepared"])

    # Peer 2 prepares
    p2 = pbft.add_prepare("node_2", tx_proposal)
    print("Vote 2 (Prepare):", p2["is_prepared"])

    # Peer 3 prepares -> Quorum reached!
    p3 = pbft.add_prepare("node_3", tx_proposal)
    print("Vote 3 (Prepare - Quorum Achieved!):", p3["is_prepared"])

    # Commit phase
    pbft.add_commit("node_1", tx_proposal)
    pbft.add_commit("node_2", tx_proposal)
    c3 = pbft.add_commit("node_3", tx_proposal)
    print("\n=== TRANSACTION COMMITTED VIA PBFT ===")
    print("Committed:", c3["is_committed"])

if __name__ == "__main__":
    main()
