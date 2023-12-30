terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}


variable "ami" {
  default = {
    "{{ CONSUL_VM_AWS_REGION }}" = "{{ CONSUL_VM_AMI_IMAGE }}"
  }
}

variable "instance_count" {
  default = {{ (CONSUL_VM_SERVER_COUNT | int) + (CONSUL_VM_CLIENT_COUNT | int) }}
}

variable "key_name" {
  default = "{{ CONSUL_VM_KEY_NAME }}"
}

variable "instance_type" {
  default = "{{ CONSUL_VM_INSTANCE_TYPE }}"
}

variable "aws_region" {
  default = "{{ CONSUL_VM_AWS_REGION }}"
}

variable "security_groups" {
  default = ["{{ CONSUL_VM_SECURITY_GROUP }}"]
}


resource "aws_instance" "consul-servers" {
  count         = var.instance_count
  ami           = lookup(var.ami,var.aws_region)
  instance_type = var.instance_type
  key_name      = var.key_name
  security_groups = var.security_groups

  tags = {
    Name  = "{{ CONSUL_VM_NAME_TAG_PREFIX }}-{{ DC_NORM }}-n${count.index + 1}"
    Owner = "{{ CONSUL_VM_OWNER_TAG }}"
  }
}

output "provisioned_nodes" {
  description = "List of public IP addresses assigned to the instances"
  value = "${aws_instance.consul-servers.*.public_ip}"
}
