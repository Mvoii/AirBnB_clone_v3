#!/usr/bin/python3
"""test .get() and .count() methods"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.all()))
print("All State objects: {}".format(storage.all(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First State object: {}".format(storage.get(State, first_state_id)))
