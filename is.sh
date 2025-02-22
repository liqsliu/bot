#!/bin/bash

if [[ -z "$1" ]]; then
  echo "image search"
  echo ".is \$image_url"
else
  url=$1

  # from telegram bot @soutubot
  # echo "https://www.google.com/searchbyimage?&image_url=https://img1.acgvia.workers.dev/photos/file_1.jpg?&client=firefox-bd"
  echo google
  echo "https://www.google.com/searchbyimage?&image_url=${url}?&client=firefox-bd"
  # https://lens.google.com/uploadbyurl?url=https://img1.acgvia.workers.dev/photos/file_1.jpg
  echo google lens
  echo "https://lens.google.com/uploadbyurl?url=$url"

  echo yandex
  echo "https://yandex.com/images/search?url=${url}&rpt=imageview"

  echo bing
  echo "https://www.bing.com/images/search?q=imgurl:${url}&view=detailv2&iss=sbi"

  url2=$(echo "$url"|sed -e 's|^http://||' -e 's|^https://||' -e 's|/|%2F|g')
  echo tineye
  echo "https://tineye.com/search?url=https://images.weserv.nl/?url=$url2"
  echo "https://tineye.com/search?url=$url"

  echo saucenao
  echo "https://saucenao.com/search.php?url=$url"

  echo ascii2d
  echo "https://ascii2d.net/search/url/https://images.weserv.nl/?url=$url2"
  echo "https://ascii2d.net/search/url/$url"

  echo --
  echo trace
  echo "https://trace.moe/?auto&url=$url"

  echo iqdb
  echo "http://iqdb.org/?url=$url"

  echo iqdb 3d
  echo "http://3d.iqdb.org/?url=$url"

  echo karmdecay
  echo "http://karmadecay.com/search?q=$url"

fi
