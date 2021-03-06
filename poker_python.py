# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 23:19:46 2018

@author: Ragini
"""

import string
import math
import random

#The first class defined, the Card class. 
#Each object from the card class will have 2 attributes tied to it: a Suit type and a Rank (2-A). 
#The Suit ranking follow through as Spades with the highest and Clubs the lowest. 
class Card (object):
  RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

  SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
  
  def __init__ (self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __str__ (self):
    if self.rank == 14:
      rank = 'A'
    elif self.rank == 13:
      rank = 'K'
    elif self.rank == 12:
      rank = 'Q'
    elif self.rank == 11:
      rank = 'J'
    else:
      rank = self.rank
    return str(rank) + self.suit

  def __eq__ (self, other):
    return (self.rank == other.rank)

  def __ne__ (self, other):
    return (self.rank != other.rank)

  def __lt__ (self, other):
    return (self.rank < other.rank)

  def __le__ (self, other):
    return (self.rank <= other.rank)

  def __gt__ (self, other):
    return (self.rank > other.rank)

  def __ge__ (self, other):
    return (self.rank >= other.rank)
   

class Deck (object):
  #This is a initialisation of a deck. For each suit, all 13 characters of the numbers are created and added to an empty list.   
  def __init__ (self):
    self.deck = []
    for suit in Card.SUITS:
      for rank in Card.RANKS:
        card = Card (rank, suit)
        self.deck.append(card)
  
  #using a random shuffle method to shuffle up the deck
  def shuffle (self):
    random.shuffle (self.deck)

  #This can help return the number of remaining cards on the dealers side
  def __len__ (self):
    return len (self.deck)

  #deal is a method to issue cards to the other players. Pop(0) helps remove the first card from the deck list and issue it to the players.
  def deal (self):
    if len(self) == 0:
      return None
    else:
      return self.deck.pop(0)

class Poker (object):
  def __init__ (self, numHands):
    self.deck = Deck()
    self.deck.shuffle ()
    self.hands = []
    self.ptlist=[]       #create a list to store total_point
    numCards_in_Hand = 5
    
    #Dealing 5 cards to one person and popping them off the deck list
    for i in range (numHands):
      hand = []
      for j in range (numCards_in_Hand):
        hand.append (self.deck.deal())
      self.hands.append (hand)
  
  #Sort the cards with the highest rank on the left and the lowest on the right
  def organize (self):
    for i in range (len (self.hands) ):
      sortedHand = sorted (self.hands[i], reverse = True)
      hand = ''
      for card in sortedHand:
        hand = hand + str(card) + ' '
      print ('Hand ' + str(i + 1) + ': ' + hand)

  def point(self,hand):                         #point()function to calculate partial score
    sortedHand=sorted(hand,reverse=True)
    c_sum=0
    ranklist=[]
    for card in sortedHand:
      ranklist.append(card.rank)
    c_sum=ranklist[0]*13**4+ranklist[1]*13**3+ranklist[2]*13**2+ranklist[3]*13+ranklist[4]
    return c_sum

  #Method for the top combo: Royal Flush    
  def isRoyalFlush (self, hand):               #returns the total_point and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=10
    Cursuit=sortedHand[0].suit
    Currank=14
    total_point=h*13**5+self.point(sortedHand)
    for card in sortedHand:
      if card.suit!=Cursuit or card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
        print('Royal Flush')
        self.ptlist.append(total_point)    
    else:
      self.isStraightFlush(sortedHand)
    
  #Method for the second combo: Straight Flush
  def isStraightFlush (self, hand):       #returns the total_point and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=9
    Cursuit=sortedHand[0].suit
    Currank=sortedHand[0].rank
    total_point=h*13**5+self.point(sortedHand)
    for card in sortedHand:
      if card.suit!=Cursuit or card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
      print ('Straight Flush')
      self.ptlist.append(total_point)
    else:
      self.isFourOfaKind(sortedHand)

  #Method for the thrid combo: Four of a kind
  def isFourOfaKind (self, hand):                  #returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=8
    Currank=sortedHand[1].rank               #since it has 4 identical ranks,the 2nd one in the sorted list must be the identical rank
    count=0
    total_point=h*13**5+self.point(sortedHand)
    for card in sortedHand:
      if card.rank==Currank:
        count+=1
    if not count<4:
      flag=True
      print('Four of a Kind')
      self.ptlist.append(total_point)

    else:
      self.isFullHouse(sortedHand)
  
  #method for fourth combo: Full house
  def isFullHouse (self, hand):                     #returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=7
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                 #create a list to store ranks
    for card in sortedHand:
      mylist.append(card.rank)
    rank1=sortedHand[0].rank                  #The 1st rank and the last rank should be different in a sorted list
    rank2=sortedHand[-1].rank
    num_rank1=mylist.count(rank1)
    num_rank2=mylist.count(rank2)
    if (num_rank1==2 and num_rank2==3)or (num_rank1==3 and num_rank2==2):
      flag=True
      print ('Full House')
      self.ptlist.append(total_point)
      
    else:
      flag=False
      self.isFlush(sortedHand)

  #method for Flush
  def isFlush (self, hand):                         #returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=6
    total_point=h*13**5+self.point(sortedHand)
    Cursuit=sortedHand[0].suit
    for card in sortedHand:
      if not(card.suit==Cursuit):
        flag=False
        break
    if flag:
      print ('Flush')
      self.ptlist.append(total_point)
      
    else:
      self.isStraight(sortedHand)

  #method for straight combo
  def isStraight (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=5
    total_point=h*13**5+self.point(sortedHand)
    Currank=sortedHand[0].rank                        #this should be the highest rank
    for card in sortedHand:
      if card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
      print('Straight')
      self.ptlist.append(total_point)
      
    else:
      self.isThreeOfaKind(sortedHand)
     
  #method for 3 of a kind
  def isThreeOfaKind (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=4
    total_point=h*13**5+self.point(sortedHand)
    Currank=sortedHand[2].rank                    #In a sorted rank, the middle one should have 3 counts if flag=True
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
    if mylist.count(Currank)==3:
      flag=True
      print ("Three of a Kind")
      self.ptlist.append(total_point)
      
    else:
      flag=False
      self.isTwoPairs(sortedHand)
 
  #method for 2 pairs        
  def isTwoPairs (self, hand):                           #returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=3
    total_point=h*13**5+self.point(sortedHand)
    rank1=sortedHand[1].rank                        #in a five cards sorted group, if isTwo(), the 2nd and 4th card should have another identical rank
    rank2=sortedHand[3].rank
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
    if mylist.count(rank1)==2 and mylist.count(rank2)==2:
      flag=True
      print ("Two Pair")
      self.ptlist.append(total_point)
      
    else:
      flag=False
      self.isOnePair(sortedHand)
  
  def isOnePair (self, hand):                            #returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=2
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                       #create an empty list to store ranks
    mycount=[]                                      #create an empty list to store number of count of each rank
    for card in sortedHand:
      mylist.append(card.rank)
    for each in mylist:
      count=mylist.count(each)
      mycount.append(count)
    if mycount.count(2)==2 and mycount.count(1)==3:  #There should be only 2 identical numbers and the rest are all different
      flag=True
      print ("One Pair")
      self.ptlist.append(total_point)
      
    else:
      flag=False
      self.isHighCard(sortedHand)

  def isHighCard (self, hand):                          #returns the total_point and prints out 'High Card' 
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=1
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                       #create a list to store ranks
    for card in sortedHand:
      mylist.append(card.rank)
    print ("High Card")
    self.ptlist.append(total_point)
    
def main ():
  numHands = int (input ('Enter number of hands to play: '))
  while (numHands < 2 or numHands > 6):
    numHands = int( input ('Enter number of hands to play: ') )
  game = Poker (numHands)
  game.organize()  

  print('\n')
  for i in range(numHands):
    curHand=game.hands[i]
    print ("Hand "+ str(i+1) + ": " , end="")
    game.isRoyal(curHand)

  maxpoint=max(game.ptlist)
  maxindex=game.ptlist.index(maxpoint)

  print ('\nHand %d wins'% (maxindex+1))
  
main()

