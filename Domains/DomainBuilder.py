import json
from nltk.corpus import wordnet

# this part goes into the NLProcessor


def synonymizer(word):
    print(word)
    synlist = wordnet.synsets(word)
    print(synlist)
    for item in synlist:
        lemmalist = item.lemmas()
        for lemma in lemmalist:
            print(lemma.name())

# This part stays in the domainbuilder

# domain needs:
# - domain name (set by user)
# - intent name (set by user)
# - domain context (made up of noun and verb?)
# - noun (intent object)
# - verb (intent action)
# - command
# - ?


# show existing domains/intents

# handle raw input

#d_name = input("Please enter the domain name: ")
#i_name = input("Please enter the intent name: ")
#d_noun = input("Please enter the intent object (domain noun): ")
#d_verb = input("Please enter the intent action (domain verb): ")
d_name = "websearch"
i_name = "websearch"
d_noun = ""
d_verb = "switch_on"

d_context = d_verb + " " + d_noun
d_command = ""


# create data structure, then compare what's there

data = json.dumps({"domain_name": d_name,
                         "intent": { "intents": [
                                    {"intent_name": i_name, "domain_noun": d_noun,
                                    "domain_verb": d_verb, "domain_context": d_context,
                                    "domain_command": d_command}]}}, sort_keys=True, indent=4)
print(data)
jsondata = json.loads(data)



# check if a file with name == d_name already exists

filename = str(jsondata['domain_name']) + ".json"
print(filename)

try:
    with open(filename, "x") as file:
        print("no file present, creating domain file: {0}".format(filename))
        intentdata = jsondata['intent']
        json.dump(intentdata, file)
        file.close()


except:
    with open(filename, "r") as file:
        domaindata = json.load(file)
        file.close()

        if domaindata:

            dataToAdd = False

            for entry in domaindata['intents']:

                if not entry['domain_context'] == jsondata['intent']['intents'][0]['domain_context']:
                    dataToAdd = jsondata['intent']['intents'][0]

                else:
                    print("Domain context already exists")
                    dataToAdd = False


            if dataToAdd:
                domaindata['intents'].append(jsondata['intent']['intents'][0])
                print("Adding new data")
                with open(filename, "w") as file:
                    json.dump(domaindata, file)
                    file.close()
















