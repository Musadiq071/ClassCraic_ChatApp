# ClassCraic 

## Overview

Class Craic is specially designed for the purpose of communication among teachers and students. The platform provides multiple forms of interaction which include public chat, Private messaging and class-based group chats.

Users can create accounts and manage their profiles, choose their role and start exploring the application.


Users can communicate in a public chat space where they can introduce themselves, share announcements, discuss daily activities, and post general information.

Private messaging: The Application provides private messaging which allows teachers and students to communicate with chosen user as one-to-one conversation

For structured and better controlled communication, Applcation provides class based groupchats which can be created by teachers, after creation the joining code is created which teacher can share with the students.
Students can join the class group by using the unique code joining code of the groupchat 
Within class group-chats, users can discuss class activities, share notes, and upload files or images.


The goal of this project was to create a simple but structured communication system for a college-style environment, with proper role management and real-time interaction.

---

## Project Aim

I wanted to build ClassCraic Chat App  because many existing chat applications are very general-purpose and not specifically designed for an educational environment. My aim was to create a simple and focused platform tailored for students and teachers, where communication is structured and relevant to academic use.

The goal was to include only the necessary features such as group discussions, private messaging, and file sharing, while keeping the interface easy to use and not overloaded with unnecessary complexity.

I also implemented role-based functionality so that teachers and students have different responsibilities within the system. Teachers can create and manage class groups, while students can join groups and participate in discussions. This makes the platform more organised compared to generic chat applications.

Another important part of the project was to support practical use cases, such as sharing notes, images, and files directly within chats, which is useful for everyday class activities.

In addition, I wanted this project to be useful beyond just a final-year submission. The system is designed in a way that small colleges or institutions with limited budgets could potentially reuse or adapt the code to build their own internal communication platform.

Moreover, it also offers language translation feature by which different language text can be translated into English in an effort to break language barrier among peers.

Overall, the focus of this project was to create a clean, functional, and educational-focused chat system that demonstrates real-time communication, role-based access control, and practical usability.
This makes the app more controlled than a normal chat system and closer to a real educational platform.

---


## Features

###  Authentication & User Profiles
- Users can create accounts and log in securely
- Each user has a profile with:
  - username
  - preferred name
  - avatar
  - role (student or teacher)
- Users can update and manage their profile information any time

---

###  Real-Time Chat System
- Messages are sent and received instantly without refreshing the page
- Built using WebSockets (Django Channels)
- Supports both text messages and file sharing

---


###  Public Chat
- Open chat space available to all users
- Used for:
  - introductions
  - announcements
  - general discussions
  - sharing common information

---

###  Private Messaging
- One-to-one chat between users
- Students can message other students
- Students and teachers can communicate privately
- Private chat rooms are created automatically when a conversation starts

---

###  Class Group Chats
- Teachers can create class groups
- Each group generates a unique join code
- Students can join groups using the code
- Only group members can access the chat

---

###  Teacher Role & Permissions
- Only users with the teacher role can create class groups
- Teachers can:
  - manage their class groups
  - can see join code for group
  - view members
  - remove students from groups
  - delete groups if needed

---

###  Admin Controls
- Admin (superuser) has full control of the system
- Admin can:
  - approve teachers
  - disapprove teachers
  - manage all groups

---

###  Teacher Approval System
- Teachers must be approved before they can create groups
- Admin decides who becomes a teacher
- If a teacher is disapproved:
  - they lose teacher permissions
  - existing class groups are not deleted (to avoid data loss)


---

###  File & Image Sharing
- Users can upload files in chats
- Images are displayed directly in the chat
- Other file types are available for download


---

### Message Translation

The application includes a message translation feature implemented using the `deep-translator` python library.

This allows users to translate chat messages into English directly within the chat interface.

#### Installation

The translation library is included in the project dependencies. If needed, it can be installed manually:

```bash
pip install deep-translator==1.11.4
```

#### How It Works

- When a user requests translation, the message text is processed using the library
- The source language is automatically detected
- The message is translated into English
- The translated text is displayed without refreshing the page

#### Example Usage:

```python
from deep_translator import GoogleTranslator

translated_text = GoogleTranslator(
    source='auto',
    target='en'
).translate("Hola mundo")
```

