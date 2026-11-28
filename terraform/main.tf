resource "aws_instance" "myinstance" {
tags={
Name=var.iname
Environment=var.ienv
}
ami=var.iami
instance_type=var.itype
key_name=aws_key_pair.mykey.key_name
vpc_security_group_ids=[aws_security_group.mysecurity.id]
root_block_device{
 volume_size=var.isize
}
count=var.icount
availability_zone=var.izone
}
