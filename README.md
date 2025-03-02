# Endless Sky Ship Search Engine

## IT&C 350 Database Design Project - Winter 2024  
**Authors:**  
- Facundo Fernandez  
- Ethan Richmond  
- Jeremy Beutler  

## Project Overview  
The Endless Sky Ship Search Engine is a web application that allows users to query, modify, and add ship, outfit, and attribute information from the game *Endless Sky*. Users can create custom ships while maintaining the integrity of base-game ships.

## Features  
- Query ships, attributes, weapon stats, and default outfits  
- Create and modify custom ships  
- Base-game ships remain unmodifiable  
- Simple, intuitive UI for easy interaction  

## Tech Stack  
- **Database:** PostgreSQL 14.15 (Ubuntu 20.04)  
- **Backend:** TBD  
- **Frontend:** TBD  

## Database Setup  
To clone and initialize the database:  

```sh
git clone https://github.com/jeremybeutler/endlessskysearch.git
cd endlessskysearch/data/scripts
sudo -u postgres psql -f init.sql
```
To run queries or modify the database:

```
sudo -u postgres psql script.sh

```