#### Points to note
- If translation fails, a fallback message is shown
- The main chat system works independently of this feature

---

###  Online User Tracking
- Shows users who are currently online in a chat
- Updates in real-time

---

###  Chat Management
- Users can leave private and group chats
- Teachers/Admin can manage group members
- Admin/Teacher can delete class groups

---

###  Database System
- Uses PostgreSQL for better performance and reliability
- Supports multiple users and real-time operations efficiently

---

### Real-Time Updates with WebSockets
- Messages and online status update instantly
- No page reload required
- Improves user experience compared to traditional apps



## System Design

###  Real-Time Messaging (WebSockets)

The chat system is built using Django Channels, which allows real-time communication through WebSockets.

When a user sends a message:
1. The message is sent through a WebSocket connection
2. The server receives the message and saves it in the database
3. The message is broadcast to all users connected to that chat group
4. The chat updates instantly on all users’ screens without refreshing

This makes the application faster and more interactive compared to traditional request-response systems.

---

###  Chat Groups & Structure

The application supports three types of chat:

- **Public Chat** → open to all users  
- **Private Chat** → one-to-one communication  
- **Class Groups** → created by teachers for structured discussions  

Each chat group is stored in the database and has:
- a unique group name
- a type (public, private, or class)
- a list of members

Private chats are automatically created when two users start a conversation.

---

###  Permission System

The system uses role-based access control to manage who can do what.

There are three roles:
- Student
- Teacher
- Admin

Permissions are enforced in two places:
1. Django views (HTTP requests)
2. WebSocket consumers (real-time communication)

This ensures users cannot bypass restrictions.

Examples:
- Only approved teachers can create class groups
- Only members can access a class chat
- Admin can override permissions

---

###  Teacher Approval Logic

A teacher must be approved before they can create or manage class groups.

If a teacher is disapproved:
- They lose access to teacher features
- Their existing class groups remain active

This helps to reduce risk of student data loss like chats history.
---

###  Online User Tracking

The application tracks which users are currently online in each chat group.

When a user connects:
- They are added to an online users list

When they disconnect:
- They are removed from the list

This information is updated in real-time and displayed in the chat interface.

---

### File Handling

Messages can include file uploads.

- Images are displayed directly in the chat
- Other files are available as download links
- File size can't exceed 5MB.

Files are stored and linked to the message in the database.

---

###  Database Design

The system uses PostgreSQL as the main database.

Key models include:
- ChatGroup → stores chat information
- GroupMessage → stores messages
- User/Profile → stores user data and roles

Relationships:
- Users belong to chat groups
- Messages belong to both users and groups

---

###  Data Flow Summary

1. User sends message  
2. Message saved in database  
3. Message broadcast via WebSocket  
4. UI updates instantly  

This cycle ensures real-time communication across all users.



##  Tech Stack

This project uses a combination of backend, frontend, and real-time technologies to build a full-stack chat application.

---

###  Backend

#### Django
- Main web framework used to build the application
- Handles:
  - URL routing
  - views and templates
  - authentication system
  - database models

I chose Django to built this project  because it provides a structured and secure way to build full-stack applications 
with many built-in features, and also because I already have strong experience and familiarity with it, which helped me to develop the project more efficiently.
---

#### Django Channels
- Used to add real-time functionality to the app
- Enables WebSocket communication

Used for:
- live chat messages
- online user tracking

I used Channels because Django alone follows a request-response model and does not support real-time updates.

---
#### Redis
- Used as the channel layer for Django Channels
- Handles real-time message broadcasting and online user tracking


#### Daphne (ASGI Server)
- Used to run the application with WebSocket support
- Required for Django Channels

---

#### Django Allauth
- Handles authentication features
- Provides:
  - signup/login
  - account management

I used Django Allauth because it offers secure and structured handling of authentication, 
and it is flexible enough to extend for role-based features like teachers and students in my application.

---

---

###  Frontend

#### HTML (Django Templates)
- HTML is used to build the UI structure
- Integrated with Django template engine for dynamic content

---

#### Tailwind CSS
- Used for styling the UI
- Provides utility classes for fast and better design

I chose Tailwind because it allows building clean and responsive layouts quickly.

