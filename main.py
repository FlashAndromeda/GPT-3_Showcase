import os

import openai
from PyInquirer import prompt

import config

openai.api_key = config.API_KEY
openai.organization = config.ORG_KEY

class Sets:
    eng = 'text-davinci-001'    # def 'davinci'
    temp = 0.8                  # Temperature (def 0)
    tok = 100                   # No. of tokens (def 100)
    best = 3                    # Pick best out of n outputs (def 1)
    freq_pen = 0.5              # Frequency penalty (def 0.0)
    pres_pen = 0.3              # Presence penalty (def 0.0)

class Bcolors:
    HEADER = '\033[95m'     #
    BLUE = '\033[94m'       # Bot output
    CYAN = '\033[96m'       #
    GREEN = '\033[92m'      #
    YELLOW = '\033[93m'     # User input
    RED = '\033[91m'        # Errors
    END = '\033[0m'         #
    BOLD = '\033[1m'        #
    UNDERLINE = '\033[4m'   #

########################### SUB-MENUS ##################################
def generate_menu():
    clear()
    q = [
        {
            'type': 'list',
            'name': 'activity',
            'message': 'Pick a feature to try out!',
            'choices': [
                'Continue a prompt      | Continues a given prompt',
                'Short story            | Generates a very short story on a given topic\n',
                '[Return]',
            ]
        }]

    a = prompt(q)
    pick = a['activity']

    if pick == 'Continue a prompt      | Continues a given prompt':
        prompt_complete()
    elif pick == 'Short story            | Generates a very short story on a given topic\n':
        short_story()
    elif pick == '[Return]':
        main_menu()
    else:
        clear()
        print(f'{Bcolors.RED}Ya dun goofed with code!{Bcolors.END}\n')
        os.system('pause')
        main_menu()


def qna_menu():
    clear()
    q = [
        {
            'type': 'list',
            'name': 'activity',
            'message': 'Pick a feature to try out!',
            'choices': [
                'Q & A                  | Simple QnA',
                'Word meaning           | Explains the meaning of a given word\n',
                '[Return]',
            ]
        }]

    a = prompt(q)
    pick = a['activity']

    if pick == 'Q & A                  | Simple QnA':
        qna()
    elif pick == 'Word meaning           | Explains the meaning of a given word\n':
        meaning()
    elif pick == '[Return]':
        main_menu()
    else:
        clear()
        print(f'{Bcolors.RED}Ya dun goofed with code!{Bcolors.END}\n')
        os.system('pause')
        main_menu()


def trans_menu():
    clear()
    q = [
        {
            'type': 'list',
            'name': 'activity',
            'message': 'Pick a feature to try out!',
            'choices': [
                'Translate              | Translates a given sentence between given languages',
                'Correct grammar        | Corrects the grammar in a given sentence',
                'Rewrite sentence       | Rewrites the sentence according to demands',
                'Tl;dr                  | Writes a tl;dr of a given text\n',
                '[Return]',
            ]
        }]

    a = prompt(q)
    pick = a['activity']

    if pick == 'Translate              | Translates a given sentence between given languages':
        translate()
    elif pick == 'Correct grammar        | Corrects the grammar in a given sentence':
        grammar()
    elif pick == 'Rewrite sentence       | Rewrites the sentence according to demands':
        sent_rewrite()
    elif pick == 'Tl;dr                  | Writes a tl;dr of a given text\n':
        tldr()
    elif pick == '[Return]':
        main_menu()
    else:
        clear()
        print(f'{Bcolors.RED}Ya dun goofed with code!{Bcolors.END}\n')
        os.system('pause')
        main_menu()


def other_menu():

    clear()
    q = [
        {
            'type': 'list',
            'name': 'activity',
            'message': 'Pick a feature to try out!',
            'choices': [
                'Chat                   | Simple chatbot',
                'Open                   | Unmodified prompt passed straight into the API\n',
                '[Return]',
            ]
        }]

    a = prompt(q)
    pick = a['activity']

    if pick == 'Chat                   | Simple chatbot':
        mood = 'Firstlaunch'
        chat(mood)
    elif pick == 'Open                   | Unmodified prompt passed straight into the API\n':
        open_ended()
    elif pick == '[Return]':
        main_menu()
    else:
        clear()
        print(f'{Bcolors.RED}Ya dun goofed with code!{Bcolors.END}\n')
        os.system('pause')
        main_menu()


