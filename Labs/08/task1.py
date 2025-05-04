#task 1 - lab 08

#probability of drawing a red card?
#there are 26 red cards (hearts + diamonds) out of total 52 cards -> 26/52 -> 1/2
total_cards = 52
red_cards = 26
print(f"probability of drawing a red card: {red_cards / total_cards:.2f}")

#probability its a heart, given its red?
#among 26 red cards, 13 are hearts -> 13/26 -> 1/2
hearts_red = 13
print(f"probability red card is a heart: {hearts_red / red_cards:.2f}")


#given its a face card (J, Q, K), probability its a diamond?
#4 suits * 3 face-ranks = 12 face-cards total
#diamonds contribute -> J, Q, K -> 3 cards
#3/12 -> 1/4
face_cards = 12
diamond_face = 3
print(f"probability face card is a diamond: {diamond_face / face_cards:.2f}")

#given its a face card, probability its a spade or a queen?
#spade face cards (J♠, Q♠, K♠) -> 3
#queen face cards (Q♣, Q♦, Q♥, Q♠) -> 4
#spade union queen = 3 + 4 -1 = 6 (-1 bec queen of spades, is in both)
#P(spade or queen | face) = 6/12 -> 1/2
spade_face = 3
queens = 4

spade_or_queen_face = spade_face + queens - 1
print(f"probability face card is spade or queen: {spade_or_queen_face / face_cards:.2f}")




