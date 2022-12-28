from django.test import TestCase

# Create your tests here.
selectwords = {"hello": ['hello', 'hi', 'hey'],
                   "what": ['what', "why"]}
user_text = "hello fron it "

msg = ""

if any(word in user_text for word in selectwords.get("hello")):
    msg += "he you"

print(msg)    