########################### MISC FUNC ##################################
def repeat(func, menu):
    q_repeat = [
        {
            'type': 'confirm',
            'message': 'Try again?',
            'name': 'again',
            'default': True,
        }
    ]
    answer = prompt(q_repeat)
    if answer['again']:
        clear()
        func()
    else:
        menu()


def clear():
    os.system('cls')


########################### GENERATE FEATURES ##########################
def prompt_complete():
    clear()
    prompt = str(input(f"Please input a prompt to complete:\n> {Bcolors.YELLOW}"))
    print(Bcolors.END, end='\r')
    try:
        clear()
        tokens = int(input("How many tokens are you willing to use?\n> "))
    except ValueError:
        print(f"{Bcolors.RED}That's not a number dumbo!{Bcolors.END}")
        print('')
        os.system("pause")
        generate_menu()

    ans = (openai.Completion.create(engine=Sets.eng, prompt=prompt, max_tokens=tokens))['choices'][0]['text']

    clear()

    if ans[:1] == ' ':
        print(f'{Bcolors.YELLOW}{prompt}{Bcolors.BLUE}{ans}{Bcolors.END}\n')
    else:
        print(f'{Bcolors.YELLOW}{prompt} {Bcolors.BLUE}{ans}{Bcolors.END}\n')
    repeat(prompt_complete, generate_menu)


def short_story():
    clear()
    top = str(input(f"I would like the story to be about: {Bcolors.YELLOW}"))
    print(Bcolors.END, end='\r')
    query = openai.Completion.create(
        engine="text-davinci-001",
        prompt=f"\n\nTopic:{top}\nStory:",
        temperature=Sets.temp,
        max_tokens=500,
        best_of=Sets.best,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen
    )
    ans = query['choices'][0]['text']
    clear()
    print(f'Topic: {Bcolors.YELLOW}{top}{Bcolors.END}\nStory:{Bcolors.BLUE}{ans}{Bcolors.END}\n')
    repeat(short_story, generate_menu)


########################### Q & A FEATURES #############################
def qna():
    clear()
    question = str(input(f"Please ask a question:\n> {Bcolors.YELLOW}"))
    print(Bcolors.END, end='\r')

    answer = openai.Completion.create(
        engine=Sets.eng,
        prompt=f'Question:{question}\nAnswer:',
        temperature=Sets.temp,
        max_tokens=Sets.tok,
        top_p=1.0,
        best_of=Sets.best,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen,
    )
    ans = answer['choices'][0]['text']
    clear()
    if '\n' in ans[:5]:
        print(f'Q: {Bcolors.YELLOW}{question}{Bcolors.END}'
              f'{Bcolors.BLUE}{ans}{Bcolors.END}\n')
    else:
        print(f'Q: {Bcolors.YELLOW}{question}{Bcolors.END}\n'
              f'{Bcolors.BLUE}{ans}{Bcolors.END}\n')
    repeat(qna, qna_menu)


def meaning():
    clear()
    inp = str(input(f"What word do you want explained?\n> {Bcolors.END}"))
    print(Bcolors.END, end='\r')
    query = openai.Completion.create(
        engine=Sets.eng,
        prompt=f'Word:Dermatology — the branch of medicine dealing with the skin. It is a speciality with both medical and surgical aspects.\n\n'
               f'Word:Discombobulate — to disconcert or confuse (someone).\n\n'
               f'Word:{inp} —',
        temperature=Sets.temp,
        max_tokens=Sets.tok,
        best_of=Sets.best,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen,
        stop=['\n']
    )
    ans = query['choices'][0]['text']
    clear()
    print(f'\n{Bcolors.YELLOW}{inp}{Bcolors.END} —{Bcolors.BLUE}{ans}{Bcolors.END}\n')
    repeat(meaning, qna_menu)


