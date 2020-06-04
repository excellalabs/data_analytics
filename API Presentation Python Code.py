import pandas as pd
import requests
import json

# !Elements of the Get Request

api_url = "https://api.data.gov/sam/v3/registrations"
api_key = 'VpTi8pF59uRnH9TY5djWg8YUWVNgeOut39RiEL1G'
status = 'registrationStatus:A'
zipcode = 'samAddress.zip:22201'

# ? Instead of using params, you can also build the full URL and run the following:
# ? api_url = https://api.data.gov/sam/v3/registrations?qterms=registrationStatus:A+AND+samAddress.zip:22201&length=5&api_key=VpTi8pF59uRnH9TY5djWg8YUWVNgeOut39RiEL1G
# ? response = requests.get(api_url)

# *Can build the parameters dictionary by concatenating the strings

params = {'qterms': status + '+AND+' +
          zipcode, 'api_key': api_key, 'length': 5}

print(params)

#!Calling the API

response = requests.get(api_url, params=params)
print(response)

# in this case, status code 200 means the request was successful
print(response.status_code)

# Print this to see the possible headers
print(response.headers)

# This tells you that this particular API will return a JSON object
print(response.headers['Content-Type'])
# This will tell you how many more calls you can make with this api-key and IP address on this day
print(response.headers['X-RateLimit-Remaining'])

# !Parsing JSON
# * read response as JSON object
data = response.json()

print(data)

# *print a more JSON object
print(json.dumps(data, indent=4))
# If indent is a non-negative integer or string, then JSON will be printed with that indent level

# * Write data to a JSON file to examine
with open('data.json', 'w') as outfile:
    outfile.write(json.dumps(data, indent=4))

# define results because we dont care about the 'links' part of the JSON
results = data['results']

with open('results.json', 'w') as outfile:
    outfile.write(json.dumps(results, indent=4))


# TODO  Use a JSON path to yield result (key, value pairs)
# get the cage number from the second result
cage_number_2 = results[2]['cage']

print(cage_number_2)

# ? With deeply nested JSON objects can have a path that looks like
# ? value_n = JSON_object[index_1]['key_1']['key_2'][index_2][key_3]...['key_n']

# TODO Create a list of values
# Use for loop to list all of the cage numbers
results_list = []
for i in list(range(0, len(results))):
    results_list.append(results[i]['cage'])

print(results_list)

# TODO Create a list of two values as key-value pairs
# use a for loop to create a dictionary that assigns the value cage number to the corresponding key legalBusinessName
# Can extend this such that values are a list of values
results_dict = {}
for i in list(range(0, len(results))):
    var_name = results[i]['legalBusinessName']
    results_dict[var_name] = results[i]['cage']

print(results_dict)

# turn dictionary into a data frame, where the indexes are numbers and the columns are the keys and the values
# just using pd.DataFrame(results_dict) will create a column of the values that has the keys as indexes

results_df = pd.DataFrame(list(results_dict.items()), columns=[
                          'legalBusinessName', 'cage'])

print(results_df)


# ! Flatten whole response

# TODO use pd.json_normalize to flatten
# Note that json_normalize is a pandas function.  Use this turn a JSON object into tabular data.
# Python deals with dictionaries and arrays better than data frames, unlike excel and R, but this can still be a very useful tool for viewing and displaying information

df_normalized = pd.json_normalize(results, sep="_")

print(df_normalized)

print(df_normalized['links'])

# *using parameters record_path and meta
links_flatten = pd.json_normalize(results, record_path='links')
print(links_flatten)

# print(results['cage'], results['samAddress']['zip'])
# TypeError: list indices must be integers or slices, not str
# this means that there are multiple ['samAddress'], and thus we need to include and index to tell python which to choose

# * meta
print(results[0]['cage'], results[0]['samAddress']['zip'])

# * record_path
print(results[0]['links'])

# This is one row of data
row_0 = pd.json_normalize(results[0], record_path='links', meta=['cage', 'hasKnownExclusion', 'legalBusinessName', 'duns', 'debtSubjectToOffset', 'duns_plus4', 'status', 'expirationDate', [
    'samAddress', 'zip'], ['samAddress', 'stateOrProvince'], ['samAddress', 'city'], ['samAddress', 'countryCode'], ['samAddress', 'zip4'], ['samAddress', 'line1']], sep="_")

print(row_0)

# Because an index is needed, if there are a lot of results it is more efficient to use a loop
df_normalized2 = pd.DataFrame([])
for i in range(0, len(results)):
    row = pd.json_normalize(results[i], record_path='links', meta=['cage', 'hasKnownExclusion', 'legalBusinessName', 'duns', 'debtSubjectToOffset', 'duns_plus4', 'status', 'expirationDate', [
                            'samAddress', 'zip'], ['samAddress', 'stateOrProvince'], ['samAddress', 'city'], ['samAddress', 'countryCode'], ['samAddress', 'zip4'], ['samAddress', 'line1']])
    df_normalized2 = df_normalized2.append(row)

print(df_normalized2)


# 1 to 1 series
# This will create an entirely flat series where there is a unique name for each value.

