
# https://stackoverflow.com/questions/38911936/how-to-make-twitter-api-call-through-curl-in-unix

curl --request POST \
  --url 'https://api.twitter.com/1.1/statuses/update.json?status=Hello%20world' \
  --header 'authorization: OAuth oauth_consumer_key="CONSUMER_API_KEY", oauth_nonce="OAUTH_NONCE", oauth_signature="OAUTH_SIGNATURE", oauth_signature_method="HMAC-SHA1", oauth_timestamp="OAUTH_TIMESTAMP", oauth_token="ACCESS_TOKEN", oauth_version="1.0"'
