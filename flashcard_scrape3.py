import pygame
import urllib
import urllib.request
from bs4 import BeautifulSoup
import re


##################################################
#class flashcard, contains a term and a definition
#
#
##################################################
class Flashcard:

	def __init__(self,term, definition):
		self.term = term
		self.definition = definition
		#self.prev = None
		self.next = None
		#self.alt = None

	def print_card(self):
		print("front: {}\nback: {}".format(self.term, self.definition))

	def get_value(self):
		return(self.definition)

	def set_next(self, next_card):
		self.next = next_card
		next_card.next = self

#################################################
#class deck, a deck contains a set of cards 
#if duplicates are found it will try to merge them
#although this is not yet implemented
#
#################################################
class Deck:

	def __init__(self):
		self.cards = {}

	def add_card(self,card):
		if('...' not in  card.definition):	
			if card.term in self.cards:
				self.cards[card.term].alt = card.definition
				self.cards[card.term].next = card
			else:
				self.cards[card.term] = card

	def print_deck(self):
		for card in self.cards:
			print("{}:\n \t{}\n\n".format(card, self.cards[card].definition))

	def play(self):
		for card in self.cards:
			print("{}:\n".format(card))
			input("press enter for answer")
			print("\t{}\n\n".format(self.cards[card].definition))

	def get_list(self):
		ls = [self.cards[c] for c in self.cards]
		#print(ls)
		return(ls)

############################################
#method get_cards takes a url and returns a 
#list of them to be added to the deck
#
############################################
def get_cards(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	terms = [x.getText() for x in soup.find_all("span", {"class":re.compile("TermText notranslate*")})]
	deck = [Flashcard(terms[i],terms[i+1]) for i in range(0,len(terms),2)]
	return(deck)

def splitJoin(text):
	return(" ".join(text.split()[:len(text.split())//2]),
			" ".join(text.split()[len(text.split())//2:]))


prime = Deck()

urls = ["https://quizlet.com/207731231/classical-mythology-final-flash-cards/",
		"https://quizlet.com/207731231/classical-mythology-final-flash-cards/",
		"https://quizlet.com/207223543/classical-mythology-final-university-of-iowa-flash-cards/"]

for url in urls:
	d = get_cards(url)
	for c in d:
		#print(c)
		prime.add_card(c)
#prime.play()
#prime.print_deck();
print(len(prime.cards))
play_deck = prime.get_list() #returns the cards in list form
#print(play_deck)


pygame.init()
screen = pygame.display.set_mode((900, 480))
clock = pygame.time.Clock()
done = False

font = pygame.font.SysFont("comicsansms", 28)

xl = False
count = 0
text = font.render(play_deck[0].term, True, (0, 128, 0))
#btext = font.render(play_deck[0], True, (0, 128, 0))
default = (255, 255, 255)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True


        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #default = (0,0,0)
            count +=1
            text = play_deck[count].term
            if(len(text)>60):
            	xl = True
            	t = splitJoin(text)
            	text = font.render(t[0], True, (0, 128, 0))
            	btext = font.render(t[1], True, (0, 128, 0))
            else:
            	xl = False
            	text = font.render(play_deck[count].term, True, (0, 128, 0))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        	count -= 1
        	text = play_deck[count].term
        	if len(text)>60:
        		xl = True
        		t = splitJoin(text)
        		text = font.render(t[0], True, (0, 128, 0))
        		btext = font.render(t[1], True, (0, 128, 0))
        	else:
        		xl = False
        		text = font.render(text, True, (0,128,0))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        	#trying to use the linked list style implementation come back to this
        	#text = font.render(play_deck[count].next.definition, True, (0, 128, 0))
        	print(play_deck[count].definition)
        	text = play_deck[count].definition
        	if(len(text)>60):
        		xl = True
        		t = splitJoin(text)
        		text = font.render(t[0], True, (0, 128, 0))
        		btext = font.render(t[1], True, (0,128,0))
        	else:
        		xl = False
        		text = font.render(text, True, (0,128,0))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        	text = play_deck[count].term

        	if(len(text)>60):
        		xl = True
        		t = splitJoin(text)
        		text = font.render(t[0], True, (0,128,0))
        		btext = font.render(t[1], True, (0,128,0))
        	else:
        		xl = False
        		text = font.render(play_deck[count].term, True, (0,128,0))
    
    screen.fill(default)
    if(xl):
    	screen.blit(text,(450 - text.get_width() // 2, 215 - text.get_height() // 2))
    	screen.blit(btext,(450 - btext.get_width() // 2, 245 - btext.get_height() // 2))
    else:
	    screen.blit(text,
	        (450 - text.get_width() // 2, 240 - text.get_height() // 2))
	    #screen.blit(btext,
	    #    (450 - btext.get_width() // 2, 240 - btext.get_height() // 2))
    pygame.display.flip()
    clock.tick(60)

