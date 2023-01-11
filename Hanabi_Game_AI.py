import random


# 270201029 Muhammed Efe İncir

# The most important place of the bot in the game is to offer us the best possibilities.Firstly, tip given to us,
# it tells us the number or color that is most frequently in our deck.I did not consider the job here as "just" giving a
# tip according to the card to be put on the stack. Because the tip given also helps with the cards to be deleted.
# For this reason, I directed bot's intelligence to the cards it would discard.
# Because removing a card that will be needed from his hand may reflect very badly on the possibilities in the process
# of the game. To complete it with high score, the bot and the player must leave the best cards in their hands.

# For this reason, my priorities for eliminating cards in the pick_discard section can be counted as follows:
# 1) If the card is already on the stack
# 2) If bot has two of the same card in it deck (the number and color must be known)
# 3) If the number of card has already passed on either side of the stack
# 4) If only the color is known and the stack containing that color is already full
# 5) If there is no information about the card
# 6) If there is just color known about the card
# 7) If there is just number known about the card

# The goal of the discard sequence I'm doing is to protect the potentially useful card as much as possible.
class Gamebot:

    def __init__(self, play_hand, stack):
        self.play_hand = play_hand  # a reference to the player's hand
        self.stack = stack  # a reference to the stack
        self.count_deck = [['b', 1], ['b', 1], ['b', 1], ['b', 2],  # a list to count the remaining
                           ['b', 2], ['b', 3], ['b', 3], ['b', 4],  # cards in the deck
                           ['w', 1], ['w', 1], ['w', 1], ['w', 2],
                           ['w', 2], ['w', 3], ['w', 3], ['w', 4]]
        for card in play_hand:  # bot has already seen the player's hand,so it knows
            self.update_count_deck(card)  # that those cards are not in the deck anymore.
        self.hand = [['!', -1], ['!', -1], ['!', -1]]  # bot's hand. '!' indicates unknown color,
        # -1 indicates unknown value

    def get_tip(self, tip: str):
        """ input: tip: a string entered by the player in the form of 'loc1,loc2*,loc3*,tip'
        where * indicates optionality and tip is either a value or a color. e.g. '1,2,w' or '2,3' or '1,2,3,2'
        output: none
        The tip is processed and the information about the bot's hand is updated."""
        tipLocations = tip.split(",")  # Splited the entered tip by comma
        info = tipLocations[-1]  # Splited the information part(end) of the tip
        tipLocations.pop(-1)  # Separated information from locations

        if info.lower() == "w" or info.lower() == "b":  # When color information is entered
            for locations in tipLocations:  # Computer deck updated
                self.hand[int(locations) - 1][0] = info  # The information was added to the given locations
        else:  # When number information is entered
            for locations in tipLocations:  # Computer deck updated
                self.hand[int(locations) - 1][1] = int(info)  # The information was added to the given locations

    def update_count_deck(self, card):
        """input: card to be removed
        output: none
        Card is removed from the count_deck of the bot."""
        if len(self.count_deck) > 0:  # We check if there are cards in the deck
            self.count_deck.remove(card)  # We delete the card entered and update the list

    def update_hand(self, num):
        """input: num: location of the card to be removed from the bot's hand
        output: none
        A card is removed from the bot's hand according to the given input and a new one is appended."""
        # Since the entered num is location, it subtracts 1 for the value of num.
        self.hand.pop(int(num) - 1)  # The card in the entered location is deleted
        # If there are 3 cards in the deck, those cards are the cards that were given to us at the beginning
        # But were not deleted.
        fixAppend = ["!", -1]  # The card template to be attached to the hand of the computer
        if len(self.count_deck) > 3:  # Checking if there are enough cards in the deck to add
            self.hand.append(fixAppend)  # The determined template card is added to the hand

    def give_tip(self):
        """input: none
        output: a string created by the bot in the form of 'loc1,loc2*,loc3*,tip'
        where * indicates optionality and tip is either a value or a color. e.g. '1,2,w' or '2,3' or '1,2,3,2'
        The bot checks the player's hand and finds a good tip to give. Minimal requirement for this function is that bot
        gives the tip for maximum possible number of cards."""
        # The bot tries to find the most "frequently" used content in the player's hands in order to give the best tip.
        # For this reason, it counts them all separately.
        count1 = [0, "count1"]  # List containing the number of 1s in hand
        count2 = [0, "count2"]  # List containing the number of 2s in hand
        count3 = [0, "count3"]  # List containing the number of 3s in hand
        count4 = [0, "count4"]  # List containing the number of 4s in hand
        countw = [0, "countw"]  # List containing the number of w's in hand
        countb = [0, "countb"]  # List containing the number of b's in hand
        for deckList in self.play_hand:  # Looking through the cards in hand
            # Since the number on a card has an index of 1, it is looking for a match there
            # If it gets a match, it increases the index 0 in the relevant list by 1
            if deckList[1] == 1:
                count1[0] += 1
            elif deckList[1] == 2:
                count2[0] += 1
            elif deckList[1] == 3:
                count3[0] += 1
            elif deckList[1] == 4:
                count4[0] += 1

            # Looking at the color for the same card
            # Since the color on a card has an index of 0, it is looking for a match there
            # If it gets a match, it increases the index 0 in the relevant list by 1
            if deckList[0] == "w":
                countw[0] += 1
            elif deckList[0] == "b":
                countb[0] += 1

        def sortedKey(list: list):  # To arrange that the "Sorted" function sorts by looking at the 0 index
            return list[0]  # For this reason, we return to the 0th index.

        # Listed containing the names and numbers of the frequent values as mostFrequent.
        mostFrequent = sorted([count1, count2, count3, count4, countw, countb], key=sortedKey)
        tipIndex = []  # List to keep indexes of the tip to return to

        # Check if the hint, the first element of mostFrequent list, is related to the number value or color
        if str(mostFrequent[-1][1])[-1].isdigit():  # Action if number
            for cards in self.play_hand:  # Looks at the indexes of the user's hand for the tip it will provide.
                if cards[1] == int(str(mostFrequent[-1][1])[-1]):  # The numbers are in the 1st index, looking for the match there
                    indexes = list(self.play_hand).index(cards)  # Finds its index when there is a match
                    tipIndex.append(indexes)  # Adds index value to tipIndex list

        else:  # Action if color (w,b)
            for cards in self.play_hand:  # Looks at the indexes of the user's hand for the tip it will provide.
                if cards[0] == (str(mostFrequent[-1][1])[-1]):  # The colors are in the 0st index, looking for the match there
                    indexes = list(self.play_hand).index(cards)  # Finds its index when there is a match
                    tipIndex.append(indexes)  # Adds index value to tipIndex list

        string = ""  # The string to which it will return
        for i in tipIndex:  # Adds the locations values to the string sequentially
            string += str(i + 1) + ","
        string += str(mostFrequent[-1][1])[-1]  # Adds what the clue is about at the end of the string
        return string  # Returns the string which is the tip

    def pick_stack(self):
        """input: none
        output: If possible, the location of the card to be placed in the stack, otherwise -1.
        Minimal the requirement for this function is to find the card to be stacked with 100% certainty."""
        # If the card we chose is the first card to be placed and the part of the stack belonging to that card's color is
        # blank, it adds the card to the stack. The first two conditions(if,elif) checks this
        if len(self.stack[0]) == 0 and (["b", 1] in self.hand):
            return self.hand.index(["b", 1]) + 1  # Returning the location of the card in hand
        elif len(self.stack[1]) == 0 and (["w", 1] in self.hand):
            return self.hand.index(["w", 1]) + 1  # Returning the location of the card in hand

        # First it checks if there is at least one card in the stack.
        # Looks at the two parts(b,w) of the stack separately.(first elif checks stack[0] ,second elif checks stack[1])
        # Second Checks if there is a card containing 1 more than the number value in the 1st index of the last card in the stack and the color of it
        # If both condition is true, then it returns the card's location in the hand
        elif len(self.stack[0]) != 0 and ([str(self.stack[0][-1][0]), int(self.stack[0][-1][1]) + 1] in self.hand):
            return int(self.hand.index([self.stack[0][-1][0], int(self.stack[0][-1][1]) + 1])) + 1
        elif len(self.stack[1]) != 0 and ([self.stack[1][-1][0], self.stack[1][-1][1] + 1] in self.hand):
            return self.hand.index([self.stack[1][-1][0], int(self.stack[1][-1][1]) + 1]) + 1
        else:  # If it can't find a card to place it returns -1
            return -1

    def pick_discard(self):
        """input: none
        output: The location of the card to be discarded. Minimal requirement for this function is that,
        If possible, the bot picks the card that is already in the stack.
        If this is not the case, the bot picks the card of which it has minimum information."""

        if len(self.hand) == 1: # If there is a card left, that card is returned directly to save time from transactions
            return 1

        for card in self.hand:  # Looking through the list of cards in order to select the card
            if card in self.stack[0] or card in self.stack[1]:
                # If the card is already on the stack it chooses it
                return self.hand.index(card) + 1  # Returns the current location of the selected card

        for card in self.hand:  # If bot has two of the same card in it deck (the number and color must be known)
            if card[0] != "!" and card[1] != int(-1):  # If the card is completely unknown, it doesn't evaluate it
                if self.hand.count(card) > 1:
                    return self.hand.index(card) + 1  # Returns the current location of the selected card

        for card in self.hand:  # If the number of card has already passed on either side of the stack
            if card[0] == "!" and card[1] != int(-1):  # The color is not determined, but the number is certain
                cardNumber = card[1]
                if len(stack[0]) > 0 and len(stack[1]) > 0:  # For this possibility there must be cards on both sides
                    if cardNumber < self.stack[0][-1][1] and cardNumber < self.stack[1][-1][1]:
                        return self.hand.index(card) + 1  # Returns the current location of the selected card

        for card in self.hand:  # If only the color is known and the stack containing that color is already full
            if card[0] == "b" and card[1] == int(-1):  # The color is black, but the number is not determined
                if len(self.stack[0]) == 4:  # For this possibility there must be full stack on black side
                    return self.hand.index(card) + 1  # Returns the current location of the selected card

            elif card[0] == "w" and card[1] == int(-1):  # The color is white, but the number is not determined
                if len(self.stack[1]) == 4:  # For this possibility there must be full stack on white side
                    return self.hand.index(card) + 1  # Returns the current location of the selected card

        for card in self.hand:  # Looking through the list of cards in order to select the card
            if card[0] == "!" and card[1] == int(-1):  # If there is no information about the card
                return self.hand.index(card) + 1  # Returns the current location of the selected card

        # If there is just color or number information about the card, it eliminates the color containing one.
        # Because color is a more general feature than its number value.
        for card in self.hand:  # Looking through the list of cards in order to select the card
            if card[0] == "!":  # Color is more general(index of color is card's 0th index)
                return self.hand.index(card) + 1  # Returns the current location of the selected card
            elif card[1] == -1:  # (index of number is card's 1th index)
                return self.hand.index(card) + 1  # Returns the current location of the selected card

        # If none of these conditions are met, all the contents of all cards must be known.
        # And none of them can be put on the stack. In this case, it can be returned randomly
        return self.hand.index(random.choice(self.hand)) + 1


