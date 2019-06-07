from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, Base, User

engine = create_engine('sqlite:///vgcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
# Add my info
User1 = User(name="Ryan Fernandez", email="iscariot.tf@gmail.com")
session.add(User1)
session.commit()


# Menu for SNES
category1 = Category(user_id=1, name="SNES")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Base Console", description="SNES Console with one controller",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Deluxe Console",
             description="Console with two controllers and Super Mario World", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Controller",
             description="Basic SNES controller from Nintendo",
             category=category1)

session.add(item3)
session.commit()


# Menu for Genesis
category2 = Category(user_id=1, name="Genesis")

session.add(category2)
session.commit()


item1 = Item(user_id=1, name="Base Console", description="Genesis console with one controller",
             category=category2)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Deluxe Console",
             description="Genesis console with two controllers and Sonic", category=category2)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Controller", description="Basic controller from Sega",         		     category=category2)

session.add(item3)
session.commit()


# Menu for PC Engine
category1 = Category(user_id=1, name="PC Engine")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Core Grafx",
             description="Basic system with controller", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Core Grafx 2", 
             description="Same as Core Grafx but with turbo controller", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Controller",
             description="Basic controller from NEC", category=category1)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Turbo Controller", description="Controller with turbo function",
             category=category1)

session.add(item4)
session.commit()

item5 = Item(user_id=1, name="Booster", description="Allows for AV output and game saves",
             category=category1)

session.add(item4)
session.commit()

# Menu for Sony
category1 = Category(user_id=1, name="Sony Playstation")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Playstation", description="Playstation system",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Controller",
             description="Sony Playstation controller", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Memory Card",
             description="Sony branded memory card", category=category1)

session.add(item3)
session.commit()

# Menu for Microsoft
category1 = Category(user_id=1, name="Microsoft")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Xbox Console", description="Basic Xbox console",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Controller",
             description="Microsoft branded controller",
             category=category1)

session.add(item2)
session.commit()


# Menu for Atari
category1 = Category(user_id=1, name="Atari")

session.add(category1)
session.commit()

item9 = Item(user_id=1, name="Atari 2600", description="Atari 2600 Console with 2 controllers",
             category=category1)

session.add(item9)
session.commit()

item1 = Item(user_id=1, name="Joystick",
             description="Classic Atari 1 button joystick",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Pac-Man Cartridge",
             description="Literally the game that crashed the market", category=category1)

session.add(item2)
session.commit()


# Menu for Coleco
category1 = Category(user_id=1, name="Coleco")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Colecovision",
             description="Colecovision arcade console with two controllers",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="2600 Adapter",
             description="Booster to allow for play of atari games on coleco",
             category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Steering adapter",
             description="Play driving games on your coleco",
             category=category1)

session.add(item2)
session.commit()

print "added items!"
