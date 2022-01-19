import os

import openai
from PyInquirer import prompt


openai.api_key = 'API_KEY_HERE'

class Settings:
    eng = 'davinci'     # def 'davinci'
    temp = 0.7          # Temperature (def 0)
    tok = 100           # No. of tokens (def 100)
    best = 1            # Pick best out of n outputs (def 1)
    freq_pen = 0.5      # Frequency penalty (def 0.0)
    pres_pen = 0.2      # Presence penalty (def 0.0)

# TODO REFORMAT ALL FUNCTIONS SO REPEAT PROPERLY REPEATS (leave only function calls in the menu selection part)
# TODO MAYBE ONE DAY TURN THIS INTO A PACKAGE OF IT'S OWN THAT I'LL PUBLISH
"""
Need to add functionality that:
WILL SPLIT THE MAIN MENU INTO SUBMENUS FOR TYPES OF GENERATION

menu: # Add \n at the end of the last option before Return so it appears separated by a single line!
    -Generate:
        -Complete a prompt
        -Short story
        -Generate code
        -Return
    -Question & Reply:
        -Q&A
        -Word meaning
        -Explain code
        -Return
    -Transform:
        -Translate
        -Correct Grammar
        -Rewrite the sentence to sound more advanced
        -Keywords
        -Return
    -Chat
    -Other:
        -Versitile
        -Tl;dr
        -Return
    -Settings: # give ability to reset singular settings to default as well
        -Engine
        -Temperature
        -Tokens
        -Best of
        -Frequency penalty
        -Presence penalty
        -Reset all to default
        -Return
    -Exit
"""
def completion():
    prompt = str(input(f"Please input a prompt to complete:\n-"))
    try:
        tokens = int(input("How many tokens are you willing to use?\n-"))
    except ValueError:
        print("That's not a number dumbo!!!")
        print('')
        os.system("pause")
        main()
    return prompt, (openai.Completion.create(engine=Settings.eng, prompt=prompt, max_tokens=tokens))['choices'][0]['text']


def question():
    question1 = str(input(f"Please ask a question:\n-"))
    question = 'Q: ' + question1 + '\nA:'

    answer = openai.Completion.create(
        engine="davinci",
        prompt=question,
        temperature=Settings.temp,
        max_tokens=Settings.tok,
        top_p=1,
        best_of=Settings.best,
        frequency_penalty=Settings.freq_pen,
        presence_penalty=Settings.pres_pen,
        stop=['\n', 'Q: ']
    )
    return question1, answer['choices'][0]['text']


def grammar():
    prompt1 = str(input('Please type in the sentence you want corrected:\n-'))

    answer = openai.Completion.create(
        engine="davinci",
        prompt=f"Original: {prompt1}\nStandard American English:",
        temperature=Settings.temp,
        max_tokens=Settings.tok,
        top_p=1,
        best_of=Settings.best,
        frequency_penalty=Settings.freq_pen,
        presence_penalty=Settings.pres_pen,
        stop=["\n"]
    )

    return prompt1, answer['choices'][0]['text']


def chat(mood):
    sent = str(input('Me: '))
    if sent == 'Goodbye!':
        response = openai.Completion.create(
            engine="davinci",
            prompt=f'AI is {mood}. Human: {sent}\nAI:',
            temperature=Settings.temp,
            max_tokens=Settings.tok,
            top_p=1,
            best_of=Settings.best,
            frequency_penalty=Settings.freq_pen,
            presence_penalty=Settings.pres_pen,
            stop=["\n", " Human:", " AI:"]
        )
        print(f"AI:{response['choices'][0]['text']}")
        print('')
        os.system("pause")
        main()
    elif sent[:15] == 'Change mood to ':
        mood = sent[15:]
        print(f'Mood changed to {mood}', end='\r')
        print('\n', end='\r')
        chat(mood)
    else:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f'AI is {mood}. Human: {sent}\nAI:',
            temperature=Settings.temp,
            max_tokens=Settings.tok,
            top_p=1,
            best_of=Settings.best,
            frequency_penalty=Settings.freq_pen,
            presence_penalty=Settings.pres_pen,
            stop=["\n", " Human:", " AI:"]
        )
        print(f"AI:{response['choices'][0]['text']}")
        chat(mood)