def shuffle(deck):
    """input: deck to be shuffled
    output: none
    Shuffle the deck. You are free to choose the algorithm you want."""
    # We are creating a new list that will keep randomly selected cards from the deck.
    # And we make assignments with the algorithm that explained on the "for" loop.
    # At the end it returns the shuffled list as output.
    shuffledDeck = []  # New list which keep the cards which chosen in for loop
    for times in range(len(deck)):  # Process as many as the number of elements in the given list
        cardIndex = random.randint(0, len(deck) - 1)  # Chooses the location to get a card from a random location
        shuffledDeck.append(deck[cardIndex])  # Appends the selected card to the shuffledDeck list
        deck.pop(cardIndex)  # Removes added card from selected list
    deck[0:-1] = shuffledDeck


def print_menu():
    # Print operations which contains the options
    print("Hit 'v' to view the status of the game.")
    print("Hit 't' to spend a tip.")
    print("Hit 's' to try and stack your card.")
    print("Hit 'd' to discard your card and earn a tip.")
    print("Hit 'h' to view this menu.")
    print("Hit 'q' to quit.")


def update_hand(hand: list, deck: list, num: int):
    """input: hand to be updated,current deck and the location of the card to be removed
    output: removed card
    This function is called when a card is played (either stacked or discarded). It removes the played card from the hand.
    If there are any cards left in the deck, the top card in the deck is drawn and appended to the hand."""
    # Since the num value is the location, we subtracted 1 from num to select and delete the correct card from the list.
    removedCard = hand.pop(num - 1)  # It assigned discarded card as removedCard
    if len(deck) > 0:  # If there is a card in the deck, the updated hand adds a card
        hand.append(deck[0])  # Picks and appends the top card
        deck.pop(0)  # It pulls that card out of the deck
    return removedCard  # Removed card is returned


