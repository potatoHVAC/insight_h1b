# H1B Immigration trends analysis
By Daniel Speer
A project for the Insight Data Science boot camp application.

# Problem
To automatically clean

# Data Cleaning and Analysis Assumptions

# Run Instructions
Placer input CSV file in the `./input/` directory. CSV must use `;` as delimiter. 

The appropriate columns will be automatically collected if the following strings are included in the header. 

1. Status    => 'STATUS'
2. SOC       => 'SOC_CODE'
3. Job name  => 'SOC_NAME'
4. State     => 'WORKSITE_STATE' or 'WORKLOC1_STATE'



# Output Information



# Example
Given the input file, `./input/file_name.csv` with the following data:

```
;CASE_STATUS;YEAR_SOC;YEAR_SOC_NAME;WORKSITE_STATE
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