def translate():
    os.system('cls')
    in_lang = str(input("What language to translate from?\n-"))
    os.system('cls')
    out_lang = str(input("What language to translate to?\n-"))
    os.system('cls')
    inp = str(input("Type in the sentence you want to translate.\n-"))
    answers = openai.Completion.create(
        engine="davinci",
        prompt=f"Translate the Original sentence from {in_lang} to {out_lang}\nOriginal: {inp}\nTranslated:",
        temperature=Settings.temp,
        max_tokens=Settings.tok,
        top_p=1,
        best_of=Settings.best,
        frequency_penalty=Settings.freq_pen,
        presence_penalty=Settings.pres_pen,
        stop=["\n"]
    )
    return in_lang, out_lang, inp, answers['choices'][0]['text']


def versitile():
    inp = str(input('You can write anything for the bot to do! Be free!\n-'))
    response = openai.Completion.create(
        engine="davinci",
        prompt=inp,
        temperature=Settings.temp,
        max_tokens=Settings.tok,
        top_p=1,
        best_of=Settings.best,
        frequency_penalty=Settings.freq_pen,
        presence_penalty=Settings.pres_pen,
    )
    return inp, response['choices'][0]['text']


def main():
    # TODO Test out the repeat function after sorting out the function calls in answers[]
    # def repeat(func):
    #     q = [
    #         {
    #             'type': 'confirm',
    #             'message': 'Try again?',
    #             'name': 'again',
    #             'default': True,
    #         }
    #     ]
    #     answer = prompt(q)
    #     if answer['again']:
    #         os.system('cls')
    #         func()

    os.system('cls')
    questions = [
        {
            'type': 'list',
            'name': 'activity',
            'message': 'What would you like to do?',
            'choices': [
                'Complete a prompt',
                'Q&A',
                'Correct grammar',
                'Chat',
                'Translate',
                'Versitile\n',
                'Exit',
            ]
        }]

    answers = prompt(questions)
    # TODO Replace these with code from here: https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
    if answers['activity'] == 'Complete a prompt':
        a, b = completion()
        os.system('cls')
        if b[:1] == ' ':
            print(f'{a}{b}')
        else:
            print(f'{a} {b}')
        print('')
        os.system("pause")
        main()
    elif answers['activity'] == 'Q&A':
        a, b = question()
        os.system('cls')
        print(f'Q: {a}\nA: {b[1:]}')
        print('')
        os.system("pause")
        main()
    elif answers['activity'] == 'Correct grammar':
        a, b = grammar()
        os.system('cls')
        print(f'Original: {a}\nCorrected: {b[1:]}')
        print('')
        os.system("pause")
        main()
    elif answers['activity'] == 'Translate':
        a, b, c, d = translate()
        os.system('cls')
        print(f"Translated from {a} to {b}\n"
              f"Original: {c}\n"
              f"Translated: {d}")
        print('')
        os.system("pause")
        main()
    elif answers['activity'] == 'Versitile\n':
        a, b = versitile()
        os.system('cls')
        print(f'{a}\n{b}')
        print('')
        os.system("pause")
        main()
    elif answers['activity'] == 'Chat':
        os.system('cls')
        mood = str(input("What would you like the AI's mood to be?\n-"))
        os.system('cls')
        print(f'Say something to me! Say "Goodbye!" if you want to finish talking to me or "Change mood to [mood]" to change the mood.\nCurrently the AI is {mood}.\n')
        chat(mood)
    elif answers['activity'] == 'Exit':
        print('\nGoodbye!\n')
        os.system("pause")
        os.system('cls')
        exit()
print('')
main()
