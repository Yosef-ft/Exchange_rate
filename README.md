# Scraper for Ethiopian Bank Exchange Rates and WordPress Site Integration
### Overview
This project scrapes the exchange rates from all Ethiopian banks and saves the data to a MySQL database. The program then sends the results to a `WordPress` website or `Streamlit` site.

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
4. Create a databases in MySQL:
    - Call your database 'Exchange_Rates' 
5. In the pipeline.py file, configure your database connection details:
```
self.conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='Exchange_Rates'
)

```

## Configuring WordPress Integration
1. Create a local WordPress site on your development machine.
2. In the WP_api.py file, configure the WordPress site connection details:
``` 
def main():
    url = 'http://exchange-rates.local/wp-json/wp/v2'
    user = 'your_wordpress_username'
    password = 'your_wordpress_password' # Generated from Application Passwords plugin
    creds = user + ":" + password
    token = base64.b64encode(creds.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
```

- Make sure to replace 'your_wordpress_username' and 'your_wordpress_password' with your actual WordPress credentials. 
- Generating password refer `https://robingeuens.com/blog/python-wordpress-api/`

## Configuring Streamlit site
1. To run `streamlit.py` configure the database connection go to `streamlit.py`:
```
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'your_username',
            password = 'your_password',
            database = 'Exchange_Rates'
        )
 
```

## Running the Project
After completing the setup, you can start the project by running the spiders from the command line or run the python file RateScraper/RateScraper/spiders/__init__.py . The exchange rates will be saved to the local MySQL database, and by running the WP_api.py file; results will be sent to the configured WordPress site.

Enjoy!