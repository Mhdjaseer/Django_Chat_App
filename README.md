
# Real-Time Chat Application

This is a real-time chat application that allows users to create chat rooms, join existing rooms, and communicate with other users in real-time. The application provides user authentication and authorization to ensure privacy and security. It is built using a web framework ( Django) for the server-side logic and user interface.
![Screenshot (79)](https://github.com/Mhdjaseer/Django_Chat_App/assets/98450786/ddc755cb-cc15-4874-a431-a2dec598e4e0)
![Screenshot (80)](https://github.com/Mhdjaseer/Django_Chat_App/assets/98450786/5093a1d4-97b6-455e-b936-3bdd1986de62)
![Screenshot (81)](https://github.com/Mhdjaseer/Django_Chat_App/assets/98450786/1be992fe-58df-46eb-b942-17099aa95ffd)

![Screenshot (83)](https://github.com/Mhdjaseer/Django_Chat_App/assets/98450786/87fc3b89-eca1-497a-a385-112234f57614)



## Features

* User registration and login: Users can create an account and authenticate themselves to access the chat application.

* Chat room creation and joining: Users can create their own chat rooms or join existing rooms to participate in conversations.
* Real-time messaging: Users can send and receive messages in real-time within a chat room, providing a seamless communication experience.
* User authentication and authorization: The application ensures that only authenticated and authorized users can access the chat rooms.
* User-friendly interface: The application provides an intuitive and user-friendly interface for users to view and participate in chat conversations.
* Additional features: The application includes features like message timestamps, user presence indicators, and notifications for new messages to enhance the user experience.
* Message editing and deletion: Users can edit and delete their own messages within a certain timeframe, giving them control over their conversations.
* Moderation features: The application implements basic moderation features to handle offensive or inappropriate content to maintain a positive environment.
* Scalability and concurrency: The application is designed to handle high concurrent connections and scale effectively to accommodate a large number of users.
* Unit tests: The application includes comprehensive unit tests to verify its functionality and ensure robustness.

## Technologies Used

 - [Web framework: Django](https://www.djangoproject.com/)
 - [Real-time communication: Django Channels](https://channels.readthedocs.io/en/stable/)
 - [Prevent-web attacks :django defender](https://django-defender.readthedocs.io/en/latest/)
 - [For template edit: django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/)
 - [Docker](https://www.docker.com/)

## Deployment

To deploy this project run


1. Clone the repository:

```bash
 https://github.com/Mhdjaseer/djanog_chat_app.git
```
or download the zip file 

2. Create virtual enviorment:

```bash
 python -m venv env
```
2. Make sure you have installed the Docker:

```bash
 https://www.docker.com/
```
3. Install Required Dependencies:

```bash
 pip install -r requirements.txt

```
4. install this already installed then ignore this step :

```bash
 python3 -m pip install channels_redis

```
5. run makemigration and migrate :

```bash
 python manage.py makemigrations
 python manage.py migrate

```
6. run your server :

```bash
python manage.py runserver 

```
7. after open your browser past it  :

```bash
http://127.0.0.1:8000/

```

8. if your not like realoading then, and the notification is to see then inside the room.html   :

```bash
#for removing reload 
#room.html > inside script  
location.reload()-- remove it
#for showing notifiaction 
#in side onmessage funntion add
showNotification('message recived')
#also add inside the querySelector function 
showNotification('message sended')

```


## Usage

1. Register a new user or log in with an existing account.
2. Create a new chat room or join an existing room.
3. Start sending and receiving messages in real-time.
4. Edit or delete your own messages within the allowed timeframe.
5. Enjoy the chat application!

## Security

- Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) protection is implemented using Django Defender middleware.
- User activities and system performance are logged and monitored for security purposes.(//not implemented //)

## Testing

Run the unit tests to verify the functionality and robustness of the chat application:(tested)
