# baseliner
An easy deployment &amp; demo of applications for Consul over VMs.

--> Work in progress. The code needs to be made resilient on failures (e.g., unable to bootstrap, unable to run a specific task... etc,) and it is not right now. 
but, stay tuned!


The goal is to get some resiliency on failures.

Tasks to be addressed in this branch:
1. Provisioning in AWS (nodes, security groups, ingress rules) - [Done]
2. Installing Consul.
3. Installing Envoy.
4. Installing Python pip & virtualenvs.
5. Setting up Consul (like, what if it is already working. say, there is a file that says /root/setup-complete-donodisturb) [This covers- gossip-enc, tls & acl]
6. Setting up a traditional gateway.
7. Setting up a mesh gateway.
