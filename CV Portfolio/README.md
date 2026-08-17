Hi, and welcome to my CV portfolio, intended to demonstrate my test automation capabilities.

In order to demonstrate this, I've put together a small flask-server e-commerce website upon which I can run automated tests, stored in the 'Tests' folder.

I've also created the run_tests.py file in order to demonstrate a small CI-CD pipeline example, in which the server is seeded and set up, automated tests run against it, and then ended.

Please note this is a work in progress, and any suggestions for inclusions that may build upon this portfolio are more than welcome!

### DISCLAIMER

The qa_ecommerce_demo folder was set up with the help of AI, as the intention of this portfolio was to demonstrate automation capabilities.

## Launch server

If you wish to to run the e-commerce site locally without the need to run automated tests on it, then from within a terminal, navigate into the qa_ecommerce_demo folder and run the following commands:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python run.py
```

This will run the server within the terminal. Then, to access the site, simply open http://localhost:5000.

Two demo accounts should be established in seed.py, details below:

- Username: `alice`
- Password: `Password123!`

- Username: `bob`
- Password: `Password123!`

## Automation Tests

To run the automation tests, you may either use run_tests.py to run all automation tests, or you can navigate into specific folders to run specific files, or test cases within the files.

If using run_tests.py, please make sure the server is not already active prior to executing the file.

If running a specific file or test case, you will need to run the server using the instructions above before these tests will work. Please note that some files include tests that run sequentially, and executing these tests out of order may cause them to fail.