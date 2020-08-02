# Blinkist Book Scraper
### Python Script to fetch book summaries from [blinkist.com](https://www.blinkist.com/) with pdf output 

#### This script is part of my efforts of teaching myself how to code. It's solely for educational purposes!

#### What the script does, step-by-step:
1. Starts Selenium Firefox session, navigates and logs in to blinkist.com (needs manual reCaptcha resolution)
2. Either reads out books in personal library or acquires list of all books
3. Compares against files in directory and skips any file that has already been acquired. 
4. Scrapes books' meta data and summary content
5. Saves each to docx and converts to pdf

#### What you need to run the script: 
- Premium subscription with [blinkist.com](https://www.blinkist.com/)
- Only run and tested on Windows environment
- A number of libraries that can be found [here](https://github.com/LangeJM/Selenium_Blinkist/blob/master/requirements.txt)
- Selenium webdriver for Firefox, [Geckodriver](https://github.com/LangeJM/Selenium_Blinkist/blob/master/geckodriver.exe)

I am using Anaconda and installed the needed libraries one after another. 
Not sure if this works here, but usually you can install all packages with: 
```
conda install --file requirements.txt
```

main_blink.py imports modules from the other scripts as needed. Run main_blink.py with command line arguments for blinkist.com username and password (of course you can login manually as well, in which case no aditional arguments). 
Please note, you still have to manually solve the reCaptcha. This is something I haven't been able to solve by now.

```
python main_blink.py <username> <password>
```







