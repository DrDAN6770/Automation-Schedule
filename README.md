﻿Automation-Schedule
===

# Motivation
Don't want to miss the movies released in Taiwan recently, so I want to send the movies that will be released next week by automated schedule web crawlers
# Demo
![Demo](https://github.com/DrDAN6770/Automation-Schedule/assets/118630187/c8c65b67-e12a-4314-96fa-361cf63d0610)
# Concept
![structure](https://github.com/DrDAN6770/Automation-Schedule/assets/118630187/960233e4-75d3-4b0a-856c-8c43c8f8028f)
1. Python compose crawler main file
2. Pandas processing crawler data to structured data
3. Mail the table via smtplib module
4. Using airflow on docker and setting the cycle duration (7 days)
5. Considering that the data is continuously updated, and I don't need to know the movies that have been released, I use mail to use the current week's data for a single time.
