#Use enumerate() and zip() for paired iteration
fruits = ["Apple", "Banana", "Watermelon"]
colors = ["Red", "Black", "White"]

for index, fruit in enumerate(fruits, start=1):
    print(f"Item {index}: {fruit}")

for fruit, color in zip(fruits,colors):
    print(f"Fruit: {fruit}, Color: {color}")

#Demonstrate type checking and conversions
x = "42.5"

if isinstance(x, str):
    print ("x is a string")

float = float(x)
int = int(float)

print(f"Float: {float}, Type: {type(float).__name__}" )
print(f"Integer: {int}, Type: {type(int).__name__}")

chars = ['H', 'e', 'l', 'l', 'o']
word = "".join(chars)
print(word)