import sysv_ipc
import threading
import random
import time
import multiprocessing
from multiprocessing import Manager
import kb
import os


# MQ TYPES:[1 Demande de val][2 Reponse de validation p1][3 Reponse de validation p2][4 SHUTDOWN][5 UpdateAff topcard][6 UpdateAff P1hand][7 UpdateAff P2hand][8 UpdateAff P1Message][9 UpdateAff P2Message][10 P1 Input][11 P2 Input]


def draw(pile_mutex):
	pile_mutex.acquire()
	drawn_card = pile[0]
	pile.pop(0)
	pile_mutex.release()
	return drawn_card


def check_move(card, new_card):
	if (card[1] == new_card[1]) and (card[2] != new_card[2]):
		return True

	if (int(new_card[1]) - 1 == int(card[1])) or (int(new_card[1]) + 1 == int(card[1])) and (card[2] == new_card[2]):
		return True

	return False


def create_pile():
	new_pile = []

	while len(new_pile) < 20:

		card = str(random.randint(0, 9))
		color = random.randint(0, 1)
		if color == 0:
			card += "r"
		else:
			card += "b"

		if not (card in new_pile):
			new_pile.append(card)

	return new_pile


def board(pile_mutex):
	card = "8r"
	card = "0" + card
	first_card = card.encode()
	mq.send(first_card, type=5)

	while True:
		
		try:
			message, t = mq.receive(block=False, type=4)
		except sysv_ipc.BusyError:
			pass
		else:
			possibleshutdown = message.decode()
			if possibleshutdown[0] == "s":
				mq.send(message, type=4)
				break
				
		try:
			playermove, t = mq.receive(block=False, type=1)
		except sysv_ipc.BusyError:
			pass
		else:
			
			playermove = playermove.decode()
			
			if playermove[0] == "1":
				
				if check_move(card, playermove):
					
					card = playermove
					first_card = card.encode()
					mq.send(first_card, block=False, type=5)
					answer = ("v1" + card[1] + card[2]).encode()
					
				else:
					
					answer = "u100".encode()
				mq.send(answer, block=False, type=2)

			if playermove[0] == "2":
				
				if check_move(card, playermove):
					
					card = playermove
					first_card = card.encode()
					mq.send(first_card, block=False, type=5)
					answer = ("v2" + card[1] + card[2]).encode()
					
				else:
					answer = "u200".encode()
				mq.send(answer, block=False, type=3)
				
	time.sleep(1)
	print("BOARD WILL NOW EXIT")
	time.sleep(1)


def player(n, pile_mutex, action_mutex):
	hand = [str( 5 + n ) + "r"]
	tosend = str(hand)
	encoding = tosend.encode()
	mq.send(encoding, type=5 + n)

	while True:

		try:

			message, t = mq.receive(block=False, type=4)

		except sysv_ipc.BusyError:

			pass

		else:
			
			message = message.decode()

			if message[0] == "s":
				message.encode()
				mq.send(message, block=False, type=4)
				break

		running = [True]

		def timeout(running):
			running[0] = False

		timer = threading.Timer(10, timeout, args=(running,))
		timer.start()

		while running[0]:

			try:

				userinput, t = mq.receive(block=False, type=9 + n)

			except sysv_ipc.BusyError:

				pass

			else:
				
				c = userinput.decode()

				if n == 1:

					if c == "a":
						index = 0
						timer.cancel()
						move = ("1" + hand[index]).encode()
						action_mutex.acquire()
						mq.send(move, type=1)
						break

					if c == "z":
						index = 1
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a second card".encode(), block=False, type=7 + n)
						else:
							move = ("1" + hand[index]).encode()
							print(move)
							action_mutex.acquire()
							mq.send(move, type=1)
							break

					if c == "e":
						index = 2
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a third card".encode(), block=False, type=7 + n)
						else:
							move = ("1" + hand[index]).encode()
							action_mutex.acquire()
							mq.send(move, type=1)
							break

					if c == "r":
						index = 3
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a fourth card".encode(), block=False, type=7 + n)
						else:
							move = ("1" + hand[index]).encode()
							action_mutex.acquire()
							mq.send(move, type=1)
							break

					if c == "t":
						index = 4
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a fifth card".encode(), block=False, type=7 + n)
						else:
							move = ("1" + hand[index]).encode()
							action_mutex.acquire()
							mq.send(move, type=1)
							break

				if n == 2:

					if c == "h":
						index = 0
						timer.cancel()
						move = ("2" + hand[index]).encode()
						action_mutex.acquire()
						mq.send(move, type=1)
						break

					if c == "j":
						index = 1
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a second card".encode(), block=False, type=7 + n)
						else:
							move = ("2" + hand[index]).encode()
							action_mutex.acquire()
							mq.send(move, type=1)
							break

					if c == "k":
						index = 2
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a third card".encode(), block=False, type=7 + n)
						else:
							move = ("2" + hand[index]).encode()
							action_mutex.acquire()
							mq.send(move, type=1)
							break

					if c == "l":
						index = 3
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a fourth card".encode(), block=False, type=7 + n)
						else:
							move = ("2" + hand[index]).encode()
							action_mutex.acquire()
							mq.send(move, type=1)
							break

					if c == "m":
						index = 4
						timer.cancel()
						if len(hand) < index + 1:
							mq.send("You don't have a fifth card".encode(), block=False, type=7 + n)
						else:
							move = ("2" + hand[index]).encode()
							action_mutex.acquire()
							mq.send(move, type=1)
							break

		if not running[0]:
			
			tooslow = "Too slow. You draw a card"
			tooslow.encode()
			mq.send(tooslow, block=True, type=7 + n)
			
			if len(pile) != 0:
				
				hand.append(draw(pile_mutex))
				mq.send(str(hand).encode(), type=5 + n)
				
			if len(pile) == 0:
				
				shutdown = "s000".encode()
				mq.send(shutdown, type=4)

		else:

			while True:

				board_answer, t = mq.receive(type=1 + n)

				answer_to_check = board_answer.decode()

				if answer_to_check[0] == "v":
					
					mq.send('Right move'.encode(), type=7 + n)
					hand.pop(index)
					tosend = str(hand)
					encoding = tosend.encode()
					mq.send(encoding, type=5 + n)
					
					action_mutex.release()
					
					if len(hand) == 0:
						
						win_shutdown = ("s" + str(n) + "00").encode()
						mq.send(win_shutdown, type=4)
		
					break

				if answer_to_check[0] == "u":
					
					if len(pile) != 0:
						
						mq.send('Wrong move. You draw a card.'.encode(), type=7 + n)
						hand.append(draw(pile_mutex))
						tosend = str(hand)
						encoding = tosend.encode()
						mq.send(encoding, type=5 + n)
						
					action_mutex.release()
					pile_mutex.acquire()
					
					if len(pile) == 0:
						
						shutdown = "s000".encode()
						mq.send(shutdown, type=4)
					
					pile_mutex.release()
					
					break
					
	time.sleep(1)
	print("PLAYER " + str(n) + " WILL NOW EXIT")
	time.sleep(1)

