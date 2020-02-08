# instagram_automation_tool

python tool that automates the Instagram follow/unfollow method visually. To gather followers,  
the tool uses a recursive algorithm to scrape followers from Instagrams website, follow them, and  
then unfollow them after a specified period of time. The overall goal is to create a net positive  
of followers

## Prerequisites

You must have google chrome installed on your system. The tool uses the chromium web driver

## Dependencies

Use pip to obtain all necessary dependencies for this project. Type the following command
```
pip install -r requirements.txt
```

## Usage

Just run automation.py and the GUI will take you through the rest of the settings
```
python3 automation.py
```

## The Settings

Once you run automation.py, a GUI will pop up with the following options  
  * Username: valid instagram username
  * Password: valid instagram password
  * Recursive Depth: the number of layers deep into followers to scrape
  * Recursive Layer: the length of the layer
  * Gather Count: number of followers to gather before starting following process
  * Runtime: number of hours for program to run
  * Actions each day: number of follow/unfollow actions to occur per 24 hours
  * Hours to unfollow: number of hours until unfollowing a followed user

## Author

  * **Nick Matthews** - (https://github.com/nickmatthews713)
