Automation-Schedule
===

# Motivation
Don't want to miss the movies released in Taiwan recently, so I want to send the movies that will be released next week by automated schedule web crawlers
# Demo
![image](https://github.com/DrDAN6770/Automation-Schedule/assets/118630187/a0036a92-2dc7-4bea-93fb-b541728df91f)
# Concept
![structure](https://github.com/DrDAN6770/Automation-Schedule/assets/118630187/960233e4-75d3-4b0a-856c-8c43c8f8028f)
1. Python compose crawler main file
2. Pandas processing crawler data to structured data
3. Mail the table via smtplib module
4. Using airflow on docker and setting the cycle duration (7 days)
5. Considering that the data is continuously updated, and I don't need to know the movies that have been released, I use mail to use the current week's data for a single time.
