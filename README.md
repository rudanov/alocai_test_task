# alocai_test_task
Test task for Intern Backed Developer

# Run service
```commandline
 docker build -t csv_transformator .
 docker run -dp 80:80 csv_transformator
```

# Run tests
Since it's not possible to use docker container as an interpreter in PyCharm CE, for local tests I used venv
```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest csv_transformator/test.py 
```

# Sample data errors
### 1) Rounding rules are inconsistent. I used round() and it made my output sample differ from the one in backend-intern.md for Fortnite in "Total Revenue"
### 2) "assasins" misspelling
### 3) "Assassin's creed" price value in input sample is wrong (should be as in output sample)