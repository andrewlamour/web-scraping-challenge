{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies and Setup\n",
    "from bs4 import BeautifulSoup\n",
    "from splinter import Browser\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "\n",
    "\n",
    "# Set Executable Path & Initialize Chrome Browser\n",
    "executable_path = {\"executable_path\": \"/usr/local/bin/chromedriver\"}\n",
    "browser = Browser(\"chrome\", **executable_path, headless=False)\n",
    "\n",
    "# NASA Mars News Site Web Scraper\n",
    "def mars_news(browser):\n",
    "    # Visit the NASA Mars News Site\n",
    "    url = \"https://mars.nasa.gov/news/\"\n",
    "    browser.visit(url)\n",
    "\n",
    "\n",
    "    browser.is_element_present_by_css(\"ul.item_list li.slide\", wait_time=0.5)\n",
    "    \n",
    "    html = browser.html\n",
    "    news_soup = BeautifulSoup(html, \"html.parser\")\n",
    "\n",
    " \n",
    "    try:\n",
    "        slide_element = news_soup.select_one(\"ul.item_list li.slide\")\n",
    "        slide_element.find(\"div\", class_=\"content_title\")\n",
    "\n",
    "        # Scrape the Latest News Title\n",
    "        # Use Parent Element to Find First <a> Tag and Save it as news_title\n",
    "        news_title = slide_element.find(\"div\", class_=\"content_title\").get_text()\n",
    "\n",
    "        news_paragraph = slide_element.find(\"div\", class_=\"article_teaser_body\").get_text()\n",
    "    except AttributeError:\n",
    "        return None, None\n",
    "    return news_title, news_paragraph\n",
    "\n",
    "\n",
    "\n",
    "# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper\n",
    "def featured_image(browser):\n",
    "    # Visit the NASA JPL (Jet Propulsion Laboratory) Site\n",
    "    url = \"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars\"\n",
    "    browser.visit(url)\n",
    "\n",
    "    # Ask Splinter to Go to Site and Click Button with Class Name full_image\n",
    "    # <button class=\"full_image\">Full Image</button>\n",
    "    full_image_button = browser.find_by_id(\"full_image\")\n",
    "    full_image_button.click()\n",
    "\n",
    "    # Find \"More Info\" Button and Click It\n",
    "    browser.is_element_present_by_text(\"more info\", wait_time=1)\n",
    "    more_info_element = browser.find_link_by_partial_text(\"more info\")\n",
    "    more_info_element.click()\n",
    "\n",
    "    # Parse Results HTML with BeautifulSoup\n",
    "    html = browser.html\n",
    "    image_soup = BeautifulSoup(html, \"html.parser\")\n",
    "\n",
    "    img = image_soup.select_one(\"figure.lede a img\")\n",
    "    try:\n",
    "        img_url = img.get(\"src\")\n",
    "    except AttributeError:\n",
    "        return None \n",
    "   # Use Base URL to Create Absolute URL\n",
    "    img_url = f\"https://www.jpl.nasa.gov{img_url}\"\n",
    "    return img_url\n",
    "\n",
    "# Mars Weather Twitter Account Web Scraper\n",
    "def twitter_weather(browser):\n",
    "    # Visit the Mars Weather Twitter Account\n",
    "    url = \"https://twitter.com/marswxreport?lang=en\"\n",
    "    browser.visit(url)\n",
    "    \n",
    "    # Parse Results HTML with BeautifulSoup\n",
    "    html = browser.html\n",
    "    weather_soup = BeautifulSoup(html, \"html.parser\")\n",
    "    \n",
    "    # Find a Tweet with the data-name `Mars Weather`\n",
    "    mars_weather_tweet = weather_soup.find(\"div\", \n",
    "                                       attrs={\n",
    "                                           \"class\": \"tweet\", \n",
    "                                            \"data-name\": \"Mars Weather\"\n",
    "                                        })\n",
    "   # Search Within Tweet for <p> Tag Containing Tweet Text\n",
    "    mars_weather = mars_weather_tweet.find(\"p\", \"tweet-text\").get_text()\n",
    "    return mars_weather\n",
    "\n",
    "\n",
    "# Mars Facts Web Scraper\n",
    "def mars_facts():\n",
    "    # Visit the Mars Facts Site Using Pandas to Read\n",
    "    try:\n",
    "        df = pd.read_html(\"https://space-facts.com/mars/\")[0]\n",
    "    except BaseException:\n",
    "        return None\n",
    "    df.columns=[\"Description\", \"Value\"]\n",
    "    df.set_index(\"Description\", inplace=True)\n",
    "\n",
    "    return df.to_html(classes=\"table table-striped\")\n",
    "\n",
    "# Mars Hemispheres Web Scraper\n",
    "def hemisphere(browser):\n",
    "    # Visit the USGS Astrogeology Science Center Site\n",
    "    url = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "    browser.visit(url)\n",
    "\n",
    "    hemisphere_image_urls = []\n",
    "\n",
    "    # Get a List of All the Hemisphere\n",
    "    links = browser.find_by_css(\"a.product-item h3\")\n",
    "    for item in range(len(links)):\n",
    "        hemisphere = {}\n",
    "        \n",
    "        # Find Element on Each Loop to Avoid a Stale Element Exception\n",
    "        browser.find_by_css(\"a.product-item h3\")[item].click()\n",
    "        \n",
    "        # Find Sample Image Anchor Tag & Extract <href>\n",
    "        sample_element = browser.find_link_by_text(\"Sample\").first\n",
    "        hemisphere[\"img_url\"] = sample_element[\"href\"]\n",
    "        \n",
    "        # Get Hemisphere Title\n",
    "        hemisphere[\"title\"] = browser.find_by_css(\"h2.title\").text\n",
    "        \n",
    "        # Append Hemisphere Object to List\n",
    "        hemisphere_image_urls.append(hemisphere)\n",
    "        \n",
    "        # Navigate Backwards\n",
    "        browser.back()\n",
    "    return hemisphere_image_urls\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "def scrape_all():\n",
    "    executable_path = {\"executable_path\": \"/usr/local/bin/chromedriver\"}\n",
    "    browser = Browser(\"chrome\", **executable_path, headless=False)\n",
    "    news_title, news_paragraph = mars_news(browser)\n",
    "    img_url = featured_image(browser)\n",
    "    mars_weather = twitter_weather(browser)\n",
    "    facts = mars_facts()\n",
    "    hemisphere_image_urls = hemisphere(browser)\n",
    "    timestamp = dt.datetime.now()\n",
    "\n",
    "    data = {\n",
    "        \"news_title\": news_title,\n",
    "        \"news_paragraph\": news_paragraph,\n",
    "        \"featured_image\": img_url,\n",
    "        \"weather\": mars_weather,\n",
    "        \"facts\": facts,\n",
    "        \"hemispheres\": hemisphere_image_urls,\n",
    "        \"last_modified\": timestamp\n",
    "    }\n",
    "    browser.quit()\n",
    "    return data \n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    print(scrape_all())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
