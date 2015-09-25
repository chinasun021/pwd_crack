#!/usr/bin/expect -f
set cert [lindex $argv 0]
set password [lindex $argv 1]
spawn openssl
expect "OpenSSL>"
send "pkey -in $cert -out privatekey.tmp\r"
expect "Enter pass phrase for privatekey.pem:"
send "$password\r"
expect {
	"unable to load key*" {puts "\r";return 0}
	"OpenSSL>" {puts "\r";return 1}
}
expect eof
exit