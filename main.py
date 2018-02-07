'''
Project Name : Instabot
Created By   : ANURAG SHAKYA       [IMS ENGINEERING COLLEGE]
Submitted to : Mr. SHUBHAM JAIN    [AcadView]
             : Ms. TANVI RANGA     [AcadView]
             : Mr. RISHABH ARORA   [AcadView]
Date         : 07/02/2018
Description  : At the end of program
'''



import requests                                                      # to make HTTP requests simpler and handy
import urllib                                                        # fetching/downloading data by URLs using urlretrieve
import ctypes                                                        # here it is used to provide message boxes of different styles eg, 0,1,2 etc.,
import os                                                            # importing os modules for reading/ opening files [user posts/images]
from textblob import TextBlob                                        # |-\ __  to make Sentimental analysis of comments over a post
from textblob.sentiments import NaiveBayesAnalyzer                   # |-/


BASE_URL = "https://api.instagram.com/v1/"
ACCESS_KEY = "4870715640.a48e759.874aba351e5147eca8a9d36b9688f494"                              # Acadview's Access Token

# Following 2 key's will not work when the code is made public and pushed on to github.
#ACCESS_KEY = "6624879469.f736d0d.d38c462b0cd44063968e090abb4f4531"                             # my Token, anurags18
#ACCESS_KEY = "7047201851.9a7b597.2e1ca50a2d614016bd501e54d3a7c80c"                             # my Token, anurags18_test



# -------------------------------  function start_bot() starts here  ----------------------------------------------------------------------------------

# function name: start_bot(), it provides user a Instabot Menu where they can choose from a bunch of options like...
                             # fetching own post, media or post media of a particular user of Instagram