---

#### HTMX
- Used for dynamic updates without full page reload
- Handles:
  - form submissions
  - partial updates

Helps reduce JavaScript complexity.

---

#### Alpine.js
- Lightweight JavaScript framework
- Used for:
  - dropdown menus
  - UI interactions

I used Alpine.js instead of heavy frameworks like React to keep the project simple and light-weight.

---

---

###  Real-Time Communication

#### WebSockets
- Enables two-way communication between client and server
- Used for:
  - instant messaging
  - live updates

This is the core technology behind the chat system.

---

---

###  Database

#### PostgreSQL
- Main database used for the project
- Stores:
  - users
  - messages
  - chat groups

I switched from SQLite to PostgreSQL because :
- of its better performance with multiple users
- more suitable for production
- handles concurrent operations better

---

---

###  Other Tools & Libraries

#### Psycopg
- PostgreSQL adapter for Python
- Allows Django to connect to PostgreSQL

---

#### Whitenoise
- Used to serve static files in production

---

#### Hyperscript
- Used for small frontend interactions
- Works well with HTMX

---

#### Python
- Main programming language used for backend logic

---

---

###  Development Tools

- Virtual environment (venv)
- Git & GitHub for version control
- Render for deployment

---


---
## Installation & Setup

Follow the steps below to run the project locally.

**Python 3.10+ is recommended**

---

### 1. Clone the Repository

```bash
git clone https://github.com/Musadiq071/ClassCraic_ChatApp.git
cd ClassCraic_ChatApp
```

---

### 2. Create a Virtual Environment

```bash
python -m venv env
```

Activate the environment:

**Mac/Linux:**
```bash
source env/bin/activate
```

**Windows:**
```bash
env\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Install PostgreSQL

Make sure PostgreSQL is installed and running on your system.

Download from:  
https://www.postgresql.org/download/

After installation, ensure the PostgreSQL service is running before creating the database.

---

### 4. Set Up PostgreSQL Database

Create a PostgreSQL database and user.

```sql
CREATE DATABASE classcraic;
CREATE USER your_user WITH PASSWORD 'your_password';
ALTER ROLE your_user SET client_encoding TO 'utf8';
ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE classcraic TO your_user;
```

Then update your `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'classcraic',  # create this DB in PostgreSQL
        'USER': 'your_user',   # replace with your local PostgreSQL username
        'PASSWORD': 'your_password',  # replace with your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

