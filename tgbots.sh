

#SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
cd "$SH_PATH" || cd ..

if [[ "$(whoami)" == "u0_a202" ]]
then
  :
  python3 -m tg test 1 2 3 4 5
else
  SH_PATH=$(cat SH_PATH)
  [[ -d "$SH_PATH" ]] && {
    tgp
    bash init.sh
    cd "$SH_PATH"
  }
  python3 -m tg
fi