def update_display():
	top_card = ''
	handA = []
	handB = []

	messageA = 'Welcome Player 1 ! GLHF'
	messageB = 'Welcome Player 2 ! GLHF'

	while True:

		time.sleep(2)

		try:
			message, t = mq.receive(block=False, type=4)
		except sysv_ipc.BusyError:
			pass
		else:
			possibleshutdown = message.decode()
			if possibleshutdown[0] == "s":
				os.system('clear')
				print('')
				print('		_--===[ FREAK OUT !]===--_')
				print('')
				print('')
				print('')
				print('')
				print('')
				print('##############################################################')
				print('')
				print('')
				print('')
				if possibleshutdown[1]=='0':
					print('      No one wins :(')
				else:
					print('    Player '+possibleshutdown[1]+' wins !')
				print('')
				print('')
				print('            GAME OVER')
				print('')
				print('')
				print('##############################################################')
				mq.send(message, type=4)
				break
		try:
			message, t = mq.receive(block=False, type=5)
		except sysv_ipc.BusyError:
			pass
		else:
			top_card = message.decode()
		try:
			message, t = mq.receive(block=False, type=6)
		except sysv_ipc.BusyError:
			pass
		else:
			handA = message.decode()
		try:
			message, t = mq.receive(block=False, type=7)
		except sysv_ipc.BusyError:
			pass
		else:
			handB = message.decode()
		try:
			message, t = mq.receive(block=False, type=8)
		except sysv_ipc.BusyError:
			pass
		else:
			messageA = message.decode()
		try:
			message, t = mq.receive(block=False, type=9)
		except sysv_ipc.BusyError:
			pass
		else:
			messageB = message.decode()

		###########################################################################################
		os.system('clear')
		print('')
		print('		_--===[ FREAK OUT !]===--_')
		print('')
		print('			[Board]')
		print('')
		print('			 # ' + top_card[1] + top_card[2] + ' #')
		print('')
		print('##############################################################')
		print('')
		print('')
		print(' [P1] : ' + messageA)
		print('')
		print('')
		print('')
		print(' [P2] : ' + messageB)
		print('')
		print('')
		print('##############################################################')
		print('')
		print(' [P1] [Controls : A Z E R T]')
		print(handA)
		print('')
		print(' [P2] [Controls : H J K L M]')
		print(handB)
	###########################################################################################
	time.sleep(1)
	print("DISPLAY WILL NOW EXIT")
	time.sleep(1)


key = 1

if __name__ == "__main__":
	
	os.system('clear')
	
	pile_manager = Manager()
	
	pile_mutex = pile_manager.Lock()
	
	action_manager = Manager()

	action_mutex = action_manager.Lock()

	mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

	keyboard = kb.KBHit()

	manager = Manager()

	pile = manager.list(create_pile())

	display = multiprocessing.Process(target=update_display, args=())
	board_process = multiprocessing.Process(target=board, args=(pile_mutex,))
	player_one = multiprocessing.Process(target=player, args=(1, pile_mutex,action_mutex,))
	player_two = multiprocessing.Process(target=player, args=(2, pile_mutex,action_mutex,))

	display.start()
	board_process.start()
	player_one.start()
	player_two.start()

	InputA = ["a", "z", "e", "r", "t"]

	InputB = ["h", "j", "k", "l", "m"]

	while True:

		try:

			message, t = mq.receive(block=False, type=4)
			

		except sysv_ipc.BusyError:

			pass

		else:

			possibleshutdown = message.decode()

			if possibleshutdown[0] == "s":
				mq.send(message, type=4)
				break

		if keyboard.kbhit():

			inputchar = keyboard.getch()

			try:

				if inputchar in InputA:
					char = inputchar.encode()
					mq.send(char, type=10)

				if inputchar in InputB:
					char = inputchar.encode()
					mq.send(char, type=11)

			except UnicodeDecodeError:

				pass

	display.join()
	board_process.join()
	player_one.join()
	player_two.join()
	
	time.sleep(1)
	print("MAIN WILL NOW CLOSE")
	time.sleep(1)
	
	mq.remove()