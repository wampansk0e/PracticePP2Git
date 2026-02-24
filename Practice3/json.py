#J S O N
#JSON is a syntax for storing and exchanging data.
#If you have a JSON string, you can parse it by using the json.loads() method.
import json
x =  '{ "name":"John", "age":30, "city":"New York"}'
y = json.loads(x)
print(y["age"])

#If you have a Python object, you can convert it into a JSON string by using the json.dumps() method.
import json
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
y = json.dumps(x)
print(y)