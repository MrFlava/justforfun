#
# Create an application that will convert text-based configuration format into json.
# The application should accept input as file or a stdin-stream and print result into stdout.


# Sample input:

# config = 3
# config_b.items = item1
# config_b.items = item2
# config_b.items.named_item = 123
# config_c.root.a.b.c = 13

# Expected output for sample input:

# {
#    "config":3,
#    "config_b":{
#       "items":{
#          "0":"item1",
#          "1":"item2",
#          "named_item":123
#       }
#    },
#    "config_c":{
#       "root":{
#          "a":{
#             "c":13
#          }
#       }
#    }
# }
#
import re
import sys
import json
# import configparser#
# parse = configparser.ConfigParser()


def nested_dict(keys, value):
    return {keys[0]: nested_dict(keys[1:], value)} if keys else value


output_dict = {}

for line in sys.stdin:
    if 'q' == line.rstrip():
        break

    in_key, _, in_value = line.strip().partition("=")
    keys = in_key.strip().split(".")
    val = in_value.strip()
    if val.isnumeric():
        val = int(val)
    output_dict[keys[0]] = nested_dict(keys[1:], value=val)

out_file = open("output.json", "w")

json.dump(output_dict, out_file)
out_file.close()
