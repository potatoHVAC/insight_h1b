# H1B Immigration Trends Analysis

By Daniel Speer

A project for the Insight Data Science boot camp application.

# Problem

To clean and analyze the US Department of Labor’s Office of Foreign Labor Certification performance data. The analysis will output the top 10 occupations and the top 10 states for certified visa applications. 

# Approach

#### Data Cleaning Assumptions:
* SOC numbers with a decimal are subsets of their XX-XXX position and counted as the 


# Run Instructions

Placer input CSV file in the `./input/` directory. CSV must use `;` as delimiter. 

The appropriate columns will be automatically collected if the following strings are included in the header. 

1. Status        => 'STATUS'
2. SOC        => 'SOC_CODE'
3. Job name    => 'SOC_NAME'
4. State        => 'WORKSITE_STATE' or 'WORKLOC1_STATE'

# Output Information

Two CSV files will be created/overwritten in the `./output/` folder.
 
* `./output/top_10_occupations.txt`
* `./output/top_10_states.txt`

# Example

Given the input file, `./input/file_name.csv` with the following data:
```
id;CASE_STATUS;YEAR_SOC;YEAR_SOC_NAME;WORKSITE_STATE
1;CERTIFIED;11-1234;DOG WALKER;WA
2;CERTIFIED;22-1234;PIRATE;CA
3;CERTIFIED;33-3333;NINJA;CA
4;CERTIFIED;11-1234;DOG WALKER;CA
```

Then the output files will be:

`./output/top_10_occupations.txt`:
```
TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
DOG WALKER;2;50.0%
NINJA;1;25.0%
PIRATE;1;25.0%
```
`./output/top_10_states.txt`:
```
TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
CA;3;75.0%
WA;1;25
```
# Future Improvements

* Implement threading for the data collection to allow for files larger than the available memory.
* Both of the sorting methods are almost identical. Candidate for refactoring to follow DRY practices.

