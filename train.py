from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatterbot.trainers import UbuntuCorpusTrainer

if __name__ == '__main__':
    chatbot = ChatBot('Harold')

    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.english')

    print('Finished')