def start_bot():

    # showing instabot menu untill user himself/herself don't want to exit from instabot
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
             7. Delete negative comments on own recent post 
             8. Delete negative comments on a recent post of a user by username
             9. More Options             <----
             10. To print comments of a recent post of a user 
             11. Exit from Instabot menu
             
         \033[4;30;44m  Note: These features will be in reference with your Sandbox Users \033[0;0m
                \033[4;30;44m And the scope with which Access Token is authorized \033[0;0m
              """
        choice = raw_input()

        # to fetch own details
        if choice == "1":
            self_info()

        # to fetch details of a user by username
        elif choice == "2":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)

        # to get own recent post
        elif choice == "3":
            get_own_post()

        # to get the recent post of a user by providing username as input
        elif choice == "4":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)

        # to like recent post of a particular user of instagram by providing username as input
        elif choice == "5":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)

        # to comment on recent post of a particular user of instagram by providing username as input
        elif choice == "6":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)

        # to delete negative comments on own recent post
        elif choice == "7":
            delete_negative_comments_self()


        # to delete negative comments on recent post of any instagram user by providing username as input
        elif choice == "8":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comments_of_user(insta_username)


        # here we'll be exploring some other features of Instagram API
        elif choice == "9":
            more_options()

        # to print comments over a recent post of a user
        elif choice == "10":
            insta_username = raw_input("Enter the username of the user: ")
            fetch_user_comments(insta_username)


        # to exit from the instabot menu
        elif choice == "11":
            print "Thank you for using Instabot. \n All changes saved!\n  exiting ..."
            show_menu = False

        # if user selected an in valid option
        else:
            message_box("whoa! You've selected an invalid option\n Please try again ", "Oops", 0)


# -------------------------------  function start_bot() ends here  ------------------------------------------------------------------------------------



# -------------------------------  function message_box() starts here  --------------------------------------------------------------------------------

# function name: message_box(), used to alert, or to communicate with spy for other suggetions like invalid enties etc.,

def message_box(text, title, style):

    return ctypes.windll.user32.MessageBoxA(0, text, title, style)

# -------------------------------  function message_box() ends here  ----------------------------------------------------------------------------------



# -------------------------------  function self_info() starts here  ----------------------------------------------------------------------------------

# function : self_info(), used to fetch self information from instagram account

def self_info():

    # creating request url for accessing self[owner of Access Token] information.
    request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_KEY)
    print "GET request url : %s " % (request_url)

    # to make request and save the response in json format
    user_info = requests.get(request_url).json()

    # if request made is successfull
    if user_info["meta"]["code"] == 200:

        # extracting self details from the user_info [response saved as json]
        user_name = user_info["data"]["username"]
        name = user_info["data"]["full_name"].capitalize()
        posts = user_info["data"]["counts"]["media"]
        follows = user_info["data"]["counts"]["follows"]
        following = user_info["data"]["counts"]["followed_by"]

        print "\n\033[1;30;46m", "Name : %s \n User name : %s \n Total Posts made : %d \n %s follows : %d  people \n %d people are following %s \n\033[m" \
                                 % (name, user_name, posts, name.partition(" ")[0], follows, following,
                                    name.partition(" ")[0])
        print "\nEntering Main Menu... \n"

    # if request made is unsuccessfull
    else:
        print "Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!"

# -------------------------------  function self_info() ends here  ------------------------------------------------------------------------------------



# -------------------------------  function get_user_id() starts here  --------------------------------------------------------------------------------

# function name: get_user_id(), used to fetch user_id of a instagram user by passing instagram username

def get_user_id(insta_username):

    # creating request url for accessing user information by giving user name as a searching parameter.
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s") % (insta_username, ACCESS_KEY)
    print "GET request url : %s \n looking for user Id. of %s  ...\n" % (request_url, insta_username)

    # to make request and save the response in json format
    user_info = requests.get(request_url).json()

    # if request made is successfull
    if user_info["meta"]["code"] == 200:

        # extracting and returning the user id from the user_info [response saved as json]
        if len(user_info["data"]):
            return user_info["data"][0]["id"]

    # if request made is unsuccessfull
    else:
        print "Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!"

    return None

# -------------------------------  function get_user_id() ends here  ----------------------------------------------------------------------------------



# -------------------------------  function get_user_info() starts here  ------------------------------------------------------------------------------

# function name : get_user_info(), used to fetch user details of a instagram user by passing instagram user name

def get_user_info(insta_username):

    # fetching user id by passing username whose information is to be printed
    user_id = get_user_id(insta_username)

    # if get_user_id() returns none
    if user_id == None:
        print "User does not exist!"
        return None

    # creating request url for accessing user information by giving user_id as a parameter.
    request_url = (BASE_URL + "users/%s?access_token=%s") % (user_id, ACCESS_KEY)
    print "GET request url : %s" % (request_url)

    # to make request and save the response in json format
    user_info = requests.get(request_url).json()

    # if request made is successfull
    if user_info["meta"]["code"] == 200:

        # extracting self details from the user_info [response saved as json]
        if "data" in user_info:
            print "Username: %s" % (user_info["data"]["username"])
            print "No. of followers: %s" % (user_info["data"]["counts"]["followed_by"])
            print "No. of people you are following: %s" % (user_info["data"]["counts"]["follows"])
            print "No. of posts: %s" % (user_info["data"]["counts"]["media"])
        else:
            print "There is no data for this user!"

    # if request made is unsuccessfull
    else:
        print "Status code other than 200 received!"

# -------------------------------  function get_user_info() ends here  --------------------------------------------------------------------------------



# -------------------------------  function get_own_post() starts here  -------------------------------------------------------------------------------

# function name: get_own_post(), used to fetch recent post of owner of access key

'''
Imp. Note: some string and values are returned as this code can be reused for another funtion
'''

def get_own_post():

    # creating request url for accessing self[owner of Access Token] recent post.
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (ACCESS_KEY)
    print "GET request url : %s" % (request_url)

    # to make request and save the response in json format
    own_media = requests.get(request_url).json()

    # if request made is successfull
    if own_media["meta"]["code"] == 200:

        # if there is some post, extracting self details from the own_media[response saved as json]
        if len(own_media["data"]):
            image_name = own_media["data"][0]["id"] + ".jpeg"
            image_url = own_media["data"][0]["images"]["standard_resolution"]["url"]

            # downloading recent post named as image_name
            urllib.urlretrieve(image_url, image_name)

            # showing self recent post and returning media id
            print "Your post has been downloaded! \n Please close your Image viewer to procceed..."
            os.system(image_name)
            return own_media["data"][0]["id"]

        # if there no post at all
        else:
            print "There is no post to show!"
            return "no post to show"

    # if request made is unsuccessfull
    else:
        print "Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!"
        return "unsuccessfull request"

# -------------------------------  function get_own_post() ends here  ---------------------------------------------------------------------------------



# -------------------------------  function get_user_post() starts here  ------------------------------------------------------------------------------

# function name : get_user_post(), used to fetch the recent post of a instagram user by passing instagram user name

def get_user_post(insta_username):

    # fetching user id by passing username whose recent post is to be shown.
    user_id = get_user_id(insta_username)

    # if get_user_id() returns none
    if user_id == None:
        print "User does not exist!"
        return None

    # creating request url for accessing user recent post by giving user_id as a parameter.
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, ACCESS_KEY)
    print "GET request url [to get access media]: %s" % (request_url)

    # to make request and save the response in json format
    recent_user_media = requests.get(request_url).json()

    # if request made is successfull
    if recent_user_media["meta"]["code"] == 200:

        # if there is some post at all
        if len(recent_user_media["data"]) > 0:
            image_name = recent_user_media["data"][0]["id"] + ".jpeg"
            image_url = recent_user_media["data"][0]["images"]["standard_resolution"]["url"]

            # downloading user's recent post named as image_name
            urllib.urlretrieve(image_url, image_name)

            # showing user's recent post and returning media id
            print "recent post of %s has been downloaded \n Please close your Image viewer to procceed..." \
                  % (recent_user_media["data"][0]["user"]["full_name"].capitalize())
            os.system(image_name)
            return recent_user_media["data"][0]["id"]

        # if there is no post at all
        else:
            print "There is no post to show!"
            return "no post to show"

    # if request made is unsuccessfull
    else:
        print "Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!"
        return "unsuccessfull request"

# -------------------------------  function get_user_post() ends here  --------------------------------------------------------------------------------



# -------------------------------  function like_a_post() starts here  --------------------------------------------------------------------------------

# function name : like_a_post(), used to like recent post of the user whose user name is passed as parameter

def like_a_post(insta_username):

    # fetching media id of the recent post which is to be 'liked' by passing instagram username
    media_id = get_user_post(insta_username)

    # If get_user_post() returns no post to show then,
    if media_id == "no post to show" :
        print "So you can't make any like"


    # And if get_user_post() returns unsuccsessfull request then,
    elif media_id == "unsuccessfull request":
        print "\n please check request URL \n"

    # And if get_user_post() returns the id(ie, a string, ex: "12_23.jpeg") of recent post
    elif media_id != None :

        # creating request url for 'liking' a recent post by giving media_id as a parameter.
        request_url = (BASE_URL + "media/%s/likes") % (media_id)
        payload = {"access_token": ACCESS_KEY}
        print "POST request url [to like post]: %s" % (request_url)

        # to make request and save the response in json format
        post_a_like = requests.post(request_url, payload).json()

        # if request made is successfull
        if post_a_like["meta"]["code"] == 200:
            print "Like was successful!"

        # if request made is unsuccessfull
        else:
            print "Your like was unsuccessful. \n check for Like request_url"

    # And if get_user_post() returns None ie, type(media_id) == NoneType then,
    else:
        print "Please enter a valid Instagram username"


# -------------------------------  function like_a_post() ends here  ----------------------------------------------------------------------------------



# -------------------------------  function post_a_comment() starts here  -----------------------------------------------------------------------------


# function name : post_a_comment(), used to comment on recent post of the user whose user name is passed as parameter

def post_a_comment(insta_username) :

    # fetching media id of the recent post where user want to 'comment' by passing instagram username
    media_id = get_user_post(insta_username)

    # If get_user_post() returns no post to show then,
    if media_id == "no post to show" :
        print "So you can't make any comment"

    # And if get_user_post() returns unsuccsessfull request then,
    elif media_id == "unsuccessfull request" :
        print "\n please check request URL \n"

    # And if get_user_post() returns the id(it is a string) of recent post
    elif media_id != None :

        comment_text = raw_input("Your Comment: ")
        payload = {"access_token": ACCESS_KEY, "text": comment_text}

        # creating request url for 'commenting' a recent post by giving media_id as a parameter.
        request_url = (BASE_URL + "media/%s/comments") % (media_id)
        print "POST request url [to make comment]: %s" % (request_url)

        # to make request and save the response in json format
        make_comment = requests.post(request_url, payload).json()

        # if request made is successfull
        if make_comment["meta"]["code"] == 200:
            print "Successfully added a new comment!"

        # if request made is unsuccessfull
        else:
            print "Unable to load comment. \n check for Comment request_url"

    # And if get_user_post() returns None ie, type(media_id) == NoneType then,
    else:
        print "Please enter a valid Instagram username"


# -------------------------------  function post_a_comment() ends here  -------------------------------------------------------------------------------



# -------------------------------  function delete_negative_comments_self() starts here  --------------------------------------------------------------

# function name: delete_negative_comments_self(), to delete negative comments on own recent post after doing sentimental analysis

def delete_negative_comments_self():
    # fetching media id of own recent post to make sentimental analysis over 'comments'
    media_id = get_own_post()

    # If get_own_post() returns no post to show then,
    if media_id == "no post to show":
        print "So you can't make any sentimental analysis"

    # And if get_own_post() returns unsuccsessfull request then,
    elif media_id == "unsuccessfull request":
        print "\n please check request URL \n"

    # And if get_own_post() returns the id(it is a string) of recent post
    elif media_id != None:

        # creating request url to get access to comments of own recent post by giving media_id and ACCESS_KEY as parameters.
        request_url = (BASE_URL + "media/%s/comments/?access_token=%s") % (media_id, ACCESS_KEY)
        print "GET request url [to get comments data]: %s" % (request_url)

        # to make request and save the response in json format
        comment_info = requests.get(request_url).json()

        # if request made is successfull
        if comment_info["meta"]["code"] == 200:

            # Check if found comments on the post or not
            if len(comment_info["data"]) > 0:

                # And then read them one by one
                count_comments = 0
                count_neg_comments = 0
                for comment in comment_info["data"]:
                    comment_text = comment["text"]

                    # saving the behaviour of picked comment [i.e., comment_text] to variable blob
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                    count_comments += 1

                    # if weight of picked comment [i.e., comment_text] is negative, then delete it...
                    if blob.sentiment.p_neg > blob.sentiment.p_pos:
                        count_neg_comments += 1
                        comment_id = comment["id"]

                        # creating a request to delete specific comment by passing media_id, comment_id, ACCESS_KEY as parameters
                        delete_url = (BASE_URL + "media/%s/comments/%s/?access_token=%s") % (
                            media_id, comment_id, ACCESS_KEY)
                        print "DELETE request url : %s" % (delete_url)

                        # to make request and save the response in json format
                        delete_info = requests.delete(delete_url).json()

                        if delete_info["meta"]["code"] == 200:
                            print "Comment successfully deleted!"
                        else:
                            print "Could not delete the comment"

                # if there is no negative comments on the post
                if (count_neg_comments == 0):
                    print "Great!! %s have %d comments.\n And none of them were negative" \
                          % (comment_info["data"][0]["from"]["full_name"].capitalize(), count_comments)

                # if found some negative comments on the post
                else:
                    print  "%s have %d comments.\n And %d of them were negative" \
                           % (comment_info["data"][0]["from"]["full_name"].capitalize(), count_comments,
                              count_neg_comments)

            # Check if do not found any comment on the post
            else:
                print "No comments found. \n"

        # if request made is unsuccessfull
        else:
            print "Status code other than 200 received!. \n check for Comment request_url [to get recent comments] \n"


# -------------------------------  function delete_negative_comments_self() ends here  ----------------------------------------------------------------



# -------------------------------  function delete_negative_comments_of_user() starts here  -----------------------------------------------------------

# function name: delete_negative_comments_of_user(), to delete negative comments on the recent post after doing sentimental analysis,
                                           # it takes username as a parameter

def delete_negative_comments_of_user(insta_username):

    # fetching media id of the recent post by passing instagram username where user want to make sentimental analysis over 'comments'
    media_id = get_user_post(insta_username)

    # If get_user_post() returns no post to show then,
    if media_id == "no post to show":
        print "So you can't make any sentimental analysis"

    # And if get_user_post() returns unsuccsessfull request then,
    elif media_id == "unsuccessfull request":
        print "\n please check request URL \n"

    # And if get_user_post() returns the id(it is a string) of recent post
    elif media_id != None:

        # creating request url to get access to comments of a recent post by giving media_id and ACCESS_KEY as parameters.
        request_url = (BASE_URL + "media/%s/comments/?access_token=%s") % (media_id, ACCESS_KEY)
        print "GET request url [to get comments data]: %s" % (request_url)

        # to make request and save the response in json format
        comment_info = requests.get(request_url).json()

        # if request made is successfull
        if comment_info["meta"]["code"] == 200:

            # Check if we have comments on the post or not
            if len(comment_info["data"]) > 0:

                # And then read them one by one
                count_comments = 0
                count_neg_comments =0
                for comment in comment_info["data"]:
                    comment_text = comment["text"]

                    # saving the behaviour of picked comment [i.e., comment_text] to variable blob
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                    count_comments +=1

                    # if weight of picked comment [i.e., comment_text] is negative, then delete it...
                    if blob.sentiment.p_neg > blob.sentiment.p_pos:
                        count_neg_comments +=1
                        comment_id = comment["id"]

                        # creating a request to delete specific comment by passing media_id, comment_id, ACCESS_KEY as parameters
                        delete_url = (BASE_URL + "media/%s/comments/%s/?access_token=%s") % (
                            media_id, comment_id, ACCESS_KEY)
                        print "DELETE request url : %s" % (delete_url)

                        # to make request and save the response in json format
                        delete_info = requests.delete(delete_url).json()

                        if delete_info["meta"]["code"] == 200:
                            print "Comment successfully deleted!"
                        else:
                            print "Could not delete the comment"

                # if there is no negative comments on the post
                if (count_neg_comments == 0):
                    print "Great!! %s have %d comments.\n And none of them were negative" \
                          %(comment_info["data"][0]["from"]["full_name"].capitalize(), count_comments)

                # if found some negative comments on the post
                else :
                    print  "%s have %d comments.\n And %d of them were negative" \
                          %(comment_info["data"][0]["from"]["full_name"].capitalize(), count_comments, count_neg_comments)

            # Check if do not found any comment on the post
            else:
                print "No comments found. \n"

        # if request made is unsuccessfull
        else:
            print "Status code other than 200 received!. \n check for Comment request_url [to get recent comments] \n"

    # And if get_user_post() returns None ie, type(media_id) == NoneType then,
    else:
        print "Please enter a valid Instagram username \n"

# -------------------------------  function delete_negative_comments_of_user() ends here  -------------------------------------------------------------



# -------------------------------  function fetch_user_comments() starts here  ------------------------------------------------------------------------

# function name : fetch_user_comments(), used to fetch comments of a user by passing their username as parameter

def fetch_user_comments(insta_username):

    # fetching media id of the recent post by passing instagram username
    media_id = get_user_post(insta_username)

    # If get_user_post() returns no post to show then,
    if media_id == "no post to show":
        print "So you can't make any sentimental analysis"

    # And if get_user_post() returns unsuccsessfull request then,
    elif media_id == "unsuccessfull request":
        print "\n please check request URL \n"

    # And if get_user_post() returns the id(it is a string) of recent post
    elif media_id != None:

        # creating request url to get access to comments of a recent post by giving media_id and ACCESS_KEY as parameters.
        request_url = (BASE_URL + "media/%s/comments/?access_token=%s") % (media_id, ACCESS_KEY)
        print "GET request url [to get comments data]: %s" % (request_url)

        # to make request and save the response in json format
        comment_info = requests.get(request_url).json()

        # if request made is successfull
        if comment_info["meta"]["code"] == 200:

            # Check if we have comments on the post or not
            if len(comment_info["data"]) > 0:

                # And then print them one by one
                print("\n\nS.No.    Name         Comments \n==============================")
                count_comments = 0
                for comment in comment_info["data"]:
                    comment_made_by = "\033[1;31m" + comment["from"]["full_name"].capitalize() + "\033[0;0m"
                    comment_text = " \033[4;30;44m" + comment["text"] + "\033[0;0m"
                    count_comments += 1
                    print "%d.    %s  %s\n" % (count_comments, comment_made_by, comment_text)

                print "Total comments: %s" % (count_comments)

            # Check if do not found any comment on the post
            else:
                print "No comments found. \n"

        # if request made is unsuccessfull
        else:
            print "Status code other than 200 received!. \n check for Comment request_url [to get recent comments] \n"

    # And if get_user_post() returns None ie, type(media_id) == NoneType then,
    else:
        print "Please enter a valid Instagram username \n"


# --------------------------------  function fetch_user_comments() ends here  -------------------------------------------------------------------------



#--------------------------------  function more_options() starts here  -------------------------------------------------------------------------------

# function name: more_options(), used to provide some extra features [exploring some more features of Instagram API]

def more_options():

    while True:

        print """                MORE OPTIONS \n=========================================================\n                 

                select an option:
                
                     1. To get list of people you follows     
                     2. Check your_followers list
                     3. Back to Main Menu
                                                                            
       \033[4;30;44m  Note: These lists will be in reference with your Sandbox Users \033[0;0m 
             \033[4;30;44m And the scope with which Access Token is authorized \033[0;0m
                                                                               
        --------------- press m anytime for the Main Menu ------------"""        # ^^^ reset color and underlining
        option = raw_input()

        # to extract the list of people you follow
        if option == '1':
            user_follows()

        # to extract the self's[owner of access key] following list
        elif option == '2':
            check_followers_list()

        # to get back into main menu
        elif option.upper() == 'M' or option == '3':
            print "\n Entering Main menu... \n"
            break

        # if user made a wrong entry
        else:
            # if spy selected an in valid option
            message_box("whoa! You don\'t selected anything or may pressed invalid character\n Please try again. \n","Oops", 0)


#--------------------------------  function more_options() ends here  ---------------------------------------------------------------------------------



# -------------------------------  function user_follows() starts here  -------------------------------------------------------------------------------

# function name : user_follows(), Used to check for the list people who are followed by 'self'[the owner of Access key]

def user_follows():

    # creating request url for accessing the list of people who are followed by 'self'.
    request_url = (BASE_URL + "users/self/follows?access_token=%s") % (ACCESS_KEY)
    print "GET request url : %s " % (request_url)

    # to make request and save the response in json format
    user_info = requests.get(request_url).json()

    # if code recieved !=200 [ i.e., request made is unsuccessfull]
    if user_info["meta"]["code"] == 400 and user_info["meta"]["error_type"] == "OAuthPermissionsException":

        print "\033[4;31;40m"," You must re-authorize Access-Token with scope = follower_list to be granted this permissions. ", \
             "\033[0;0m \n" # resetting color of text

    # if code recieved ==200 [ i.e., request made is successfull]
    else:

        # if there is some friend who followed by -'self'[the owner of Access key]
        if len(user_info["data"]):

            # extracting friend names who are followed -'self'[the owner of Access key]
            count_friend = 0
            for friend in user_info["data"]:
                count_friend +=1
                print "%d. %s \n " %(count_friend, friend["full_name"])

        # if there no friend who is followed -'self'[the owner of Access key]
        else:
            print "There is no friend who follows you"


# -------------------------------  function user_follows() ends here  ---------------------------------------------------------------------------------



# -------------------------------  function check_followers_list() starts here  -----------------------------------------------------------------------

# function name: check_followers_list(), used to check for people who follows 'self'[the owner of Access key]

def check_followers_list():

    # creating request url for accessing the list of people who follows 'self'.
    request_url = (BASE_URL + "users/self/followed-by?access_token=%s") % (ACCESS_KEY)
    print "GET request url : %s " % (request_url)

    # to make request and save the response in json format
    user_info = requests.get(request_url).json()

    # if code recieved !=200 [ i.e., request made is unsuccessfull]
    if user_info["meta"]["code"] == 400 and user_info["meta"]["error_type"] == "OAuthPermissionsException":

        print "\033[4;31;40m", " You must re-authorize Access-Token with scope = follower_list to be granted this permissions. ", \
            "\033[0;0m \n"  # resetting color of text

    # if code recieved ==200 [ i.e., request made is successfull]
    else:

        # if there is some friend in following list of -'self'[the owner of Access key]
        if len(user_info["data"]):

            # extracting friend names who are followed -'self'[the owner of Access key]
            count_friend = 0
            for friend in user_info["data"]:
                count_friend += 1
                print "%d. %s \n " % (count_friend, friend["full_name"])

        # if there is no friend in following_list of -'self'[the owner of Access key]
        else:
            print "There is no friend who follows you"


# -------------------------------  function check_followers_list() ends here  -------------------------------------------------------------------------


# lets initiate the magic
start_bot()


# ========================================  Program Ended  ============================================================================================


'''
                                 Function Definitions at a Glance
                                 --------------------------------


1.  start_bot()      : It provides instabot menu and keep it untill user himself/herself don't want to exit from instabot
2.  message_box()    : To alert, or to communicate with spy for other suggetions like invalid enties etc.,  
3.  self_info()      : Used to fetch self information from instagram account
4.  get_user_id()    : Used to fetch user_id of a instagram user by passing instagram user name
5.  get_user_info()  : Used to fetch user details of a instagram user by passing instagram user name
6.  get_own_post()   : Used to fetch recent post of owner of access key
7.  get_user_post()  : used to fetch the recent post of a instagram user by passing instagram user name
8.  like_a_post()    : To like recent post of the user whose user name is passed as parameter                       
9.  post_a_comment() : Used to comment on recent post of the user whose user name is passed as parameter
10. delete_negative_comments_self()    : To delete negative comments on own recent post after doing sentimental analysis
10. delete_negative_comments_of_user() : To delete negative comments on the recent post of a user after doing sentimental analysis,
                                       it takes username as a parameter 
11. fetch_user_comments()              : used to fetch comments of a user by passing their username as parameter                                       
12. more_options()   : Used to provide some extra features [exploring some more features of Instagram API]                                 
13. user_follows()   : Used to check for the list people who are followed by 'self'
14. check_followers_list()     : Used to check for the list people who follows 'self'
'''