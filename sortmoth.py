import pandas as pd
import numpy as np
import csv

#  -------------------
# Write a finction that will take in a CSV path and output a new CSV file
# with a stratified random dample of the original csv file. 
# Should return T/F ig the stratified csv file was successful. 
#
# The CSV file should have #successful Audiomoths * 24 clips. Each clip 
# should represent a different hour of the day. 
#     * Make sure the clips chosen are a minute long ( successful regordings)
#     * They are 46.1 megabytes for reference


# The first strata layer to be represented by each Audiomoth device
#  -  Make it so that IF audiomoth device has enough clips, it will be added to first strata
#  -  Audiomoth 21, 19, 8, 28 had problems

# Second strata layer to be represented by the hours in the day 
#     -  The CSV is in UTC , ( 0- 23)
#     - Approach: You can use pandas to find all the rows in the csv that are in a certain 
#                 hour, that are a minute long, and put those in a list. You can then randomly select
#                 a clip from that list. 
#  -------------------

def strataSort():
	df = pd.read_csv('Peru_2019_AudioMoth_Data_Full.csv')
	# Work on First Strata... 
	# Since there are close to 2852 clips from each device, we need to get a strata sample of 
	g = df[df.AudioMothCode != "AM-8"]
	column_csv = g.groupby('AudioMothCode',group_keys=False).apply(lambda x: x.sample())
	

	# Work on Second Strata... 

	print(column_csv)

strataSort()
