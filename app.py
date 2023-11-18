import queue
import sounddevice as sd
import vosk
import json
import words
from skills import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

q = queue.Queue()

model = vosk.Model('vosk-model-small-ru-0.22')

device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
print(samplerate)


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    target = words.triggers.intersection(data.split())
    if not target:
        return

    data.replace(list(target)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    print(answer)

    func_name = answer.split()[0]
    speaker(answer.replace(func_name, ''))
    exec(func_name + '()')


def main():

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0],
                           dtype="int16", channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)
            # else:
            #     print(rec.PartialResult())


if __name__ == '__main__':
    main()