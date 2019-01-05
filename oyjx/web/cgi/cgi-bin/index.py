#! /usr/bin/python3.6

import io
import sys
import cgi
import cgitb

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cgitb.enable()

print("Content-Type: text/html")
print()

test_html = """
<html>
    <head>
        <meta charset="utf-8"/>
        <title>Hello world</title>
    </head>
    <body>
        <h2>Hello world %s!</h2>
    </body>
</html>
"""

fs = cgi.FieldStorage()
inputs = {}

# 将cgi从web获取到的数据存入字典inputs
for key in fs.keys():
    inputs[key] = fs[key].value

for k, v in inputs.items():
    print(test_html % v)
