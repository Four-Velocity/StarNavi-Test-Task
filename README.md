# Starnavi test task
That is a social network prototype.  
This app consists of two parts: backend using *DRF* and frontend using *Vue-cli*.  
All apps are in dev stage, so probably I will attach dev settings and secret keys to the repository,
so U can reproduce the project.  

## Backend
I write backend without TDD, 'cause I want finish fast.  
Probably I will add some tests, and swager documentation.  
### Packages
The app developed using these libraries.

|Package                        |Version|Description                               |
|------------------------------:|:-----:|------------------------------------------|
|`Django`                       |3.0.5  |Django framework                          |
|`DjangoRestFramework`          |3.11.0 |Django REST Framework                     |
|`django-cors-headers`          |3.2.1  |Cross-Origin Resource Sharing support     |
|`django-rest-swagger`          |2.2.0  |Requests docs *not sure I'll use it*      |
|`djangorestframework-simplejwt`|4.4.0  |JSON Web Token authentication support     |
|`djoser`                       |2.0.3  |Django REST Framework authentication views|
|`faker`                        |4.0.2  |Dummy data generator                      |  
|`pyyaml`                       |5.3.1  |YAML parser                               |
|`psycopg2`                     |2.8.4  |PostgreSQL adapter                        |
|`pillow`                       |7.1.1  |Image processing support                  |
|`clearbit`                     |0.1.7  |Clerbit API                               |
|`pyhunter`                     |1.7    |EmailHunter API                           |
|`requests`                     |2.23.0 |Basic requests                            |

### Settings
The backend root contains files `dev_setting.yml` and `prod_settings.yml`.  
This files divided on two sections: *project* and *generator*.  
If some non-Required settings won't be provided they will be set by default.  
`utils.py` have functions to parse settings from Yaml to python vars.  
#### Project
This section contains settings that are required for properly work

|Parameter|Type|Category|Description|Required|
|---:|:---:|---|---|:---:|
|`django_secret_key`|`str`|***Main Settings***|Django secret key|:heavy_check_mark:|
|`clearbit_key`|`str`|*API Settings*|Clearbit API Key|:heavy_check_mark:|
|`emailhunter_key`|`str`|*API Settings*|EmailHunter API Key|:heavy_check_mark:|
|`adorable_avatar`|`bool`|*API Settings*|Generate [adorable avatar](http://avatars.adorable.io) by default if user avatar is empty |:heavy_check_mark:|

#### Generator
This sections contains settings for generator bot.
> Note: Exclamation mark in **Required** field means that setting is required if previous `bool` field is `True`

|Parameter           |Type           |Default        |Category             |Description|Required|
|-------------------:|:------------: |:--------------|---------------------|---|:---:|
|`number_of_users`   |`int`          |               |***Main Settings***  |Number of users that will be generated|:heavy_check_mark:|
|`max_posts_per_user`|`int`          |               |***Main Settings***  |Maximum number of posts each user's can create|:heavy_check_mark:|
|`max_likes_per_user`|`int`          |               |***Main Settings***  |Maximum number of posts each user can like|:heavy_check_mark:|
|`api_sleep`         |`float`        |*0.07*         |*Main settings*      |Time in seconds that generator will wait before next request to API resource|:heavy_check_mark:|
|`start_datetime`    |`date %Y-%m-%d`|*now - 2 month*|*Post Settings*      |Start of datetime range in which users and posts will be created|:x:|
|`end_datetime`      |`date %Y-%m-%d`|*now*          |*Post Settings*      |End of datetime range in which users and posts will be created|:x:|
|`max_post_length`   |`int`          |*1024*         |*Post Settings*      |Maximum length of post|:x:|
|`image_generation`  |`bool`         |*true*         |*Post/Image Settings*|Insert random images in posts, or not|:x:|
|`images_percent`    |`float`        |*0.333*        |*Post/Image Settings*|Approximate percentage of posts that will be generated with pictures|:heavy_exclamation_mark:|
|`unsplash_key`      |`str`          |               |*Post/Image Settings*|[Unsplash](https://unsplash.com) API access key to choose random pictures|:heavy_exclamation_mark:|

### Generator bot
This is class using to fill db with fake users and posts.
To use it you should start ***django shell***, and after run next commands:
```python
from generator.generator import Generator

g = Generator()
# Or you can provide specific settings
g = Generator(number_of_users=10, max_post_length=2048)

g.generation()
```
This generator creates `number_of_users` users, from 0 to `max_posts_per_user` posts for every user,
and make them like from 0 to `max_likes_per_user` posts.  
Max `user.date_joined` for user is `start_datetime`.  
Min is `end_date`.  
The post's date are specific for every user. It starts with `user.date_joined` and ends with `end_date`.  
If `image_generation` is `True` the posts will include random pics.

:heavy_exclamation_mark: ***PAY ATTENTION*** that usplash basic api allows generating only 50 images/hour.  
If you run generator with 1000 posts it's ok, because there is condition to generate max 50 images.  
But if U'll run generator again, U'll probably get ~~unhandled exception~~ I really don't know what U'll get. I've never generating so many images. :sweat_smile:  
According to this when you are using generator for 2'nd time in an hour do this on class creation
```python
g = Generator(image_generation=False)
```
or provide your api key in settings

## Frontend
This part is made using Vue-cli.  
It's to raw and to prototypic, but it's working somehow :grin:
### Packages
|Package      |Version|Description|
|------:      |:-----:|:----------|
|`axios`      |0.19.2 |Used for ajax requests|
|`querystring`|0.2.0  |Used to stringify objects|
|`vue-cookies`|1.7.0  |Added ability to work with cookies|
|`vue-moment` |4.1.0  |Format date_time|
|`vue-router` |3.1.6  |Page routing|

### Workflow
That vue app has such pages as:
* Login
* Register
* Home
* User
#### Login
Loging in user requesting `/auth/jwt/create/`  
#### Register
Creating user requsting `/auth/users/` and `/api/profile/<id>/`  
Also validates email and getting additional info about user requesting `/auth/validate/`  
#### Home
Home page.  
Shows all posts requesting `/api/posts/all/`  
Allowing to like posts requesting `/api/like/<id>`  
#### User
Show info about user and all user posts.  
Requesting `/api/users/<id>/` and `/api/posts/<username>/`  
Allowing owner to edit profile, requesting `/api/profile/<id>/`  
Allowing owner to delete posts requesting `/api/posts/<id>/`  

## Launching
To launch app copy this repository and do next.
### Backend launching
* Activate virtualenv if you want to
* `cd PROJECT_ROOT/star_navi_backend`
* Provide missing settings in `prod_settings.yml` or `dev_settings.yml`
* Install requirements and makemigrations
> Note: psycopg2 and Pillow can be not installed. Update your pip to resolve the problem  
> Basicly it helps me :confused:
* Fill DB with dummy data using [*Generation bot*](#generator-bot)
* Run server exactly on 127.0.0.1:8000
> Sowwy 4 that, I haven't provide url-address settings in vue 
### Frontend launching
* Install vue-cli
* `cd PROJECT_ROOT/star_navi_frontend`
* Install requirements
* Run: `npm run serve`
> Note: if you will have eslint errors you need to have it globally to fix them
> run `eslint --fix src/**`

