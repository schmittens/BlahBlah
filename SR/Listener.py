import speech_recognition as sr
from multiprocessing.dummy import Pool as Threadpool
#import itertools
from timeit import default_timer as timer


# simple dictionary that can be read from a file
providers = {
    'google' : {'function' : 'recognize_google', 'username' : None, 'password': None},
    'ibm' :  { 'function' : 'recognize_ibm',  'username' : 'da791786-9a22-4abd-acd3-ae71df014a5a', 'password' : 'IyVzIaNtyGtM'}
}


class Listener:
    def __init__(self, providers=['google']):
        self.recognizer = sr.Recognizer()
        self.source = sr.Microphone()
        self.providers = providers
        self.results = []
        self.userprompt = "Speak now"

        print(self.userprompt)


    def multiListener(self, provider_name):
        print("{0}: Starting multiListener".format(provider_name))

        start = timer()

        provider = providers[provider_name]
        recognizer_function = provider['function']
        username = provider['username']
        password = provider['password']

        try:
            # simplifying here by assuming that all the providers will have a username and password OR neither - that might not be the case!
            if username and password:
                speechString = getattr(self.recognizer, recognizer_function)(self.audio, username=username, password=password)
            else:
                speechString = getattr(self.recognizer, recognizer_function)(self.audio)

            print("{0}: recognition successful".format(provider_name))

        except sr.UnknownValueError as e:
            speechString = provider_name + " Speech Recognition could not understand audio; {0}".format(e)
        except sr.RequestError as e:
            speechString = "Could not request results from " + provider_name + " Speech Recognition service; {0}".format(e)

        self.results.append(speechString)

        print(provider_name + ": " + speechString)

        end = timer()
        print(end - start)


    # based on http://stackoverflow.com/questions/2846653/how-to-use-threading-in-python
    def multiListen(self):
        with self.source as source:
            self.audio = self.recognizer.record(source, duration=5, offset=None)
            # audio = self.recognizer.listen(source)

        if self.audio:
            print("Audio complete")

        pool = Threadpool(len(self.providers))
        #results = pool.starmap(self.multiListener, zip(itertools.repeat(self.audio), self.providers))
        results = pool.map(self.multiListener, self.providers)
        pool.close()
        pool.join()
        print(self.results)




    def listen(self):
        with self.source as source:
            audio = self.recognizer.record(source, duration=5, offset=None)

        for provider in self.providers:
            print(provider)

        try:
            self.string = self.recognizer.recognize_google(audio)
        except sr.UnknownValueError as e:
            self.string = "Google Speech Recognition could not understand audio; {0}".format(e)
        except sr.RequestError as e:
            self.string ="Could not request results from Google Speech Recognition service; {0}".format(e)
        return self.string


