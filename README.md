Course predictor for CCIS
Usage: run.py [options]

Options:
  -h, --help            show this help message and exit
  -r, --restrict        Restrict predictions to courses available for the
                        semester.[Optional]
  -s CUR_SEM, --sem=CUR_SEM
                        semester to predict over.
  -p PROGRAM, --program=PROGRAM
                        programs to predict over. They should be comma
                        seperated single string, no extra spaces
                        'MSCS Computer Science' is the default
                        program.[Optional]
  -l LEVEL, --level=LEVEL
                        Student level to predict over. Either 'UG' or 'GR'.
                        'GR' is the default level[Optional]
  -m MIN_SUP, --minsup=MIN_SUP
                        The minimum support to consider for Frequent Patters.
                        0.3 is the default value for grads and 5.0 for
                        undergrads.[Optional]
Examples:-

