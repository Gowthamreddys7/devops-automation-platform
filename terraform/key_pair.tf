resource "aws_key_pair" "mykey" {

key_name="projectkey"

public_key=file("~/.ssh/id_rsa.pub")
}

