# AN APPLICATION OF BENFORD'S LAW USING PYTHON

The basics here are taken from Lee Vaughan's excllent book `Impractical Python`. It allows for a Benford analysis of numbers in a pre-wrangled `.txt` file. I've already uploaded a bunch of samples - mostly, state vote counts broken down by county (or parish in LA). 


### DISCLAIMER 

THERE IS NO EVIDENCE OF FRAUD IN THE 2020 ELECTION - but you are welcome to try to find it!

### My Own Extension

I've extended it (badly) with second digit analysis, to try and get around the leading digit clustering that occurs when precincts have roughly equal populations, and the candidate’s support is at the same level in each precinct.
