'''
Project Name : Instabot
Created By   : ANURAG SHAKYA       [IMS ENGINEERING COLLEGE]
Submitted to : Mr. SHUBHAM JAIN    [AcadView]
             : Ms. TANVI RANGA     [AcadView]
             : Mr. RISHABH ARORA   [AcadView]
Date         : 07/02/2018
'''

import requests
import urllib
import ctypes, os
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

BASE_URL = "https://api.instagram.com/v1/"

#ACCESS_KEY = "4870715640.a48e759.874aba351e5147eca8a9d36b9688f494"                                   # Acadview Token
ACCESS_KEY = "6624879469.f736d0d.d38c462b0cd44063968e090abb4f4531"                                    # my Token, will be removed when pushed to github




# -------------------------------  function start_bot() starts here  ----------------------------------------------------------------------------------

# function name: start_bot(), it provides user a Instabot Menu where they can choose from a bunch of options like...
# fetching own post, media or post media of a particular user of Instagram

def start_bot():
    show_menu = True
    while show_menu:

        print """\n                     INSTABOT \n=========================================================       
         select an option :

             1. Get your own details  
             2. Get details of a user by username
             3. Get your own recent post
             4. Get the recent post of a user by username
             5. To like recent post
             6. To comment on recent post
             7. Delete negative comments
             8. Miscellaneous Options          ---> [ More Options] 
             9. Exit from Instabot menu
              """
        choice = raw_input()

        # to fetch own details
        if choice == '1':
            self_info()


        # to fetch details of a user by username
        elif choice == '2':
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)


        # to get own recent post
        elif choice == '3':
            get_own_post()


        # to get the recent post of a user by username
        elif choice == '4':
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)


        elif choice == '5':
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)


        elif choice == '6':
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)


        elif choice == '7':
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comments(insta_username)


        elif choice == '8':
            pass


        # code to exit from the instabot menu
        elif choice == '9':
            print "Thank you for using Instabot. \n All changes saved!\n  exiting ..."
            show_menu = False

        # if user selected an in valid option
        else:
            message_box("whoa! You've selected an invalid option\n Please try again ", "Oops", 0)


# -------------------------------  function start_bot() ends here  ------------------------------------------------------------------------------------








# -------------------------------  function message_box() starts here  --------------------------------------------------------------------------------

def message_box(text, title, style):

    return ctypes.windll.user32.MessageBoxA(0, text, title, style)

# -------------------------------  function message_box() ends here  ----------------------------------------------------------------------------------







# -------------------------------  function self_info() starts here  ----------------------------------------------------------------------------------

# function : self_info(), used to fetch self information from instagram account

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_KEY)
    print 'GET request url : %s ' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        user_name = user_info["data"]["username"]
        name = user_info["data"]["full_name"].capitalize()
        posts = user_info["data"]["counts"]["media"]
        follows = user_info["data"]["counts"]["follows"]
        following = user_info["data"]["counts"]["followed_by"]

        print "\n\033[1;30;46m", "Name : %s \n User name : %s \n Total Posts made : %d \n %s follows : %d  people \n %d people are following %s \033[m" \
                                 % (name, user_name, posts, name.partition(' ')[0], follows, following,
                                    name.partition(' ')[0])

    else:
        print 'Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!'


# -------------------------------  function self_info() ends here  ------------------------------------------------------------------------------------


# -------------------------------  function get_user_id() starts here  --------------------------------------------------------------------------------

# function name: get_user_id(), used to fetch user_id of a instagram user by passing instagram user name

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_KEY)
    print 'GET request url : %s \n looking for user Id. of %s  ...\n' % (request_url, insta_username)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!'



# -------------------------------  function get_user_id() ends here  ----------------------------------------------------------------------------------


'''
Function declaration to get the info of a user by username
'''


# -------------------------------  function get_user_info() starts here  ------------------------------------------------------------------------------

# function name : get_user_info(), used to fetch user details of a instagram user by passing instagram user name

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        return None
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_KEY)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if 'data' in user_info:
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


