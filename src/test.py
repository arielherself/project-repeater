import pickle

def load_actions():
    with open('actions.pkl', 'rb') as f:
        return pickle.load(f)