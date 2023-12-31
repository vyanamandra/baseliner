import os
import json
import argparse
import subprocess
import configparser

INVENTORY_TEMPLATE = '{datacenter}_{nodename} ansible_host={node_ip} ansible_connection=ssh ansible_user={user} ansible_private_key_file={ssh_private_key}'

def remove_config_section_if_exists(config, prefix, suffixes):
	for suffix in suffixes:
		try:
			config.remove_section(f'{prefix}_{suffix}')
		except:
			pass

def main(args):
	inventory = 'inventory/hosts'
	if args.inventory:
		inventory = args.inventory	
	tf_nodes = {}
	os.chdir(args.location)
	try:
		result = subprocess.run(['terraform', 'output', '-json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		tf_nodes = json.loads(result.stdout.decode('utf-8'))
	except:
		pass	

	config = configparser.ConfigParser(allow_no_value = True)
	config.read(inventory)
	
	remove_config_section_if_exists(config, args.datacenter, ['nodes', 'servers', 'clients', 'mgmt', 'mgw'])

	config[f'{args.datacenter}_nodes'] = {}
	nid = 0
	for pubip in tf_nodes['provisioned_nodes']['value']:
		config[f'{args.datacenter}_nodes'][INVENTORY_TEMPLATE.format(datacenter=args.datacenter, nodename=f'node{nid}', node_ip = pubip, user = 'ubuntu', ssh_private_key = args.sshkey)] = None
		nid += 1

	num_servers = int(args.servers)
	num_clients = int(args.clients)
	config[f'{args.datacenter}_servers'] = {}
	for nid in range(num_servers):
		config[f'{args.datacenter}_servers'][f'{args.datacenter}_node{nid}'] = None

	config[f'{args.datacenter}_clients'] = {}
	print (f'{num_servers}, {num_servers+num_clients}')
	for nid in range(num_servers, num_servers+num_clients):
		config[f'{args.datacenter}_clients'][f'{args.datacenter}_node{nid}'] = None

	if not f'{args.task}_nodes' in config.keys():
		config[f'{args.task}_nodes'] = {}

	for nid in range(num_servers+num_clients):
		try:
			config[f'{args.task}_nodes'][f'{args.datacenter}_node{nid}'] = None
		except:
			pass

	config[f'{args.datacenter}_mgmt'] = {}
	config[f'{args.datacenter}_mgmt'][f'{args.datacenter}_node0'] = None

	config[f'{args.datacenter}_mgw'] = {}
	config[f'{args.datacenter}_mgw'][f'{args.datacenter}_node{num_servers+num_clients-1}'] = None

	with open(inventory, 'w') as config_file:
		config.write(config_file, space_around_delimiters=False)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='add_new_nodes_to_inventory.py',
					description = 'Add newly created servers to the right config blocks of our inventory')
					
	parser.add_argument('-i', '--inventory', help = 'inventory file')
	parser.add_argument('-d', '--datacenter', help = 'datacenter these hosts beong to')
	parser.add_argument('-s', '--servers', help = 'number of server agents')
	parser.add_argument('-c', '--clients', help = 'number of client agents')
	parser.add_argument('-t', '--task', help = 'task name')
	parser.add_argument('-l', '--location', help = 'location where terraform output is to be run')
	parser.add_argument('-k', '--sshkey', help = 'SSH private key file to login to the nodes')
	args = parser.parse_args()
	main(args)
