Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. It is a simple and minimalist appication created to express my knowledge of implementing my CRUD operation fundamental.

Created during my early stage in software development, i occassionally refactor it with new features

Most of the frontend utilities of the application where offered by Udacity. The backend logic was implement by me/

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

The fastest way to install all dependencies mentioned above running `pip` as:
```
pip3 install -r requirements.txt
```

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
├── server
│ ├── app.py
  ├── CODEOWNERS
  ├── config.py
  ├── error.log
  ├── fabfile.py
  ├── forms.py
  ├── __init__.py
  ├── models.py
  ├── README.md
  ├── settings.py
  ├── static
  ├── templates
  │   ├── errors
  │   │   ├── 404.html
  │   │   └── 500.html
  │   ├── forms
  │   │   ├── edit_artist.html
  │   │   ├── edit_venue.html
  │   │   ├── new_artist.html
  │   │   ├── new_show.html
  │   │   └── new_venue.html
  │   ├── layouts
  │   │   ├── form.html
  │   │   └── main.html
  │   └── pages
  │       ├── artists.html
  │       ├── home.css
  │       ├── home.html
  │       ├── search_artists.html
  │       ├── search_venues.html
  │       ├── show_artist.html
  │       ├── show.html
  │       ├── shows.html
  │       ├── show_venue.html
  │       └── venues.html
  ├── utils.py
  └── views.py
├── requirements.txt
└── wsgi.py


## Development Setup
1. **Download the project starter code locally**
```
git clone https://github.com/Chiefkufre/fyyur
cd fyuur
```

2. **Create an empty repository in your Github account online. To change the remote repository path in your local repository, use the commands below:**
```
git remote -v 
git remote remove origin 
git remote add origin <https://github.com/<USERNAME>/<REPO_NAME>.git>
git branch -M main
```

3. **Initialize and activate a python environment using:**
```
python -m venv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

4. **Install the dependencies:**
```
pip install -r requirements.txt
```

5. **Run the development server:**
```
python3 wsgi.py
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

