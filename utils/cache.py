import memcache

cache = memcache.Client(['172.18.20.95:11211'],debug=True)

def set(key,value,timeout=60):
    #重写之后可以灵活添加代码
    return  cache.set(key,value,timeout)
def get(key):
    return cache.get(key)

def delete(key):
    return delete(key)

