## Movie Describer

This is a simple portfolio application utilizing Django.

## Installation

1. Get pip: https://pip.pypa.io/en/stable/installing/

2. Get `docker-compose`:
```
pip install docker-compose
```

3. Clone the repo:
```
git clone https://github.com/Coolthulhu/moviedescriber.git
```

4. Set environmental variables:
```
export OMDB_API_KEY=[your omdb api key here]
export SECRET_KEY=[your secret key here]
```

5. Run:
```
cd moviedescriber
docker-compose up
```

6. Open `http://127.0.0.1:8000` in browser
