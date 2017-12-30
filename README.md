
# Cloud Computing Application

Cloud computing has become more and more popular. There several different platforms out there, **Amazon, Google, Azure, Heroku** etc.

Since Amazon, Google all require credit card to use the free service, Heroku is chosen to test making a simple useful cloud application.

The application is a simple python flask website which provides lottery(marksix) numbers for picking options.

Content and logic of the web is not important. **Hope this is helpful for people who want to try out cloud applications.**

### Prerequisites

Python
Flask
Selenium
Phantomjs

## Steps

1. Register Heroku account, good thing about Heroku is credit card is not required
2. Install Heroku CLI, which can be downloaded from the official website. If you already installed git, you can uncheck it while installing.
3. Set up virtual environment using virtualenv. If you are not familiar with using virtualenv to build up flask website, please google about it first.
4. Create Procfile, do not make it as txt. Paste the content into the procfile: `web: gunicorn app:app`
5. Create requirements file: `pip freeze > requirements.txt`. In windows, the txt will be unicode format, use notepad to save as **ANSI** format, this is required by Heroku.
6. Use `heroku login` to login 
7. Use git to push your application to Heroku:
```
git init
git add --all
git commit -m "commit changes"
git push heroku master
```
8. You should see your application address after pushing, then you can visit the application via that address.

9. **extra tips: **since this application involves web scraping, headless explorer Phantomjs is used, you might need to add the buildpack to your heroku application: `heroku buildpacks:add https://github.com/stomita/heroku-buildpack-phantomjs` 

## License

GPL

## Acknowledgments

Many thanks to different online tutorials online about heroku applications.
