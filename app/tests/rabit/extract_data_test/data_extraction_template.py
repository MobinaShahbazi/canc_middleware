
# Steps for extracting data from any database and loading into SWH

# Fetch data source configurations
# Set queries for extracting data
# Set metadata generation

from app.crud import workspaces_crud

# Configure a new workspace

ws = {
    'name': 'sjs_sr_ops',
    'description': 'SJS Search and Rescue Operations',
    'meta': {},
    'comp_meta': {}
}

workspaces_crud.create(obj_in=ws)
