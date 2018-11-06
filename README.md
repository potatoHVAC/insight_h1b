# H1B Immigration Trends Analysis

By Daniel Speer

A project for the Insight Data Science boot camp application.

# Problem

The US Department of Labor provides raw performance data for its Office of Foreign Labor Certification. The data needs to be cleaned and analyzed to find the top 10 certified jobs and the top 10 states where those jobs are performed. 

# Approach

1. Open target input file
2. Clean the data as each row is checked.
3. Collect the relevant data for certified applications that have valid data.
4. Run analysis on the collected data.
5. Save outputs to their respective files.

#### Data Cleaning Assumptions:
* SOC numbers with a decimal are subsets of their XX-XXX position and counted as the base job
* Certifications with SOC numbers that are too short or too long are rejected entirely.
* Certifications missing a job name but include a valid SOC number are not rejected from the count. If a second job is found with a matching SOC number then its job title will update the collected data point. 
* Certifications missing a proper state code are rejected entirely.
* Jobs with different SOC numbers but the same title are treated as separate jobs. 
* Certifications are only accepted if the status is ‘CERTIFIED’ - no cleaning was applied to this section.

# Run Instructions

Place input CSV file in the `./input/` directory. CSV must use `;` as delimiter. 

The appropriate columns will be automatically collected if the following strings are included in the header. 

1. Status        => 'STATUS'
2. SOC        => 'SOC_CODE'
3. Job name    => 'SOC_NAME'
4. State        => 'WORKSITE_STATE' or 'WORKLOC1_STATE'

# Output Information

Two CSV files will be created in the `./output/` folder.
 
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

The output files will be:

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

* Implement streaming for the data collection to allow for files larger than the available memory.
* Both of the sorting methods are almost identical. Candidate for refactoring to follow DRY practices.
* Use time stamps and input file names to automatically name output files to prevent accidental overriding and to allow for batch file analysis. 
