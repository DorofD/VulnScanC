from app.services.svacer.api import Svacer


def get_projects():
    svacer = Svacer()
    return svacer.get_projects()


def get_snapshots(project_id, branch_id):
    svacer = Svacer()
    snapshots = svacer.get_snapshots(project_id, branch_id)
    for snapshot in snapshots:
        try:
            del snapshot['details']
        except:
            continue
    return snapshots
