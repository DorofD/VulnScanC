from app.services.fstec.bdu_fstec import FSTEC


def update_bdu():
    fstec = FSTEC()
    fstec.update_bdu()
    return True


def update_vulns_by_cve_id():
    fstec = FSTEC()
    fstec.update_vulns('common')
    fstec.update_vulns('bitbake')
    return True


def get_bdu_info():
    fstec = FSTEC()
    return fstec.get_bdu_info()


def get_component_bdu_vulns(component_id: int, component_type: str):
    fstec = FSTEC()
    return fstec.get_component_bdu_vulns(component_id, component_type)
