# Blinkist Book Scraper
### Python Script to fetch book summaries from [blinkist.com](https://www.blinkist.com/) with pdf output 

#### Steps:
1. Start Selenium Firefox session, navigate and log in to blinkist.com (needs manual reCaptcha resolution)
2. Either read out books in personal library or get list of all books
3. Compare against files in directory and skip any file that has already been acquired. 
4. Scrape books meta data and summary content
5. Save each to docx and convert to pdf


#### Requirements:
- Premium subscription with [blinkist.com](https://www.blinkist.com/)
- A number of libraries that can be found [here](https://github.com/LangeJM/Selenium_Blinkist/blob/master/requirements.txt)
- Selenium webdriver [Geckodriver](https://github.com/LangeJM/Selenium_Blinkist/blob/master/geckodriver.exe)
- Probably only works on Windows machines
