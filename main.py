import requests

BASE_URL = "https://api.instagram.com/v1/"
ACCESS_KEY = "4870715640.a48e759.874aba351e5147eca8a9d36b9688f494"

#-------------------------------  function self_info() starts here  ----------------------------------------------------

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
                                 % (name, user_name, posts, name.partition(' ')[0], follows, following, name.partition(' ')[0])

    else:
        print 'Oops! Unsuccessful response received for your HTTP request \nStatus code other than 200 received!'


#-------------------------------  function self_info() ends here  ------------------------------------------------------


self_info()