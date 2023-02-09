# saner-connectathon-01-23
Files for testing the SANER IG at the HL7 Connectathon

Set up "development" config

   - Local git checkout mounted over git checkout built into container (for hot-reloading)
   - Invoke scripts via: dc run etl $SCRIPT_FILE eg dc run etl tabulateMeasureReport.py
   - Run dc build anytime requirements.txt is updated