def try_stack(card, stack, trash: list, lives):
    """input: the card to be stacked, current stack, current trash, number of lives
    output: updated number of lives
    This function tries to place the card in the stack. If successful, the card is appropriately added to the stack and
    the updated stack is printed. Otherwise, the card is appended to the trash, the trash is sorted for better viewing
    and number of lives is decreased by 1. A warning and the current number of lives are printed."""
    if card[0] == "b":  # If the card is black
        if len(stack[0]) == 0 and card[1] == 1:  # If the black part of the stack is empty and the card is number 1
            stack[0].append(card)  # It adds the card to stack
            print(stack)  # It prints the current stack
        elif len(stack[0]) != 0 and int(stack[0][-1][1]) + 1 == card[1]:  # If the black part of the stack is not empty
            # And If the selected card contains more than 1 number on the last card of the stack
            stack[0].append(card)  # It adds the card to stack
            print(stack)  # It prints the current stack
        else:  # If the selected card is not suitable for the stack
            trash.append(card)  # It adds the card to trash
            trash.sort()  # It sorts the trash for better view
            lives -= 1  # Decreased health by 1
            print("Card is not suitable for stack , you lose live")  # The warning message
            print(f"Lives: {lives}")  # Printing current lives
    else:  # If the card is white
        if len(stack[1]) == 0 and card[1] == 1:  # If the white part of the stack is empty and the card is number 1
            stack[1].append(card)  # It adds the card to stack
            print(stack)  # It prints the current stack
        elif len(stack[1]) != 0 and int(stack[1][-1][1]) + 1 == card[1]:  # If the white part of the stack is not empty
            # And If the selected card contains more than 1 number on the last card of the stack
            stack[1].append(card)  # It adds the card to stack
            print(stack)  # It prints the current stack
        else:  # If the selected card is not suitable for the stack
            trash.append(card)  # It adds the card to trash
            trash.sort()  # It sorts the trash for better view
            lives -= 1  # Decreased health by 1
            print("Card is not suitable for stack , you lose live")  # The warning message
            print(f"Lives: {lives}")  # Printing current lives
    return lives  # It returned the current value of lives


