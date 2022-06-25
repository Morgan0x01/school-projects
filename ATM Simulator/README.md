# CASH-OUT 🌚 ATM (Automated Teller Machine) simulator
![ATM](https://i.imgur.com/UKKtawK.png)

## Description
A CLI based database driven ATM simulator coded in Python.

### The DBMS used is Sqlite3
Sqlite3 is a lightweight Database system which handles the creation, storage and management of a lightweight relational Database (SQL) without the need for the installation of DB Software like MySQL or Postgresql.

Data is read and written directly to a lightweight file with the '.db' extension.

### Python has a built-in implementation of Sqlite3 as a module which can easily be imported with the following command:

```python
import sqlite3
```

### A Database connection can be initiated with the following example command:

```python
connection = sqlite3.connect('ATM.db')
```

### Dependency Installation:

```python
pip install -r requirements.txt
```

### Usage:

```python
python atm.py
```

### ATM Options
![ATM Options](https://i.imgur.com/I9vD9uu.png)

### The ATM Simulator simulates the following seamlessly:

- Withdrawals
- Transfers
- Balance retrieval
- Deposits
- PIN change
- Account management etc.

### Transfers Menu:

![ATM receiving accounts](https://gyazo.com/51629090306318cce22d7cdcb8413c68)

