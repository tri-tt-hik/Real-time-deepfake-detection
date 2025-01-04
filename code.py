import os
import hashlib
#import cv2
from det_model import videodet
from web3 import Web3

# Connect to Ganache local blockchain
GANACHE_URL = "http://127.0.0.1:8545"  # Default Ganache URL
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Check connection
if not web3.is_connected():
    print("Failed to connect to Ganache. Ensure it's running.")
    exit()

# Contract details (update with your contract details from Ganache)
CONTRACT_ADDRESS = "0x2DF3771E61bDABF03602A94E8D6e411Eb072e1a0"  # Replace with the deployed contract address
CONTRACT_ABI = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "imageHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "result",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "DetectionStored",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "name": "detectionResults",
      "outputs": [
        {
          "internalType": "string",
          "name": "imageHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "result",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "imageHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "result",
          "type": "string"
        }
      ],
      "name": "storeDetectionResult",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "imageHash",
          "type": "string"
        }
      ],
      "name": "getDetectionResult",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]

# Initialize contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Use one of the accounts provided by Ganache
ACCOUNT_ADDRESS = "0x88Fe16cd31b35A25A7a523D5Aac08B1f7d78fEeb"  # Replace with an address from Ganache
PRIVATE_KEY = "0xa1f5a3b1cdbe702b1c93214f21f91d8f813509cfe55cbe3abcd64741b5fc0712"  # Replace with the private key

# Function to calculate the hash of a file
def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of the given file."""
    with open(file_path, "rb") as file:
        file_data = file.read()
    return hashlib.sha256(file_data).hexdigest()

# Function to calculate the hash of a video (based on frame data)
def calculate_video_hash(video_path):
    """Calculate SHA-256 hash for a video by hashing its frames."""
    with open(video_path, "rb") as f:
        video_data = f.read()
    return hashlib.sha256(video_data).hexdigest()

# Function to store a file on the blockchain
def store_file_on_blockchain(file_hash,file_path):
    """Store the file hash on the blockchain if not already present."""
    if(videodet.predict_video(file_path)['confidence']<90):
        return
    tx = contract.functions.storeDetectionResult(file_hash, videodet.predict_video(file_path)['label']).build_transaction({
        "from": ACCOUNT_ADDRESS,
        "nonce": web3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        "gas": 3000000,
        "gasPrice": web3.to_wei("20", "gwei"),
    })
    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction sent: {web3.to_hex(tx_hash)}")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction confirmed:", receipt)

# Function to check if a file hash exists on the blockchain
def check_file_exists(file_hash):
    """Check if the given file hash exists on the blockchain."""
    try:
        result = contract.functions.getDetectionResult(file_hash).call()
        if result[0]:  # Check if the hash exists
            print(f"File with hash {file_hash} exists in the blockchain.")
            return True
        else:
            print(f"File with hash {file_hash} does not exist in the blockchain.")
            return False
    except Exception as e:
        print(f"Error checking file existence: {e}")
        return False

# Process a file (image or video) and store it on the blockchain
def process_file(file_path):
    """Process the file and store its hash on the blockchain if it doesn't exist."""
    if not os.path.exists(file_path):
        print("File not found!")
        return

    if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):  # Image file
        file_hash = calculate_file_hash(file_path)
    elif file_path.lower().endswith((".mp4", ".avi", ".mkv", ".mov", ".flv")):  # Video file
        file_hash = calculate_video_hash(file_path)
    else:
        print("Unsupported file format!")
        return

    print(f"Processing {file_path} with hash {file_hash}")
    if not check_file_exists(file_hash):
        store_file_on_blockchain(file_hash,file_path)


def get_detection_result(video_path):
    video_hash = calculate_video_hash(video_path)
    if not check_file_exists(video_hash):
        print(f"File with hash {video_hash} does not exist in the blockchain.")
        return {}
    try:
        # Call the smart contract's function
        result = contract.functions.getDetectionResult(video_hash).call()

        # Unpack the result tuple
        stored_hash, detection_result, timestamp = result
        detection = { 'image_hash': stored_hash, 'detection_result': detection_result, 'timestamp': timestamp }
        return detection
    except Exception as e:
        print(f"Error reading from blockchain: {e}")
        return None