def discard(card, trash: list, tips):
    """input: the card to be discarded, the current trash, number of tips
    output: updated number of tips
    This function appends the card to the trash, re-sorts it and increases the number of tips by 1.
    The updated trash and the number of tips are printed."""
    trash.append(card)  # It adds the card to trash
    trash.sort()  # Sorts the trash for better view
    tips += 1  # Tip number increased by 1
    print(f"Trash: {trash}")  # The current thrash is printed.
    print(f"Tips: {tips}")  # The number of tips are printed.
    return tips  # Returned current numbers of tip

# ----------------------------------------------------MAIN GAME---------------------------------------------------------
print("Welcome! Let's play!")
print_menu()
deck = [['b', 1], ['b', 1], ['b', 1], ['b', 2], ['b', 2], ['b', 3], ['b', 3], ['b', 4],
        ['w', 1], ['w', 1], ['w', 1], ['w', 2], ['w', 2], ['w', 3], ['w', 3], ['w', 4]]
stack = [[], []]  # 0 means black, 1 means white
trash = []
lives = 2
tips = 3
shuffle(deck)  # Deck shuffled
# First hands are dealt.
comp_hand = deck[0:3]  # TODO: obtain cards (3 cards) from deck
play_hand = deck[3:6]  # TODO: obtain cards (3 cards) from deckbg
del deck[0:6]
bot = Gamebot(play_hand, stack)  # Gamebot object is created.
turn = 0  # 0 means player, 1 means computer. So for each game, the player starts.
while True:
    if turn == 0:  # If it's the player's turn
        inp = input("Your turn:")  # Player's move received
        if inp == 'v':  # view the status of the game
            print("Computer's hand:", comp_hand)
            print("Number of tips left:", tips)
            print("Number of lives left:", lives)
            print("Current stack:")
            print("Black:", stack[0])
            print("White:", stack[1])
            print("Current trash:", trash)
        elif inp == "t":  # Spend a tip
            if tips > 0:  # Checked whether there is a available tip
                # Take a tip from the player, give it to the bot, update and print the number of tips.
                userTip = input("Tip: ")  # Player tip receive
                bot.get_tip(userTip)  # Tip was given to bot
                tips -= 1  # The number of tips has been reduced by 1
                print(f"{tips} tips left")  # Printing current tip numbers
                turn = 1  # Switched the turn to bot
            else:
                print("Not possible! No tips left!")
        elif inp == "s":  # try and stack your card.
            # Take the location of the card to be stacked from the player,
            # update hands and bot's count_deck and try to stack the selected card.
            if len(play_hand) > 0:  # Player must have card for the stack
                cardLocation = input("Location: ")  # Card location is taken from the player
                cardOnHand = play_hand[int(cardLocation) - 1]  # The card in the specified location is assigned to the variable
                if len(deck) > 0:  # If there are card on deck
                    bot.update_count_deck(deck[0])  # Bot updated count_deck
                update_hand(play_hand, deck, int(cardLocation))  # Player hand is updated
                lives = try_stack(cardOnHand, stack, trash, lives)  # Tested for stack fit
            else:
                print("You do not have card to play")
            turn = 1  # Switched the turn to bot
        elif inp == "d":  # Discard your card and earn a tip.
            # Take the location of the card to be discarded from the player,
            # update hands and bot's count_deck and discard the selected card.
            if len(play_hand) > 0:  # Player must have card for the discard
                discardLocation = input("Location: ")  # Card location is taken from the player
                discardedCard = play_hand[int(discardLocation) - 1]  # The card in the specified location is assigned to the variable
                if len(deck) > 0:  # If there are card on deck
                    bot.update_count_deck(deck[0])  # Bot updated count_deck
                update_hand(play_hand, deck, int(discardLocation))  # Player hand is updated
                tips = discard(discardedCard, trash, tips)   # Tips is updated
            else:
                print("You do not have card to play")
            turn = 1  # Switched the turn to bot
        elif inp == "h":  # view this menu."
            print_menu()
        elif inp == "q":  # quit.
            break
        else:
            print("Please enter a valid choice (v,t,s,d,h,q)!")
    else:
        # If it's the bot's turn
        # A minimal strategy of the bot is given.
        if tips > 1 and len(play_hand) > 0:  # If the player has a card and the number of tip is greater than 1
            # Take a tip from the bot. Update the number of tips. Print both
            # the given tip by the bot and the updated number of tips.
            print(f"Bot's tip: {bot.give_tip()}")  # Tip generated by the bot has been printed
            print(f"{tips} tips left.")  # The current number of tips printed
        else:
            if len(comp_hand) != 0:
                # Check if bot can pick a card to stack.
                # If yes, update comp_hand, bot's hand and bot's count_deck and try to stack the selected card.
                # If no (ELSE) , make bot pick a card to discard.
                # Update comp_hand, bot's hand and bot's count_deck and discard the selected card.
                if bot.pick_stack() != -1:  # If the bot has a card suitable for Stack
                    index = bot.pick_stack() - 1  # Bot pick a card to stack. Decreased 1 for the index because the location is returning
                    cardOnHand = comp_hand[index]   # The card in the specified index is assigned to the variable
                    bot.update_hand(index + 1)  # Bot's hand updated
                    if len(deck) > 0:  # If there are cards in the deck
                        bot.update_count_deck(deck[0])  # Updated the bot deck
                    update_hand(comp_hand, deck, index + 1)  # Computer hand updated
                    lives = try_stack(cardOnHand, stack, trash, lives)   # Lives is updated
                else:  # If the bot has not a card suitable for Stack
                    index = bot.pick_discard() - 1  # Bot pick a card to discard. Decreased 1 for the index because the location is returning
                    cardOnHand = comp_hand[index]  # The card in the specified index is assigned to the variable
                    bot.update_hand(index + 1)  # Bot's hand updated
                    if len(deck) > 0:  # If there are cards in the deck
                        bot.update_count_deck(deck[0])  # Updated the bot deck
                    update_hand(comp_hand, deck, index + 1)  # Computer hand updated
                    tips = discard(cardOnHand, trash, tips)  # Tips number updated
            else:
                print("Bot has not got card to play")
        turn = 0  # Switch turns.
    score = sum([len(d) for d in stack])
    if lives == 0:
        print("No lives left! Game over!")
        print(f"Your score is", score)
        break
    if len(comp_hand + play_hand) == 0:
        print("No cards left! Game over!")
        print("Your score is", score)
        break
    if score == 8:
        print("Congratulations! You have reached the maximum score!")
        break
