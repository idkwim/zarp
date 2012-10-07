#! /usr/local/bin/python
import os, sys
sys.path.insert(0, os.getcwd() + '/modules/')
from util import print_menu, header
import stream, session_manager, parse_cmd
from commands import getoutput

#
# Network Attack Tool; view README for more information.
# 	[ZARP]
#	v0.01
#

def main():
	# handle command line options first
	if len(sys.argv) > 1:
		parse_cmd.parse(sys.argv)
		sys.exit(1)

	# menus
	main_menu =    [ 'Poisoners', 'DoS Attacks', 'Sniffers', 'Scanners',
				     'Parameter','Sessions']
	poison_menu =  [ 'ARP Poison', 'DNS Poison', 'DHCP Poison']
	dos_menu =     [ 'NDP', 'Nestea', 'LAND', 'TCP SYN', 'SMB2',
					'DHCP Starve'
				   ]
	sniffer_menu = [ 'HTTP Sniffer', 'Password Sniffer']
	spoofer_menu = [ 'HTTP Server', 'SSH Server', 'FTP Server' ]
	scanner_menu = [ 'NetMap', 'Service Scan', 'AP Scan']
	parameter_menu = [ 'WEP Crack', 'WPA2 Crack', 'Router Pwn' ]
	
	running = True
	choice = -1
	while running:
		header()
		choice = print_menu(main_menu)		
		if choice == 0:
			# check if they've got running sessions! 
			cnt = stream.get_session_count()
			if cnt > 0:
				print '[!] You have %d sessions running.  Are you sure?'%cnt
				choice = raw_input('> ')
				if choice == 'y':
					stream.stop_session('all', -1)
					running = False	
			else:
				print '[dbg] session count: ', cnt
				print "Exiting..."
				running = False
		elif choice == 1:
			while True:
				choice = print_menu(poison_menu)
				if choice == 0:
					break
				elif choice == 1:
					stream.initialize('arp')
				elif choice == 2:
					stream.initialize('dns')
				elif choice == 3:
					stream.initialize('dhcp')
				elif choice == -1:
					pass
		elif choice == 2:
			while True:
				choice = print_menu(dos_menu)
				if choice == 1:
					stream.initialize('ndp')
				elif choice == 2:
					stream.initialize('nestea')
				elif choice == 3:
					stream.initialize('land')
				elif choice == 4:
					stream.initialize('tcp_syn')
				elif choice == 5:
					stream.initialize('smb2')
				elif choice == 6:
					stream.initialize('dhcp_starv')
				elif choice == 0:
					break
				elif choice == -1:
					pass
				else:
					os.system('clear')
		elif choice == 3:
			while True:
				choice = print_menu(sniffer_menu)
				if choice == 0:
					break
				elif choice == 1:
					stream.initialize('http_sniffer')
				elif choice == 2:
					stream.initialize('password_sniffer')
				elif choice == -1:
					pass
		elif choice == 4:
			while True:
				choice = print_menu(scanner_menu)
				if choice == 0:
					break
				elif choice == 1:
					stream.initialize('net_map')
				elif choice == 2:
					stream.initialize('service_scan')
				elif choice == 3:
					stream.initialize('ap_scan')
				elif choice == -1:
					pass
		elif choice == 5:
			while True:
				choice = print_menu(parameter_menu)
				if choice == 0:
					break
				elif choice == 1:
					stream.initialize('wep_crack')	
				elif choice == 2:
					print '[-] Not implemented.'
				elif choice == 3:
					stream.initialize('router_pwn')	
				elif choice == -1:
					pass
		elif choice == 6:
			session_manager.menu()
		elif choice == -1:
			pass

	
# Application entry
if __name__=="__main__":
	# perm check
	if int(os.getuid()) > 0:
		print "[-] Please run as root."
		sys.exit(1)
	# check for forwarding
	if not getoutput('cat /proc/sys/net/ipv4/ip_forward') == '1':
		print '[-] IPv4 forwarding disabled.  Enabling..'
		tmp = getoutput('sudo sh -c \'echo "1" > /proc/sys/net/ipv4/ip_forward\'')	
		if len(tmp) > 0:
			print '[-] Error enabling IPv4 forwarding.'
			sys.exit(1)
	main()