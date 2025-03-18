import sys, os

path = os.path.abspath(os.path.dirname(__file__))

convo = []
with open(path + '/convo.txt', 'rb') as f:
    for line in f:
        who = line.split(b'>')[0][1:]
        convo.append((who, line.split(b'>')[1]))

impostor = {
    b"Alice": b"<Alice> Hey, you're not Bob! Who's monitoring our connection!? Get out!!",
    b"Bob": b"<Bob> Alice doesn't talk like that. Who in the blazes are you?"
}

myself = os.environ["USER"].encode('utf-8')
assert myself == b"Alice" or myself == b"Bob"
other = {b"Alice": "Bob", b"Bob": "Alice"}[myself]

def alice_or_bob(recv, send):
    for author, msg in convo:
        composite = b'<' + author + b'> ' + msg
        if author == myself:
            send(composite)
        else:
            m = recv()
            if composite != m:
                send(impostor[myself], raw=True)
                return
