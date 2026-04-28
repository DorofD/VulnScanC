from app.pg_repository.queries.snapshots import DBSnapshots
from app.pg_repository.queries.components import DBComponents
from app.services.bitbake.bitbake_handler import BitbakeHandler


def get_project_snapshots(project_id):
    db_snapshots = DBSnapshots()
    db_components = DBComponents()
    snapshots = db_snapshots.get_project_snapshots(project_id)

    for snapshot in snapshots:
        if not snapshot['components']:
            snapshot['components'] = [
                {'path': 'Компоненты не обнаружены', 'status': 'Компоненты не обнаружены'}]
            continue
        component_ids_list = list(map(int, snapshot['components'].split(', ')))
        snapshot['components'] = []
        for id in component_ids_list:
            component = db_components.get_component(id)
            snapshot['components'].append(component[0])
    snapshots.reverse()
    return snapshots


def delete_snapshot(id):
    db_snapshots = DBSnapshots()
    db_snapshots.delete_snapshot(id)


def get_bitbake_project_snapshots(project_id):
    bb = BitbakeHandler()
    snapshots = bb.get_project_snapshots(project_id)
    return snapshots


def delete_bitbake_snapshot(snapshot_id):
    bb = BitbakeHandler()
    bb.delete_snapshot(snapshot_id)
    return True
