#!/bin/bash


PRIVATE_KEYS_PATH="${HOME}/.ssh/private_keys.txt"
KEY=$(grep clueai_api_key "$PRIVATE_KEYS_PATH")
KEY=${KEY#* }
echo $KEY


# https://www.clueai.cn/doc/#%E5%9B%BE%E7%89%87%E7%94%9F%E6%88%90%E7%A4%BA%E4%BE%8B%E8%BE%93%E5%87%BA

curl --location --request POST 'https://www.clueai.cn/modelfun/api/serving_api'     --header 'Content-Type: application/json' \
--header 'Model-name: clueai-base' \
--data '{
       "task_type": "classify",
       "task_name": "产品分类",
       "input_data": ["强大图片处理器，展现自然美丽的你,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
       "labels": ["美颜", "二手", "外卖", "办公", "求职"]
       }'


echo
echo
echo


curl --location --request POST 'https://www.modelfun.cn/modelfun/api/serving_api' \
  --header 'Content-Type: application/json' \
  --header 'Model-name: clueai-large' \
  --header "Api-Key: BEARER $KEY" \
  --data '{
       "task_type": "classify",
       "task_name": "产品分类",
       "input_data": ["强大图片处理器，展现自然美丽的你,,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
       "labels": ["美颜", "二手", "外卖", "办公", "求职"]
       }'
       


echo
echo
echo



curl --location --request POST 'https://www.clueai.cn/modelfun/api/serving_api'     --header 'Content-Type: application/json'     --header 'Model-name: clueai-base'     --data '{
       "task_type": "generate",
       "task_name": "信息抽取",
       "input_data":["信息抽取：\n据新华社电广东省清远市清城区政府昨日对外发布信息称,日前被实名举报涉嫌勒索企业、说“分分钟可以搞垮一间厂”的清城区环保局局长陈柏,已被免去清城区区委委员\n问题：机构名，人名，职位\n答案："]
       }'