# -------------------------------  function get_user_info() ends here  --------------------------------------------------------------------------------


# function name: get_own_post(), used to fetch recent post of owner of access key

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_KEY)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your post has been downloaded! \n Please close your Image viewer to procceed...'
            os.system(image_name)
            return own_media["data"][0]["id"]

        else:
            print 'There is no post to show!'
    else:
        print 'Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!'
        return None


# -------------------------------  function get_own_post() ends here  ---------------------------------------------------------------------------------


# -------------------------------  function get_user_post() starts here  ------------------------------------------------------------------------------

# function name : get_user_post(), used to fetch the recent post of a instagram user by passing instagram user name

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        return None
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_KEY)
    print 'GET request url : %s' % (request_url)
    recent_user_media = requests.get(request_url).json()

    if recent_user_media['meta']['code'] == 200:
        if len(recent_user_media['data']) > 0:
            image_name = recent_user_media['data'][0]['id'] + ".jpeg"
            image_url = recent_user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)

            print "recent post of %s has been downloaded \n Please close your Image viewer to procceed..." % (
                recent_user_media["data"][0]["user"]["full_name"].capitalize())
            os.system(image_name)
            return recent_user_media["data"][0]['id']

        else:
            print "There is post to show!"
            return "no post to show"

    else:
        print 'Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!'
        return None



# -------------------------------  function get_user_post() ends here  --------------------------------------------------------------------------------






# -------------------------------  function like_a_post() starts here  --------------------------------------------------------------------------------

# function name : like_a_post(), used to like recent post of the user whose user name is passed as parameter

def like_a_post(insta_username):

	media_id = get_user_post(insta_username)
	request_url = (BASE_URL + 'media/%s/likes') % (media_id)
	payload = {"access_token": ACCESS_KEY}
	print 'POST request url : %s' % (request_url)
	post_a_like = requests.post(request_url, payload).json()

	if post_a_like['meta']['code'] == 200:
		print 'Like was successful!'
	else:
		print 'Your like was unsuccessful. Try again!'



# -------------------------------  function like_a_post() ends here  ----------------------------------------------------------------------------------





# -------------------------------  function post_a_comment() starts here  -----------------------------------------------------------------------------


# function name : post_a_comment(), used to comment on recent post of the user whose user name is passed as parameter

def post_a_comment(instausername) :

    media_id = get_user_post(instausername)
    comment_text = raw_input("Your Comment: ")
    payload = {"access_token": ACCESS_KEY, "text": comment_text}
    request_url = (BASE_URL + "media/%s/comments") %(media_id)
    print "POST request url : %s" %(request_url)
    make_comment = requests.post(request_url, payload).json()
    if make_comment["meta"]["code"] == 200:
        print "Successfully added anew comment!"
    else :
        print "Unable to load comment. Try again!"


# -------------------------------  function post_a_comment() ends here  -------------------------------------------------------------------------------



# -------------------------------  function delete_negative_comments() starts here  -------------------------------------------------------------------


def delete_negative_comments(insta_username):

    media_id = get_user_post(insta_username)

    if media_id != "no post to show" :

        request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_KEY)
        print 'GET request url : %s' % (request_url)
        comment_info = requests.get(request_url).json()

        if comment_info['meta']['code'] == 200:
            # Check if we have comments on the post
            if len(comment_info['data']) > 0:
                # And then read them one by one
                for comment in comment_info['data']:
                    comment_text = comment['text']
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                    if blob.sentiment.p_neg > blob.sentiment.p_pos:
                        comment_id = comment['id']
                        delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                            media_id, comment_id, ACCESS_KEY)
                        print 'DELETE request url : %s' % (delete_url)

                        delete_info = requests.delete(delete_url).json()

                        if delete_info['meta']['code'] == 200:
                            print 'Comment successfully deleted!'
                        else:
                            print 'Could not delete the comment'



            else:
                print 'No comments found'
        else:
            print 'Status code other than 200 received!'

    else :
        print "... and so negative comments at all.."

# -------------------------------  function delete_negative_comments() ends here  ---------------------------------------------------------------------



start_bot()