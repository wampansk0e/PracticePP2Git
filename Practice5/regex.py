#Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re

def match(text):
    pattern = '^ab*$'
    
    if re.fullmatch(pattern, text):
        return f"'{text}' is a match"
    else:
        return f"'{text}' does not match"

test = ["a", "ab", "abbb", "b", "abc"]

for s in test:
    print(match(s))

#Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
import re

def match(text):
    pattern = r'^ab{2,3}$'
    
    if re.fullmatch(pattern, text):
        return f"'{text}' is a match"
    else:
        return f"'{text}' does not match"

test = ["a", "ab", "abbb", "b", "abc"]

for s in test:
    print(match(s))

#Write a Python program to find sequences of lowercase letters joined with a underscore.
import re

def match(text):
    pattern = r'[a-z]+_[a-z]+'
    
    if re.fullmatch(pattern, text):
        return f"'{text}' is a match"
    else:
        return f"'{text}' does not match"

test = ["a-b", "hello_world", "hello world", "Hello_World", "abc"]

for s in test:
    print(match(s))

#Write a Python program to find the sequences of one upper case letter followed by lower case letters.
import re

def match(text):
    pattern = r'[A-Z][a-z]+'
    
    if re.fullmatch(pattern, text):
        return f"'{text}' is a match"
    else:
        return f"'{text}' does not match"

test = ["Hello", "hello World", "Hello World", "abc"]

for s in test:
    print(match(s))

#Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
import re

def match(text):
    pattern = r'^a.*b$'
    
    if re.fullmatch(pattern, text):
        return f"'{text}' is a match"
    else:
        return f"'{text}' does not match"

test = ["ab", "axxb", "abc", "apple b"]

for s in test:
    print(match(s))

#Write a Python program to replace all occurrences of space, comma, or dot with a colon.
import re

def colon(text):
    pattern = r'[ ,.]'
    
    res = re.sub(pattern, ':', text)
    return res

test = ["Hello, world!", "Hello world!", "Hello world.", "Hello, World."]

for s in test:
    sub = colon(s)
    print(sub)