If you encounter permission issues, run:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO your_user;
```

---

### 5. Install & Run Redis

This project uses Redis for real-time communication.

**Redis must be running before starting the server, otherwise real-time features will not work.**

#### Mac (Homebrew):
```bash
brew install redis
brew services start redis
```

#### Linux:
```bash
sudo apt install redis-server
sudo systemctl start redis
```

#### Windows:
Install Redis using Docker or third-party builds.

For Docker:
```bash
docker run -p 6379:6379 redis
```

#### Verify Redis is running:
```bash
redis-cli ping
```

Expected output:
```bash
PONG
```

---

### 6. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

---

### 8. Run Development Server

```bash
python manage.py runserver
```

Then open:

http://127.0.0.1:8000/

After logging in:
- Create or log in as admin  
- Approve a teacher account  
- Create a class group  
- Join using the group code  

---

## Running with Daphne

This project uses Django Channels for real-time chat.

For normal local development, use:

```bash
python manage.py runserver
```

To run using Daphne directly (optional, for production-like testing):

```bash
daphne chatapp.asgi:application
```

---

## Environment Variables

For better security, use environment variables for sensitive data:

- SECRET_KEY  
- DATABASE_URL  
- DEBUG  
- REDIS_URL  

If environment variables are not set, default values in `settings.py` will be used.

Example:

```bash
export SECRET_KEY=your_secret_key
export DEBUG=True
```
---


## Deployment Notes(Optional)

For deployment:

- Use an ASGI server (Daphne)  
- Use PostgreSQL database  
- Set DEBUG = False  
- Configure allowed hosts  

The project is deployed using Render with PostgreSQL and redis.

The project is deployed on Render and can be accessed below:

https://classcraic-chatapp.onrender.com

### Extra Notes Based on My Journey in Completing This Project

These notes may help anyone who wishes to explore or extend the project further.

---

## Challenges Faced

During the development of this project, I encountered several practical challenges across backend logic, real-time communication, UI design, and database configuration. These issues helped me understand the system more deeply.

---

### Integrating Django Allauth with Custom Roles

One of the first challenges was integrating Django Allauth with my custom user profile system. I needed to support role-based functionality (student, teacher, admin), but Allauth does not directly handle custom roles.

I faced issues with:
- linking user profiles to authentication  
- managing role-based access after login  
- UI inconsistencies in Allauth templates  

**Solution:**  
I extended the user model using a profile model and manually handled role-based logic in views. I also customised the Allauth templates to match my application UI.

---

### WebSockets Connection Issues (Django Channels)

While implementing real-time chat, I faced problems with WebSocket connections not working properly.

The issue was caused by:
- mismatched versions of HTMX WebSocket extensions  
- incorrect WebSocket setup  

**Solution:**  
I ensured that the correct HTMX WebSocket extension (`hx-ext="ws"`) was used and matched with the proper script version. I also verified the ASGI configuration and ensured Daphne was correctly running the application.

---

### File Upload Handling in Chat

Another challenge was implementing file uploads alongside real-time messaging.

WebSockets do not handle file uploads directly, so combining file uploads with live chat was difficult.

**Solution:**  
I handled file uploads using a separate HTTP POST request (HTMX form), while keeping text messages over WebSockets. After uploading, I manually triggered the message broadcast so the file appeared in the chat instantly.

---

### PostgreSQL Migration & Permission Issues

When switching from SQLite to PostgreSQL, I faced a migration error:

> permission denied for schema public

This prevented Django from creating database tables.

**Solution:**  
After researching, I resolved the issue by granting proper permissions to the database user, which I have outlined below:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO your_user;
```

---

### Online User Tracking

Tracking online users in real-time was more complex and complicated than expected.

**Challenges included:**
- adding/removing users correctly on connect/disconnect  
- keeping the count accurate across multiple users  

**Solution:**  
I used a many-to-many field (`users_online`) in the chat group model and updated it in the WebSocket consumer during connection and disconnection events. The updated count is broadcast to all users in the chat.

---

### UI & Layout Issues

During development, I initially used multiple layout templates, which led to inconsistent styling across different pages.

I also faced some usability issues, such as poor text visibility due to colour contrast and a chat interface that felt too boxed and cluttered.

**Solution:**  
To fix this, I simplified the layout structure and standardised the design across the application. I used Tailwind CSS to improve spacing, colours, and responsiveness. These changes made the interface cleaner, easier to read, and more user-friendly across different devices.

---

### Teacher Permissions & Group Management

Designing the teacher system required careful thinking and consideration based on project requirements.

**Challenges:**
- ensuring only approved teachers can create groups  
- allowing teachers to manage members  
- handling what happens when a teacher is disapproved  

**Solution:**  
I implemented role checks in both views and WebSocket consumers. I also made a design decision that disapproving a teacher should remove their permissions but not delete existing class groups, to avoid losing student data.

---

### Combining Multiple Technologies

The project combines Django, Channels, HTMX, Alpine.js, Redis, and PostgreSQL.

One challenge was making sure all these parts worked together correctly without conflicts.

**Solution:**  
I kept the frontend simple and used HTMX and Alpine.js instead of a complex framework. This made integration easier and reduced bugs.

---

### Message Translation Feature

Initially, due to short timeframe, message translation was considered an optional feature. However, using a Python library (`deep-translator`), I was able to implement it in a simple and efficient way.

This feature can be particularly useful in bilingual or multilingual educational settings, where it helps reduce language barriers between peers.

To keep the system lightweight and avoid unnecessary complexity, translated messages are not stored in the database. Instead, they are generated and displayed instantly when requested.

In my opinion, this approach provides a practical balance — adding useful functionality without making the system heavy or over-engineered.

---

## Future Improvements

- Voice transcription  
- Notifications system  
- Better mobile responsiveness  
- Message reactions  

---

##  Author

Musadiq Hussain
Final Year Computing Student
Dublin Business School

---

##  License

This project is for educational purposes.



