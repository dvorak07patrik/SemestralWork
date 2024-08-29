# Formula 1 Racing Results Manager Web App

## Technologies Used
- **Blazor (Server-side)**: Using Blazor for server-side work and communication with the database
- **.NET 8**
- **Entity Framework Core**
- **PostgreSQL**: Using PostgreSQL database to saving Formula 1 related data
- **MSSQL**: Using MSSQL database for saving user data
- **Chart.js**: Using Chart.js for implementing charts in javascript
- **HTML**
- **Javascript**: For using chart.js and for dynamic web functions

## Prerequisites
- **.NET 8**
- **PostgreSQL database**

## Project Structure
- **Data/Models**: Data model we use for Formula 1 related data
- **Data/DatabaseComm**: Classes for communicating with the database through database context
- **Data/Migrations**: Files used for migrating MSSQL database
- **Components/Pages**: Pages for Driver Standings, Results, and upcomings
- **Components/Account**: Account related pages
- **Layout**: Main Layout components like navigation
- **Components/App.razor**: HTML head with links and references used in other components
- **Components/_Imports**: .NET imports used in other components
- **Components/Routes**: Set the page routing
- **wwwroot/bootstrap**: Bootsrap file is saved here
- **wwwroot/app.css**: Main css file
- **wwwroot/js**: Main javascript file is saved here
- **Program.cs**: Sets up whole application
- **appseting.json**: Has some settings for example database connection string

## Components
### Main part of the project are components
#### RaceDetails.razor
- **Each razor component has more layers**
- **Routing**: We use URL routes to pass parameters to the page
- **HTML combined with C# code**: Used for controling what the user sees in each interaction
- **RaceDetails.razor.css**: Subfile for RaceDetails.razor that implements css just for this component
- **@code{} - code part**: Used to implement all the logic needed for controling the page and what user sees, it communicates with database through separate class
-  **async functions and methods**: Using asynchronous methods to allow applications to remain responsive, especially with UI
-  **javascript**: Using functions to implement chart.js to display charts and also to dynamically change the URL
-  
#### Adding a new component
- **To add a new component**: Click in VS 2022 on Pages -> Add -> RazorComponent and add it
- **Use of database**: To get things from database use methods of Formula1ManagerWebApp.Data.DatabaseComm by injecting DatabaseCommunicationForStandings. You can also add other classes or methods if it suits you better
- **Use of model**: To use model just add "@using Formula1ManagerWebApp.Data.Models" you can inspire yourself in other components
- **Use of URL parameters**: with @page "/your-new-site/{someParameter:typeOfParameter}" you add routing option and than you need to add [Parameter] to the code to use the parameter in your code
- **Build Action**: When debuging in VS 2022 don't forget to click on the component and set Build Action to "Content"

#### Program.cs
- **Builds and sets up the whole application**
- **Add scopes for database communications, for user identity etc.**
- **Adds database contexts for MSSQL database with User data and for PostgreSQL database with F1 data**: connects to the databases with connections strings saved in appsettings.json