########################### TRANSFORM FEATURES #########################
def translate():
    clear()
    in_lang = str(input(f"What language to translate from?\n> {Bcolors.YELLOW}"))
    print(Bcolors.END, end='\r')
    clear()
    out_lang = str(input(f"What language to translate to?\n> {Bcolors.YELLOW}"))
    print(Bcolors.END, end='\r')
    clear()
    inp = str(input(f"Type in the sentence you want to translate.\n> {Bcolors.YELLOW}"))
    print(Bcolors.END, end='\r')
    answers = openai.Completion.create(
        engine=Sets.eng,
        prompt=f'Translate this from {in_lang} to {out_lang}:{inp}',
        temperature=0.2,
        max_tokens=Sets.tok,
        top_p=1.0,
        best_of=Sets.best,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen,
    )
    translated = answers['choices'][0]['text']
    clear()
    print(f'Translated the sentence from {Bcolors.YELLOW}{in_lang}{Bcolors.END} to {Bcolors.YELLOW}{out_lang}{Bcolors.END}!\n\n'
          f'{Bcolors.YELLOW}{inp}{Bcolors.END}'
          f'{Bcolors.BLUE}{translated}{Bcolors.END}\n')
    repeat(translate, trans_menu)


def grammar():
    clear()
    prompt1 = str(input(f'Please type in the sentence you want corrected:\n> {Bcolors.YELLOW}'))
    print(Bcolors.END, end='\r')
    answer = openai.Completion.create(
        engine=Sets.eng,
        prompt=f"Original:{prompt1}\n"
               f"Standard American English:",
        temperature=Sets.temp,
        max_tokens=Sets.tok,
        best_of=Sets.best,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen,
    )

    ans = answer['choices'][0]['text']
    clear()

    if ans == '':
        print('I am confused :(\n')
        repeat(grammar, trans_menu)
    else:
        print(f'Corrected the sentence!\n\n'
              f'{Bcolors.YELLOW}{prompt1}{Bcolors.END}'
              f'{Bcolors.BLUE}{ans}{Bcolors.END}\n')

    repeat(grammar, trans_menu)


def sent_rewrite():
    clear()
    sty = str(input(f'I want the sentence to sound: {Bcolors.YELLOW}'))
    print(f'{Bcolors.END}', end='\r')
    clear()
    inp = str(input(f'Type in the sentence you want rewritten:\n> {Bcolors.YELLOW}'))
    print(f'{Bcolors.END}', end='\r')

    answer = openai.Completion.create(
        engine=Sets.eng,
        prompt=f"The sentence '{inp} rewritten to sound {sty}: ",
        temperature=Sets.temp,
        max_tokens=Sets.tok,
        best_of=Sets.best,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen,
    )

    ans = answer['choices'][0]['text']
    clear()
    print(f"The sentence '{Bcolors.YELLOW}{inp}{Bcolors.END}' rewritten to sound {Bcolors.YELLOW}{sty}{Bcolors.END}:"
          f"{Bcolors.BLUE}{ans}{Bcolors.END}\n")
    repeat(sent_rewrite, trans_menu)


def tldr():
    clear()
    print('Paste the text you want the tl;dr for: (press Enter to start)\n')
    inp = str(input())

    query = openai.Completion.create(
        engine="davinci",
        prompt=f"The text:{inp}\n\ntl;dr of the text:",
        temperature=0.0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen,

    )
    ans = query['choices'][0]['text']
    clear()
    print(f'Here is the tl;dr:\n'
          f'{Bcolors.BLUE}{ans}{Bcolors.END}\n')

    repeat(tldr, trans_menu)


