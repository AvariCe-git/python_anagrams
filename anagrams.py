import os, random, json

class anagram:

    def __init__(self, word):
        self.word = word
        self.scrambled_word = ''
        self.word_length = 0
        self.found_it = False
        
    def scramble(self):
        position_list = []
        position = 0
        scrambling = True
        
        self.word_length = len(self.word)

        for i in range(self.word_length):
            position_list.append(i)
        
        for i in range(self.word_length):
            position = random.randint(0,self.word_length-1)
            while position not in position_list:
                position = random.randint(0,self.word_length-1)
            self.scrambled_word += self.word[position]
            position_list.remove(position)

    def game(self):
        inp = ''
        counter = 0
        failed_attempts = []
        self.found_it   = False
        invalid_input   = False
        no_of_tries     = 7
        self.scramble()
        
        while not self.found_it and counter < no_of_tries:

            if len(failed_attempts) > 0:
                print (f"Failed attempts:", end = ' ')
                for i in range(len(failed_attempts)-1):
                    print(failed_attempts[i], end = ', ')
                print(failed_attempts[-1])
            print (f'Word of the day is: {self.scrambled_word}')

            inp = input(f'Give a guess      : ').lower() 

            if inp == '':
                print(f'You missclick often and with great pleasure')
                continue
            elif len(inp) != self.word_length:
                print(f'Your guess is wrong on a very fundamental level')
                continue
            elif inp in failed_attempts:
                print(f"You've guessed this already")
                continue
            elif inp == self.scrambled_word:
                print(f"That's the anagram, you idjit")
                continue
            
            for i in range(len(inp)):
                if not inp[i].isalpha():
                    print(f"Don't guess numbers")
                    invalid_input = True
                    continue
                elif inp[i] not in self.word:
                    print(f"{inp[i]} is not even in the word. What's wrong with you?")
                    invalid_input = True
                    continue

            if inp == self.word:
                self.found_it = True
            else:
                counter += 1
                failed_attempts.append(inp)
                if (no_of_tries - counter) > 1:
                    print(f'You have {no_of_tries - counter} tries remaining')
                elif (no_of_tries - counter) == 1:
                    print(f'Last try. I\'d say you can do it, but I don\'t believe so')

    def check_win(self):
        if self.found_it:
            print (f'You suck, but at least you won')
            return True
        else:
            print (f'You suck. The word was {self.word}')
            return False

def read_file():

    word_list = []
    stats     = {'wins':  0,
                'losses': 0,
                'total':  0}

    try:
        with open('wordlist.txt','r') as words_file:
            word_list = words_file.readlines()
    except IOError:
        print(f'wordlist.txt not found')
        exit()

    try:
        if os.stat('stats.txt').st_size > 0:
            print(f'Welcome back!')
            with open ('stats.txt','r') as stats_file:
                try:
                    stats = json.loads(stats_file.read())
                    p_win  = stats['wins']   * 100 / stats['total'] 
                    p_loss = stats['losses'] * 100 / stats['total'] 

                    if (stats['wins'] > stats ['total']) or (stats['losses'] > stats['total']) or (p_win + p_loss < 99.9) or (p_win + p_loss > 100.1):
                        stats['wins']   = 0
                        stats['losses'] = 0
                        stats['total'] += 1

                    print(f'You\'ve played  {stats["total"]} games')
                    print(f'You\'ve won     {stats["wins"]} games, {str(round(p_win,2))} % of the total games')
                    print(f'You\'ve lost    {stats["losses"]} games, {str(round(p_loss,2))} % of the total games')

                except:
                    print(f'Stats file is corrupted, deleting stats')
                    with open('stats.txt','w') as stats_file:
                        stats_file.write(json.dumps(stats))

    except IOError:
        print('This is your first time playing. Welcome to hell!')
    
    return word_list,stats


def play_game():

    play_game = True
    
    word_list, stats = read_file()

    while play_game:

        i =  random.randint(0, len(word_list)-1)
        wotd = anagram(word_list[i].replace('\n', ''))
        wotd.game()

        if wotd.check_win():
            stats["wins"]    += 1
        else:
            stats["losses"]  += 1
        stats['total']       += 1

        print(f'Total games: {stats["total"]}, Wins: {stats["wins"]}, Losses: {stats["losses"]}')
        print (f'Do you want to continue?')
        inp = input(f'Press y for yes, anything else to quit: ').lower()
        
        if inp != 'y':
            with open('stats.txt','w') as stats_file:
                stats_file.write(json.dumps(stats))
            play_game = False
        else:
            del wotd

play_game()