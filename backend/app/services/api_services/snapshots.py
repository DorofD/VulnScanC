from app.repository.queries.snapshots import get_project_snapshots as get_project_snapshots_db
from app.repository.queries.snapshots import delete_snapshot as delete_snapshot_db
from app.repository.queries.components import get_component as get_component_db
from app.services.bitbake.bitbake_handler import BitbakeHandler


def get_project_snapshots(project_id):

    snapshots = get_project_snapshots_db(project_id)

    for snapshot in snapshots:
        if not snapshot['components']:
            snapshot['components'] = [
                {'path': 'Компоненты не обнаружены', 'status': 'Компоненты не обнаружены'}]
            continue
        component_ids_list = list(map(int, snapshot['components'].split(', ')))
        snapshot['components'] = []
        for id in component_ids_list:
            component = get_component_db(id)
            snapshot['components'].append(component[0])
    snapshots.reverse()
    return snapshots


def delete_snapshot(id):
    delete_snapshot_db(id)


def get_bitbake_project_snapshots(project_id):
    bb = BitbakeHandler()
    snapshots = bb.get_project_snapshots(project_id)
    return snapshots


def delete_bitbake_snapshot(snapshot_id):
    bb = BitbakeHandler()
    bb.delete_snapshot(snapshot_id)
    return True