########################### OTHER FEATURES #############################
def chat(mood):
    if mood == 'Firstlaunch':
        clear()
        mood = str(input("""What would you like the AI's mood to be?\nI feel: """))
        clear()
        print(
            f'Say "Goodbye!" if you want to finish talking to me or "Change mood to [mood]" to change the mood.\n')

    sent = str(input(f'Me: {Bcolors.YELLOW}'))
    print(Bcolors.END, end='\r')

    if sent == 'Goodbye!':
        response = openai.Completion.create(
            engine=Sets.eng,
            prompt=f'AI feels {mood}.Human: {sent}\nAI:',
            temperature=Sets.temp,
            max_tokens=Sets.tok,
            top_p=1,
            best_of=Sets.best,
            frequency_penalty=Sets.freq_pen,
            presence_penalty=Sets.pres_pen,
            stop=["Human:", "AI:"]
        )
        if '\n' in response['choices'][0]['text'][:2]:
            print(f"{Bcolors.END}AI: {Bcolors.BLUE}{response['choices'][0]['text'][2:]}{Bcolors.END}")
        else:
            print(f"{Bcolors.END}AI:{Bcolors.BLUE}{response['choices'][0]['text']}{Bcolors.END}")

        print('')
        os.system("pause")
        main_menu()
    elif sent[:15] == 'Change mood to ':
        mood = sent[15:]
        print(f'Mood changed to {Bcolors.YELLOW}{mood}{Bcolors.END}', end='\r')
        print('\n', end='\r')
        chat(mood)
    else:
        response = openai.Completion.create(
            engine=Sets.eng,
            prompt=f'AI feels {mood}.Human: {sent}\nAI:',
            temperature=Sets.temp,
            max_tokens=Sets.tok,
            top_p=1,
            best_of=Sets.best,
            frequency_penalty=Sets.freq_pen,
            presence_penalty=Sets.pres_pen,
            stop=["Human:", "AI:"]
        )
        if '\n' in response['choices'][0]['text'][:2]:
            print(f"{Bcolors.END}AI: {Bcolors.BLUE}{response['choices'][0]['text'][2:]}{Bcolors.END}")
        else:
            print(f"{Bcolors.END}AI:{Bcolors.BLUE}{response['choices'][0]['text']}{Bcolors.END}")
        chat(mood)


def open_ended():
    clear()
    inp = str(input('You can write anything for the bot to do!\n> '))
    response = openai.Completion.create(
        engine=Sets.eng,
        prompt=inp,
        temperature=Sets.temp,
        max_tokens=Sets.tok,
        best_of=Sets.best,
        frequency_penalty=Sets.freq_pen,
        presence_penalty=Sets.pres_pen,
    )
    ans = response['choices'][0]['text']
    clear()
    print(f'{Bcolors.YELLOW}{inp}{Bcolors.END}\n'
          f'{Bcolors.BLUE}{ans}{Bcolors.END}\n')
    repeat(open_ended, other_menu)


########################### MAIN MENU ##################################
def main_menu():
    clear()
    questions = [
        {
            'type': 'list',
            'name': 'activity',
            'message': f'What would you like to do?',
            'choices': [
                'Generate               | Generates new things',
                'Question & Reply       | Replies to prompts',
                'Transform              | Transforms prompts',
                'Other                  | Misc features\n',
                '[Exit]',
            ]
        }]

    answers = prompt(questions)

    if answers['activity'] == 'Generate               | Generates new things':
        generate_menu()
    elif answers['activity'] == 'Question & Reply       | Replies to prompts':
        qna_menu()
    elif answers['activity'] == 'Transform              | Transforms prompts':
        trans_menu()
    elif answers['activity'] == 'Other                  | Misc features\n':
        other_menu()
    elif answers['activity'] == '[Exit]':
        clear()
        print(f'\n{Bcolors.RED}G{Bcolors.CYAN}o{Bcolors.HEADER}o{Bcolors.BLUE}d{Bcolors.YELLOW}b{Bcolors.GREEN}y{Bcolors.RED}e{Bcolors.CYAN}!{Bcolors.END}\n')
        os.system("pause")
        clear()
        exit()
clear()
print(f"""{Bcolors.CYAN}
                     _---~~(~~-_.
                   _(        )   )
                 ,   ) -~~- ( ,-' )_
                (  `-,_..`., )-- '_,)
               ( ` _)  (  -~( -_ `,  )
               (_-  _  ~_-~~~~`,  ,' )
                 `~ -^(    __;-,((()))
                       ~~~~ (_ -_(())
                              `\  )
                                ( ){Bcolors.END}\n
{Bcolors.HEADER}                  HELLO THERE USER!\n           WELCOME TO THE GPT-3 SHOWCASE!\n                       ENJOY!\n\n               Coded by FlashAndromeda\n{Bcolors.END}""")
input('              PRESS [ENTER] TO CONTINUE\n                          ')
main_menu()