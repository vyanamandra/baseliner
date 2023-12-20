#MY_PUBIP_ADDR=$(dig +short myip.opendns.com @resolver1.opendns.com)

# Add my IP address to the security group
#aws ec2 authorize-security-group-ingress --dry-run --group-id sg-0e91a93d33c597fab --protocol -1 --port 22 --cidr $MY_PUBIP_ADDR/32

#aws ec2 modify-security-group-rules --group-id sg-0e91a93d33c597fab --security-group-rules "SecurityGroupRule={Description='Enable Access to all ports for venu.yanamandra@hashicorp.com',CidrIpv4=$MY_PUBIP_ADDR/32,IpProtocol=all,FromPort=0,ToPort=65535}"

# Just return the current host's IP address. 
curl -s http://whatismyip.akamai.com/