def flatten_nested_json_recursive(nested_json):

    flattened_result = {}

    def flatten_json(data, key=''):
        if type(data) is dict:
            for i in data:
                flatten_json(data[i], key + i + '_')
        elif type(data) is list:
            f = 0
            for i in data:
                flatten_json(i, key + str(f) + '_')
                f += 1
        else:
            flattened_result[key[:-1]] = data

    flatten_json(nested_json)
    return flattened_result


flattened_result = pd.Series(flatten_nested_json_recursive(results))
print(flattened_result)


#! Error Handling

# # TODO Method 1: if/then

# print(response.status_code)

# api_key_error is missing a character and thus will throw a 403 error
api_url = "https://api.data.gov/sam/v3/registrations"
api_key_error = 'VpTi8pF59uRnH9TY5djWg8YUWVNgeOut39RiEL1'
params = {'qterms': status + '+AND+' +
          zipcode, 'api_key': api_key_error, 'length': 5}

response = requests.get(api_url, params=params)
if response.status_code != 200:
    print("error: " + str(response.status_code))
else:
    print("success!")

# This one is the same query but uses the correct api_key
params = {'qterms': status + '+AND+' +
          zipcode, 'api_key': api_key, 'length': 5}

response = requests.get(api_url, params=params)
if response.status_code != 200:
    print("error: " + str(response.status_code))
else:
    print("success!")

# * for a looped request


duns4 = ['0230433700000', '1240234040000', '8588887610000', '858887610000', '1280234040000'
         ]

# Because some of these duns throw errors, when the loop will stop at the first error and not continue looping
for i in duns4:
    api_url = "https://api.data.gov/sam/v8/registrations/" + str(i)
    params = {'return_values': 'full',
              'api_key': 'pZRf3NHMazUCn8CxibYQWC9qttnh7EHmFPkSYoTO'}
    response = requests.get(api_url, params=params)
    data = response.json()
    # print(str(i) + " success!")
    x = data['sam_data']['registration']['businessStartDate']
    print(x)

# This loop will print the required data from the requests with a 200 response and print the type of error for the errors
for i in duns4:
    api_url = "https://api.data.gov/sam/v8/registrations/" + str(i)
    params = {'return_values': 'full',
              'api_key': 'pZRf3NHMazUCn8CxibYQWC9qttnh7EHmFPkSYoTO'}
    response = requests.get(api_url, params=params)
    data = response.json()
    if response.status_code != 200:
        print(str(i) + " error: " + str(response.status_code))
    else:
        # print(str(i) + " success!")
        x = data['sam_data']['registration']['businessStartDate']
        print(x)


# TODO Method 2: Try/Except

# Look into try/except statements, especially notes on else: and finally:
# Also look into using commands like continue and break
# Read about the different Python exceptions you can use to specify what to do given a specific error
    # using "except:" without a term after except sends all errors to the except phrase

for i in duns4:
    api_url = "https://api.data.gov/sam/v8/registrations/" + str(i)
    params = {'return_values': 'full',
              'api_key': 'VpTi8pF59uRnH9TY5djWg8YUWVNgeOut39RiEL1G'}
    response = requests.get(api_url, params=params)
    data = response.json()
    try:
        x = data['sam_data']['registration']['businessStartDate']
        print(x)
    except:
        print(str(i) + " error: " + str(response.status_code))
        continue

# TODO including a timeout option
# You can add a timeout exception so the query will stop a request that is taking too long getting a response

try:
    response = requests.get('https://api.github.com', timeout=1)
except Timeout:
    print('The request timed out')
else:
    print('The request did not time out')


# TODO using rate limit with a while loop
# The following assigns the rate limit of your api-key to x and subtracts one from x after each call
# This is useful since even if you run out of calls, your loop withh continue running adn just throw a series of 429 errors, indicating too many requests have been made

print(response.headers['X-RateLimit-Remaining'])

x_response = requests.get(
    'https://api.data.gov/sam/v8/registrations/1240234040000?return_values=full&api_key=pZRf3NHMazUCn8CxibYQWC9qttnh7EHmFPkSYoTO')
x = int(x_response.headers['X-RateLimit-Remaining'])
print(x)
while x != 0:
    for i in duns4:
        api_url = "https://api.data.gov/sam/v8/registrations/" + str(i)
        params = {'return_values': 'full',
                  'api_key': 'pZRf3NHMazUCn8CxibYQWC9qttnh7EHmFPkSYoTO'}
        response = requests.get(api_url, params=params)
        x = x-1
    break
    # x=response.headers['X-RateLimit-Remaining']
print(x)


# TODO a method for collecting errors
# This loop will enable you to collect the successful results in one dictionary and the failed results seperately
# This can be useful for checking on errors and for re-running errors
duns4 = ['0230433700000', '8487079310000', '1240234040000',
         '8588887610000', '8487079310000', '0802394200000', '5061655360000']

sam_results_dict = {}
except_dict = {}

for i in duns4:
    api_url = "https://api.data.gov/sam/v8/registrations/" + str(i)
    params = {'return_values': 'full',
              'api_key': api_key}
    response = requests.get(api_url, params=params)
    try:
        data = response.json()
        y = data['sam_data']['registration']['businessStartDate']
        sam_results_dict[str(i)] = y
    except:
        except_dict[str(i)] = response.status_code
        continue


print(sam_results_dict)
print(except_dict)
