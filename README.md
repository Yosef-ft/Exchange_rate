# Scraper for Ethiopian Bank Exchange Rates and WordPress Site Integration
### Overview
This project scrapes the exchange rates from all Ethiopian banks and saves the data to a MySQL database. The program then sends the results to a WordPress website.

### Prerequisites
* MySQL server (version 8.0 or later)
* WordPress website (with the "Application Passwords" plugin installed)

### Installation and Setup
1. Clone the project repository:

```
git clone https://github.com/Yosef-ft/Exchange_rate.git
```
2. Install the required dependencies:
```
cd Exchange_rate
pip install -r requirements.txt
```
3. Download and install the latest MySQL server from the official website: MySQL Downloads <https://dev.mysql.com/downloads/mysql/>
4. Create two tables in your MySQL database:
    - FullRates
    - Rates
5. In the pipeline.py file, configure your database connection details:
```
self.conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='FullRates'
)

self.conn2 = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='Rates'
)
```

## Configuring WordPress Integration
1. Create a local WordPress site on your development machine.
2. In the WP_api.py file, configure the WordPress site connection details:
``` 
def main():
    url = 'http://exchange-rates.local/wp-json/wp/v2'
    user = 'your_wordpress_username'
    password = 'your_wordpress_password'
    creds = user + ":" + password
    token = base64.b64encode(creds.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
```

Make sure to replace 'your_wordpress_username' and 'your_wordpress_password' with your actual WordPress credentials.

## Running the Project
After completing the setup, you can start the project by running the spiders. The exchange rates will be saved to the MySQL database, and the results will be sent to the configured WordPress site.

Enjoy!