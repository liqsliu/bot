#!/bin/bash

# piu  --break-system-packages telethon lottie cairosvg zstandard brotli aiofile aiofiles urltitle aiohttp



#SH_PATH="/run/user/1000"
#echo "$SH_PATH" > SH_PATH
[[ -n "$1" ]] && SH_PATH=$1 || SH_PATH=$(cat SH_PATH)

[[ -e  "$SH_PATH" ]] || mkdir -p "$SH_PATH"


cp SH_PATH "$SH_PATH/"
cp DOMAIN "$SH_PATH/"
cp BOTID "$SH_PATH/"


BOTID=$(cat $SH_PATH/BOTID)
sed -i 's/BOTID: [^ ]* /BOTID: '$BOTID' /g' group_help.txt
sed -i 's/BOTID: [^ ]* /BOTID: '$BOTID' /g' group_help_tox.txt


rm "$SH_PATH"/*.sh
rm "$SH_PATH"/*.py

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
file_name=group_qun.txt
[[ -e "$SH_PATH/$file_name" ]] && cp "$SH_PATH/$file_name" "$(cd $(dirname ${BASH_SOURCE[0]}); pwd )/" || cp "$(cd $(dirname ${BASH_SOURCE[0]}); pwd )/$file_name" "$SH_PATH/"




# rm "$SH_PATH/DEBUG" || true
# rm "$SH_PATH/STOP" || true



[[ -e "$SH_PATH/.BUSY" ]] || {
  echo 2 > "$SH_PATH/.BUSY"
}





