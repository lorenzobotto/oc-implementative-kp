# oc-implementative-kp
Implementative thesis of OC - Unito 2023

This project aims to implement the Knapsack Problem (KP) using a modern architecture that combines a React frontend with a Django backend. Three different algorithms have been implemented to solve the problem:

- Recursion DP1: A recursive approach with memoization to avoid redundant calculations.
- Iterative DP1: An iterative dynamic programming approach that uses a 2D array to store results of subproblems.
- Iterative DP2: A space-optimized iterative approach that uses a 1D array to store results, reducing memory usage.

## How to run

### Backend
Install the necessary packages in your environment:
```
cd backend/
pip install -r requirements.txt
```

Run the following command to run the django server:
```
python manage.py runserver
```

### Frontend
Install the necessary packages:
```
cd frontend/
npm install
```

Run the following command to run the django server:
```
npm start
```