variable "iname" {
type=string
default="server-1"
}

variable "ienv" {
type=string
default="Dev"
}

variable "iami" {
type=string
default="ami-000d209a4fc9822c4"
}

variable "itype" {
type=string
default="m7i-flex.large"
}


variable "isize" {
type=number
default=30
}

variable "icount" {
type=number
default=1
}

variable "izone" {
type=string
default="us-east-1a"
}
