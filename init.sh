#!/bin/bash




#SH_PATH="/run/user/1000"
#echo "$SH_PATH" > SH_PATH
[[ -n "$1" ]] && SH_PATH=$1 || SH_PATH=$(cat SH_PATH)

cp SH_PATH "$SH_PATH/"
cp DOMAIN "$SH_PATH/"


cp *.sh "$SH_PATH"/
rm "$SH_PATH/init.sh"
cp *.py "$SH_PATH"/
cp *.tengo "$SH_PATH"/
chmod +x "$SH_PATH"/*.sh
chmod +x "$SH_PATH"/*.py
chmod +x "$SH_PATH"/*.tengo


#cp ~/keys "$SH_PATH/"
#cp ~/keys "./"


cp group_cmd.txt "$SH_PATH/"
cp group_help.txt "$SH_PATH/"
cp group_help_xmpp.txt "$SH_PATH/"
cp group_help_tox.txt "$SH_PATH/"
cp group_help_*.txt "$SH_PATH/"



#touch "$SH_PATH/group_note.txt"
# [[ -e "$SH_PATH/group_note.txt" ]] && cp "$SH_PATH/group_note.txt" "$(cd $(dirname ${BASH_SOURCE[0]}); pwd )/" || cp "$(cd $(dirname ${BASH_SOURCE[0]}); pwd )/group_note.txt" "$SH_PATH/"

# [[ -e "$SH_PATH/$file_name" ]] && cp "$SH_PATH/$file_name" "$(cd $(dirname ${BASH_SOURCE[0]}); pwd )/"
file_name=group_note.txt
[[ -e "$SH_PATH/$file_name" ]] && cp "$SH_PATH/$file_name" "$(cd $(dirname ${BASH_SOURCE[0]}); pwd )/" || cp "$(cd $(dirname ${BASH_SOURCE[0]}); pwd )/$file_name" "$SH_PATH/"



