# Pantry Pilot (Django Delights)

## Project Overview
Pantry Pilot, originally known as Django Delights for the Codecademy Learn Django Skill Path, is a comprehensive inventory and sales application 
tailored for restaurant management. It enables efficient tracking of ingredients, menu items, recipe requirements, and sales to streamline the 
culinary business process.

## Features
- **User Authentication:** Secure login and logout functionality.
- **Menu Management:** Create and manage menu items along with their recipes, ingredients, costs, and sales prices.
- **Inventory Tracking:** Add and update ingredients in the inventory, including their unit of measurement, cost per unit, and available 
quantity.
- **Purchase Logging:** Record purchases of menu items with automatic inventory adjustments and user tracking.
- **Financial Insights:** View daily and monthly profit metrics on the home page.
- **Restock Notifications:** Receive notifications for items that need to be restocked, including the required quantity and associated costs.
- **Detailed Recipe Views:** Access individual pages for each menu item, detailing ingredients, instructions, and more.
- **Automatic Financial Updates:** Finances and inventory automatically adjust when purchases are logged.

## Installation Instructions
Before you begin, ensure you have Python, Django, Git, and command-line tools installed on your machine. Clone the project from GitHub and 
navigate to the project directory. Install the required dependencies listed in `requirements.txt`.

## Usage
Once installed, you can run the following command to start the development server:

python manage.py runserver

Open a web browser and navigate to http://127.0.0.1:8000/ to access the application. Create an account to begin managing your culinary business 
with Pantry Pilot.

## Tests
Testing instructions are forthcoming. Please check back for updates.

## Deployment
Pantry Pilot is currently in development and has not been deployed to a production environment. A demonstration video of the application in 
action is available on YouTube.

## Contributing
While Pantry Pilot is not actively seeking contributions, feedback and suggestions are always welcome. Please feel free to leave comments or 
reach out via GitHub.

## Credits
Pantry Pilot was developed as part of the Codecademy Learn Django Skill Path. Special thanks to Codecademy for providing the initial project 
framework and guidance.

## License
Pantry Pilot is currently not under any specific license.

## Contact Information
For more information or support, please visit the Pantry Pilot GitHub repository: 
[https://github.com/RobertMcIsaac/django_delights](https://github.com/RobertMcIsaac/django_delights)

## Visuals
Check out a live demonstration of Pantry Pilot on YouTube: 
[https://www.youtube.com/watch?v=7hXUfWyNPsY&t=35s&ab_channel=RobertMcIsaac](https://www.youtube.com/watch?v=7hXUfWyNPsY&t=35s&ab_channel=RobertMcIsaac)

---

### Original Codecademy project requirements:

You’ve been asked by a restaurant owner to build an application that will help keep track of how much food they have throughout the day. The 
owner starts the day with:

- An inventory of different Ingredients, their available quantity, and their prices per unit
- A list of the restaurant’s MenuItems, and the price set for each entry
- A list of the ingredients that each menu item requires (RecipeRequirements)
- A log of all Purchases made at the restaurant

Knowing that information, the restaurant, Django Delights’ owner has asked for the following features:

- They should be able to enter in new recipes along with their recipe requirements, and how much that menu item costs.
- They should also be able to add to the inventory a name of an ingredient, its price per unit, and how much of that item is available.
- They should be able to enter in a customer purchase of a menu item. When a customer purchases an item off the menu, the inventory should be 
modified to accommodate what happened, as well as recording the time that the purchase was made.

Here are some helpful tips to get you started thinking about the project: Your ingredients, recipes, and purchase data should be stored in a 
database, and should be rendered back to the Django views. Your Django backend should supply endpoints to create new recipes via a form 
submission, submit customer purchases from a different form, and get information about the total cost of inventory, the total revenue for the 
day, the different purchases that were made, and how much inventory is required to restock (as an initial example) to render them into a Django 
view.

### Project Requirements
- Build an inventory and sales application using Django
- Develop locally on your machine
- Version control your application with Git and host the repository on GitHub
- Use the command line to manage your application locally and test out queries
- Users can log in, log out, and must be logged in to see the views
- Users can create items for the menu
- Users can add ingredients to the restaurant’s inventory and update their quantities
- Users can add the different recipe requirements for each menu item
- Users can record purchases of menu items (only the ones that are able to be created with what’s in the inventory!)
- Users can view the current inventory, menu items, their ingredients, and a log of all purchases made

### Prerequisites:
- HTML
- CSS
- Python
- Django
- Git
- Command Line
