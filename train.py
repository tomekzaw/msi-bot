import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

if __name__ == '__main__':
    for path in 'db.sqlite3', 'sentence_tokenizer.pickle':
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    chatbot = ChatBot('Harold')

    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.english')

    trainer = ListTrainer(chatbot)
    with open('conversations.txt', 'r') as f:
        conversations = f.read().split('\n\n')
        for one in conversations:
            conversation = one.split('\n')
            print(conversation)
            trainer.train(conversation)

    print('Finished')
