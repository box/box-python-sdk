# Getting raw json response

The response returned by an API endpoint is being automatically translated to the corresponding
object basing on the value of the`type` field. If you want to get the raw response object,
you can access response dict using `response_object` property. Example below will print the
raw json response returned by the API.

``` python
file = client.file('1122334455').get()
print(json.dumps(file.response_object))
```
