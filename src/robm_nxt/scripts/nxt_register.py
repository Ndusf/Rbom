#!/usr/bin/env python

from __future__ import print_function

from nxt.locator import *
import os
import sys

def find_and_register_nxt(ask_for_confirmation=True):
	print("Searching NXT brick on USB...")
	b = None
	try:
		b = find_one_brick(strict=False, method=Method(usb=True, bluetooth=False, fantomusb=True))
	except:
		b = None

	if not b:
		print("No brick found... Check power and connexion then try again.")
		return
	
	(name, addr, _ , _) = b.get_device_info()
	name = name.rstrip('\0')
	print("Found brick '%s' (%s)" % (name, addr))
	
	if ask_for_confirmation:
		answer = raw_input("Register this brick (will overwrite ~/.nxt-python) [y/N]? ")
		if not answer in ["Y","y","yes","YES","Yes"]:
			print("Registration aborted.")
			return
	
	print("Updating ~/.nxt-python config file...")

	filepath = os.path.expanduser('~/.nxt-python')
	with open(filepath, "w") as f:
		print("[Brick]", file=f)
		print("name = %s" % name, file=f)
		print("host = %s" % addr, file=f)

	print("Done!")


if __name__ == "__main__":
	print("=====================================================================")
	print("=    NXT-Register tool                        (V. Drevelle, 2018)   =")
	print("=====================================================================")
	print("= Updates the ~/.nxt-python config file with USB attached NXT brick =")
	print("= Option: -y  Don't ask user before writing to config file          =")
	print("=====================================================================")
	
	yes_option = (len(sys.argv) > 1) and sys.argv[1] == '-y'	
	find_and_register_nxt(ask_for_confirmation = not yes_option)
