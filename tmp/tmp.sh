
#!/bin/bash
export debug=0
[[ "$2" == "d" ]] && export debug=1

#LP=/var/www/dav/tmp/
export LP=/home/liqsliu/tera/var/xmpp/
#LP=/tmp/
export DOMAIN=liuu.tk
export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )



debug=${debug-0}
[[ "$2" == "d" ]] && debug=${debug-1}

LP=${LP-/var/www/dav/tmp/}
DOMAIN=${DOMAIN-liuu.tk}
SH_PATH=${SH_PATH-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}





debug=0
[[ "$2" == "d" ]] && debug=1

#LP=/var/www/dav/tmp/
LP=/home/liqsliu/tera/var/xmpp/
#LP=/tmp/
DOMAIN=liuu.tk
SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )



#!/bin/bash
export LP=/var/www/dav/tmp
export DOMAIN=liuu.tk
export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
export MAX_SHARE_FILE_SIZE=15000000



os := import("os")
if msgUsername != "bot" {
if msgChannel != "-1001292248509" {
if msgText != "null" {
cmd := os.exec("/home/liqsliu/twitter_to_text.sh", msgText, msgUsername, msgChannel, msgAccount)
cmd_out := cmd.output()
if cmd_out != "null" {
//  msgText=msgText+cmd_out
  msgText=cmd_out
}

}
}
}
