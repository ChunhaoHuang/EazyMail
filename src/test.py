import re
filename = "asdf行ad  78645412 哈哈哈A16.pdf"
match = re.match(r'(.*)(A)(\d+)(\.pdf)', filename)
print(match.groups())
print(match.groups()[2])