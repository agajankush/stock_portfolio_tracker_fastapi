import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
# decode_response is used to decode the response from the redis server from bytes to UTF-8 strings.
