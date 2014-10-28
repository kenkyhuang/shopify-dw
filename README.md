<b>Overview</b>

This is a basic script to pull data from Shopify's API and push it into a local mySQL data warehouse. Tables include:

- Product
- SKU
- Order
- Order Line

<b>Installation</b>

Git clone the repository.

<pre><code>git clone git@github.com:kenkyhuang/shopify-dw.git</code></pre>

Assuming you have <a href='http://virtualenv.readthedocs.org/en/latest/virtualenv.html'>virtualenv</a> installed, install the necessary Python packages.

<pre><code>virtualenv env --no-site-packages
pip install -r requirements.txt
</code></pre>

Assuming you have <a href='https://rubygems.org/pages/download'>RubyGems</a> installed, install the shopify_api Ruby gem.

<pre><code>gem install shopify_api</code></pre>

Load the mySQL schema.

<pre><code>/usr/local/mysql/bin/mysql -u root shopify &lt; sql/schema.sql</code></pre>

Kick off the ETL script. This will:

- Pull from the Shopify API's Product and Order resources and write JSON data to the /json folder
- Transform JSON into flat text files and write these to the /import folder
- Import data into mySQL tables as defined in the schema

<pre><code>./run.sh</code></pre>

This script can be then scheduled via a cron job.

<pre><code>crontab -e</code></pre>



