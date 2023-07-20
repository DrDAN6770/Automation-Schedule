Automation-Schedule
===

# Motivation
Don't want to miss the movies released in Taiwan recently, so I want to send the movies that will be released next week by automated schedule web crawlers
# Demo
![image](https://github.com/DrDAN6770/Automation-Schedule/assets/118630187/a0036a92-2dc7-4bea-93fb-b541728df91f)

![image](https://github.com/DrDAN6770/Automation-Schedule/assets/118630187/c8ac6f58-15a5-4c4a-89ea-8e0c374034c2)
# Concept
![image](https://github.com/DrDAN6770/Automation-Schedule/assets/118630187/29e406a8-8531-40ad-a585-3fc8417ab8d9)
1. Python compose crawler main file
2. Pandas processing crawler data to structured data
3. Mail the table via smtplib module
4. Using airflow on docker and setting the cycle duration (7 days)
5. Transformed workflow into the cloud processing through Google Cloud Platform composer
6. Considering that the data is continuously updated, and I don't need to know the movies that have been released, I use mail to use the current week's data for a single time.
