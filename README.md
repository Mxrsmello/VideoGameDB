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
- **SQL**: SQL queries are used to insert, update, delete, and query information from the database, supporting comprehensive data manipulation and retrieval.

## Project Structure
- **Database Tables**:
  - `Users`: Stores user information and personal details for library tracking.
  - `Friends`: Manages connections between users for social interactions.
  - `Games`: Holds core information about each game, including developer details, genres, and platforms.
  - `Ratings`: Stores user ratings for each game, enabling personalized recommendations.
  - `Owns`: Tracks ownership details for each user’s gaming library.

## Usage
This project is intended as a personal gaming catalog application, where users can:
1. Add new games to their library.
2. Connect with friends to share gaming recommendations.
3. Rate and review games for themselves and others to see.

The design prioritizes ease of use for tracking and expanding personal gaming collections while fostering a social, connected experience around gaming.

## Installation & Setup
1. Clone the repository.
2. Ensure SQLite3 is installed on your system.
3. Load the database schema into an SQLite environment to initialize the tables.
4. Execute the SQL queries to interact with the database.

## Contributors
Marcelo Ramirez & Marian Zuniga
