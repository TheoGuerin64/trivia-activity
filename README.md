# trivia activity

*This project is under development until the end of Discord [Public Developer Preview](https://discord.com/developers/docs/activities/overview#public-developer-preview).*

This activity is a multiplayer trivia game. It handles user disconnection and reconnection, and allows for playing across multiple servers simultaneously.

The game utilizes [Open Trivia Database](https://opentdb.com/) API to fetch questions, currently limited to English. However, future versions will allow choosing the language.

## Usage
*Requires Docker and Docker Compose.*

- Create an Application in the [Discord Developer Portal](https://discord.com/developers/applications).
- Enable activities in the `Activity` tab.
- Create a .env file with the following content:
  ```
  DISCORD_CLIENT_ID=your_application_id
  DISCORD_CLIENT_SECRET=your_application_secret
  ```
  This informations can be found in the `OAuth2` tab.
- Run with `docker-compose up --build -d`.
- Run `docker-compose logs server-client client-tunnel` and copy the URLs to the `URL Mappings` tab like that:
![URL Mappings](https://github.com/TheoGuerin64/trivia-activity/assets/57496441/ef1f24c6-2933-492a-9c93-3ddf715c37e2)
- Go to a Discord voice channel in a Guild with less than 25 users.
- You are ready to play!
