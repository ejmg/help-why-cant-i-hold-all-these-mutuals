import tweepy as ty
import time
import sys
from secret import (ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_TOKEN,
                    CONSUMER_SECRET)


def setTwitterAuth():
    """
    obtains authorization from twitter API

    auth my ass, jack
    """
    # sets the auth tokens for twitter using tweepy
    auth = ty.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth)
    return api


def handleCursorLimit(cursor):
    """
    can u handle the limit?????
    """
    while True:
        try:
            yield cursor.next()
        except ty.RateLimitError:
            print("sleeping! {}".format(time.localtime()))
            # got fucked by jack's api once again, press F please
            time.sleep(60 * 15)

def mutuals(api):
    thyself = api.me().id
    iCanCountLol = 0
    mutualists = []
    print("Your user ID number: {}".format(thyself))

    for fran in handleCursorLimit(ty.Cursor(api.friends).items()):
        print("fran: {}".format(fran.id))
        # technically speaking, this api request can still fuck us over and
        # sideways, so let us pray together very very very very hard that the
        # magic dice of the universe roll our way on this request.
        franship = api.show_friendship(source_id=thyself, target_id=fran.id)
        if franship[0].following and franship[0].followed_by:
            iCanCountLol += 1
            mutualists.append(franship[1].id)
            print("{} is a mutual!".format(franship[1].screen_name))
    print("Assuming shit is not whack and my code is not whack, you"
          " have {} mutuals".format(iCanCountLol))

    print("we will now create the list.")

    try:
        # this will create the list. if you have a list of the same name,
        # afaik, twitter makes a list with the same name, but its "slug" will
        # be the list name + digit, where digit = # duplicate

        # also lol what are api limit checks yet again
        myOwnStasi = api.create_list("mutuals")
        for muchie in mutualists:
            myOwnStasi.add_member(muchie)
    except Exception as e:
        print("wtf i make horrible code, exception while making list: {}"
              .format(e))
        sys.exit()

    print("Tada it worked or something, go check it out and see")

if __name__ == '__main__':
    api = setTwitterAuth()
    mutuals(api)
