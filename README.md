# CSE 111: Video Game Library Database Project

### Created by: Marcelo Ramirez & Marian Zuniga

## Project Overview
This video game database project is designed to manage and log detailed information about games owned by users. It functions as a personal gaming catalog, enabling users to track their gaming library, preferences, and interactions with friends. 

The database stores a range of game-specific details, including:
- Game descriptions
- User ratings
- Personal ownership records

## Key Features
- **Library Tracking**: Users can maintain a catalog of the games they own, providing a clear overview of their gaming collection.
- **Social Interaction**: Users are linked with their friends, allowing them to:
  - Share game recommendations
  - View each other's gaming activity and ratings
  - Stay informed about what games friends are currently playing
- **Game Details**: The database includes extensive information about each game, making it easy for users to explore game details and discover new favorites.
- **User Ratings and Reviews**: Users can rate games and leave reviews, fostering a shared community experience.

## Technologies Used
- **SQLite3**: A lightweight, self-contained SQL database engine that serves as the back-end database for this project.
- **Flask**: A Python micro-framework used to create the back-end logic and API endpoints.
- **HTML/CSS**: Utilized for designing the front-end user interface, providing an interactive and visually appealing experience for users.

## Project Structure
- **Database Tables**:
  - `Users`: Stores user information and personal details for library tracking.
  - `Friends`: Manages connections between users for social interactions.
  - `Games`: Holds core information about each game, including developer details, genres, and platforms.
  - `Ratings`: Stores user ratings for each game, enabling personalized recommendations.
  - `Owns`: Tracks ownership details for each user’s gaming library.

- **Frontend**:
  - Built with HTML and CSS to create a dynamic and user-friendly interface.
  - Pages include game library display, friend interactions, and review/rating forms.

- **Backend**:
  - Flask handles routing between the front-end and database.
  - RESTful API endpoints to perform CRUD operations (Create, Read, Update, Delete) on the database tables.

## Usage
This project is intended as a personal gaming catalog application, where users can:
1. Add new games to their library.
2. Connect with friends to share gaming recommendations.
3. Rate and review games for themselves and others to see.

The design prioritizes ease of use for tracking and expanding personal gaming collections while fostering a social, connected experience around gaming.

## Installation & Setup
1. Clone the repository.
2. Ensure SQLite3 and Python are installed on your system.
3. Install Flask using pip:
   ```
   pip install flask
   ```
4. Load the database schema into an SQLite environment to initialize the tables.
5. Start the Flask server to enable the back-end connection:
   ```
   python app.py
   ```
6. Open the front-end in a web browser to access the application interface.

## Contributors
Marcelo Ramirez & Marian Zuniga
