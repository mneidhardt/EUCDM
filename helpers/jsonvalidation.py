from jsonschema import validate, ValidationError, Draft7Validator, FormatChecker
import json
import sys
import math
import decimal

def readJsonfile(filename):
    with open(filename) as f:
        return json.load(f, parse_float=decimal.Decimal)

# https://github.com/Julian/jsonschema/issues/247
# In order to validate using multipleOf and decimal numbers, I found it necessary
# to use parse_float in json.loads:
def decimalloads(jsonstring):
    return json.loads(jsonstring, parse_float=decimal.Decimal)

def valider(schema, data):
    try:
        validate(instance=data, schema=schema, format_checker=FormatChecker())
        #for k in FormatChecker.checkers:
        #    print(k)
    except NameError as nerr:
        return [False, nerr]
    except ValidationError as verr:
        return [False, verr]
    else:
        return [True, 'OK, valideret.']
            
if len(sys.argv) == 3:
    schemafile = sys.argv[1]
    datafile = sys.argv[2]
    res = valider(readJsonfile(schemafile), readJsonfile(datafile))
    if res[0]:
        print('OK')
    else:
        print(res[1].message)
elif len(sys.argv) == 1:
    multiple = 0.00001
    schema = {"$schema": "https://json-schema.org/draft/2019-09/schema",
              "type": "object",
              "additionalProperties": False,
              "properties": {
                  "xrate": { 
                      "type" : "number",
                      "minimum": 0.0,
                      "maximum": 999999999999.00,
                      "multipleOf": multiple
                      }
                  }
              }

    schema = decimalloads(json.dumps(schema))
    inst = []
    inst.append(decimalloads('{"xrate" : 4856545.76790}'))
    inst.append(decimalloads('{"xrate" : 4856545.76791}'))
    inst.append(decimalloads('{"xrate" : 4856545.76792}'))
    inst.append(decimalloads('{"xrate" : 4856545.76793}'))
    inst.append(decimalloads('{"xrate" : 4856545.76794}'))
    inst.append(decimalloads('{"xrate" : 4856545.76795}'))
    inst.append(decimalloads('{"xrate" : 4856545.76796}'))
    inst.append(decimalloads('{"xrate" : 4856545.76797}'))
    inst.append(decimalloads('{"xrate" : 4856545.76798}'))
    inst.append(decimalloads('{"xrate" : 4856545.76799}'))
    inst.append(decimalloads('{"xrate" : 4856545.76800}'))
    inst.append(decimalloads('{"xrate" : 5.76793}'))
    inst.append(decimalloads('{"xrate" : 45.76793}'))
    inst.append(decimalloads('{"xrate" : 545.76793}'))
    inst.append(decimalloads('{"xrate" : 6545.76793}'))
    inst.append(decimalloads('{"xrate" : 56545.76793}'))
    inst.append(decimalloads('{"xrate" : 856545.76793}'))
    inst.append(decimalloads('{"xrate" : 4856545.76793}'))
    inst.append(decimalloads('{"xrate" : 4856545.7679}'))
    inst.append(decimalloads('{"xrate" : 4856545.767}'))
    inst.append(decimalloads('{"xrate" : 4856545.76}'))
    inst.append(decimalloads('{"xrate" : 4856545.7}'))
    inst.append(decimalloads('{"xrate" : 4856545.0}'))
    inst.append(decimalloads('{"xrate" : 4856545}'))
    for instance in inst:
        res = valider(schema, instance)
        if not res[0]:
            # print(res[1])
            print(res[1].message, instance['xrate'], f"{0.00001:.65f}")
        else:
            print('OK. ', f"{instance['xrate']:.64f}")

        #r1 = math.remainder(instance['xrate'], multiple)
        #r2 = instance['xrate'] % multiple
        #print('    Remainder: ', f"{r1:.65f}")
        #print('    %        : ', f"{r2:.65f}")
else:
    print(sys.argv[0] + ': Without args, run built-in test.')
    print(sys.argv[0] + ' schemafile instancefile: With 2 args, validate instancefile with schemafile.')
