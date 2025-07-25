import React, { version } from "react";
import { useState, useEffect, useContext } from "react";
import "./Snapshots.css";
import Button from "../Button/Button";
import { apiGetProjects } from "../../services/apiProjects";
import { apiGetProjectSnapshots, apiDeleteSnapshot } from "../../services/apiSnapshots";
import { apiGetOsvReport, apiGetBduReport, apiGetBitbakeBduReport, apiGetBitbakeReport } from "../../services/apiReports";
import ProjectCard from "../Projects/ProjectCard/ProjectCard";
import SnapshotCard from "./SnapshotCard/SnapshotCard";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import filterLogo from './filter.png'
import Loader from "../Loader/Loader";
import { apiGetBitbakeProjects } from "../../services/apiBitbake";

export default function Snapshots() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
    const [loaderActive, setLoaderActive] = useState(false)

    const [loadingProjects, setLoadingProjects] = useState('loaded')
    const [projects, setProjects] = useState([])
    const [pickedProject, setPickedProject] = useState({ id: '', name: '' })

    const [projectType, setProjectType] = useState('')

    const [loadingSnapshots, setLoadingSnapshots] = useState('loading')
    const [snapshots, setSnapshots] = useState([])
    const [pickedSnapshot, setPickedSnapshot] = useState({ id: '0' })

    const [selectedSeverities, setSelectedSeverities] = useState([]);
    const [selectedLayers, setSelectedLayers] = useState([]);


    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);


    const [actionFunction, setActionFunction] = useState(null);

    const [filterSnapshots, setFilterSnapshots] = useState({ datetime: '' });
    const [showHint, setShowHint] = useState(false);

    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    function closeChangeModal() {
        setIsChangeModalOpen(false);
    }

    function closeAcceptModal() {
        setIsAcceptModalOpen(false);
    }

    async function getProjects(projectType) {
        try {
            if (projectType == 'common') {
                setLoadingProjects('loading')
                const projects = await apiGetProjects()
                setProjects(projects)
                setPickedProject({ id: '', name: '' })
                setPickedSnapshot({ id: '0' })
                setSnapshots([])
                setLoadingProjects('loaded')
            } else if (projectType == 'bitbake') {
                setLoadingProjects('loading')
                const projects = await apiGetBitbakeProjects()
                setProjects(projects)
                setPickedProject({ id: '', name: '' })
                setPickedSnapshot({ id: '0' })
                setSnapshots([])
                setLoadingProjects('loaded')
            }
        } catch (err) {
            setLoadingProjects('error')
        }
    }

    async function getProjectSnapshots(id) {
        try {
            setLoadingSnapshots('loading')
            const snapshots = await apiGetProjectSnapshots(projectType, id)

            const order = { 'none': 0, 'confirmed': 1, 'denied': 2 };

            snapshots.forEach(element => {
                element.components.sort((a, b) => {
                    return order[a.status] - order[b.status];
                });
            });
            setSnapshots(snapshots)
            setLoadingSnapshots('loaded')
        } catch (err) {
            setSnapshots([])
            setLoadingSnapshots('error')
        }
    }

    async function deleteSnapshot() {
        try {
            const response = await apiDeleteSnapshot(projectType, pickedSnapshot.id)
            if (response.status == 200) {
                getProjectSnapshots(pickedProject.id)
                setPickedSnapshot([])
                setNotificationData({ message: 'Снапшот удален', type: 'success' })
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()

            } else {
                setNotificationData({ message: 'Не удалось удалить снапшот', type: 'error' })
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()
            }
        } catch (err) {
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
        }
    }



    const handleCheckboxChange = (item) => {
        setSelectedSeverities((prevSelectedItems) =>
            prevSelectedItems.includes(item)
                ? prevSelectedItems.filter((i) => i !== item)
                : [...prevSelectedItems, item]
        );
    };

    const handleLayerCheckboxChange = (item) => {
        setSelectedLayers((prevSelectedItems) =>
            prevSelectedItems.includes(item)
                ? prevSelectedItems.filter((i) => i !== item)
                : [...prevSelectedItems, item]
        );
    };

    async function getOsvReport() {
        try {
            if (selectedSeverities.length === 0) {
                setNotificationData({ message: 'Выберете severity', type: 'error' })
                toggleNotificationFunc()
                return false
            }
            const report = await apiGetOsvReport(pickedSnapshot.id, selectedSeverities, pickedProject.name, pickedSnapshot.datetime)
            closeChangeModal()
            setPickedSnapshot('')
            setSelectedSeverities([])
        } catch (err) {
            setSnapshots([])
            setSelectedSeverities([])
            setNotificationData({ message: 'Не удалось загрузить отчет', type: 'error' })
            toggleNotificationFunc()
        }
    }

    async function getBduReport() {
        try {
            if (selectedSeverities.length === 0) {
                setNotificationData({ message: 'Выберете severity', type: 'error' })
                toggleNotificationFunc()
                return false
            }
            const report = await apiGetBduReport(pickedSnapshot.id, selectedSeverities, pickedProject.name, pickedSnapshot.datetime)
            closeChangeModal()
            setPickedSnapshot('')
            setSelectedSeverities([])
        } catch (err) {
            setSnapshots([])
            setSelectedSeverities([])
            setNotificationData({ message: 'Не удалось загрузить отчет', type: 'error' })
            toggleNotificationFunc()
        }
    }

    async function getBitbakeReport() {
        try {
            if (selectedLayers.length === 0) {
                setNotificationData({ message: 'Выберете минимум один слой', type: 'error' })
                toggleNotificationFunc()
                return false
            }
            if (selectedSeverities.length === 0) {
                setNotificationData({ message: 'Выберете severity', type: 'error' })
                toggleNotificationFunc()
                return false
            }
            const report = await apiGetBitbakeReport(pickedSnapshot.id, selectedSeverities, selectedLayers, pickedProject.name, pickedSnapshot.datetime)
            closeChangeModal()
            setPickedSnapshot('')
            setSelectedSeverities([])
            setSelectedLayers([])
        } catch (err) {
            setSnapshots([])
            setSelectedSeverities([])
            setSelectedLayers([])
            setNotificationData({ message: 'Не удалось загрузить отчет', type: 'error' })
            toggleNotificationFunc()
        }
    }

    async function getBitbakeBduReport() {
        try {
            if (selectedLayers.length === 0) {
                setNotificationData({ message: 'Выберете минимум один слой', type: 'error' })
                toggleNotificationFunc()
                return false
            }
            if (selectedSeverities.length === 0) {
                setNotificationData({ message: 'Выберете severity', type: 'error' })
                toggleNotificationFunc()
                return false
            }
            const report = await apiGetBitbakeBduReport(pickedSnapshot.id, selectedSeverities, selectedLayers, pickedProject.name, pickedSnapshot.datetime)
            closeChangeModal()
            setPickedSnapshot('')
            setSelectedSeverities([])
            setSelectedLayers([])
        } catch (err) {
            setSnapshots([])
            setSelectedSeverities([])
            setSelectedLayers([])
            setNotificationData({ message: 'Не удалось загрузить отчет', type: 'error' })
            toggleNotificationFunc()
        }
    }

    const filteredSnapshots = snapshots.filter(item => {
        return (
            (filterSnapshots.datetime === '' || item.datetime.includes(filterSnapshots.datetime))
        );
    }
    )

    // useEffect(() => {
    //     getProjects()
    // }, [])


    return (
        <>
            <div className="snapshotsProjects">
                <div className="projectTypeButtons">
                    <button
                        onClick={() => { setProjects([]); setProjectType('common'), getProjects('common') }}
                        className={projectType == 'common' ? "snapshotsProjectTypeActive" : "snapshotsProjectType"}>
                        Обычные проекты
                    </button>
                    <button onClick={() => { setProjects([]); setProjectType('bitbake'), getProjects('bitbake') }}
                        className={projectType == 'bitbake' ? "snapshotsProjectTypeActive" : "snapshotsProjectType"}>
                        Проекты Bitbake
                    </button>
                </div>

                <p>Проекты</p>
                {loadingProjects === 'loading' && <Loader />}
                {loadingProjects === 'error' && <p> бекенд отвалился</p>}
                {loadingProjects === 'loaded' && <>
                    {projects.map(project =>
                        <ProjectCard id={project.id}
                            name={project.name}
                            picked={pickedProject.id === project.id && true || false}
                            onClick={() => { setPickedProject(project); getProjectSnapshots(project.id) }}>
                        </ProjectCard>)}
                </>}
            </div>

            <div className="snapshotsComponents">
                <p>Снапшоты</p>
                <div >
                    <img src={filterLogo} alt="" className="filterLogo" />
                    <input type="text" className="snapshotFilter" placeholder="Время создания" onChange={e => setFilterSnapshots({ ...filterSnapshots, datetime: e.target.value })} value={filterSnapshots.datetime} />
                    <button onClick={() => setFilterSnapshots({ datetime: '' })} className="clearFilter">Очистить</button>
                </div>
                {pickedProject.id === '' && <p> Выберете проект</p>}
                {pickedProject.id !== '' && loadingSnapshots === 'loading' && <Loader />}
                {loadingSnapshots === 'error' && <p> бекенд отвалился</p>}
                {loadingSnapshots === 'loaded' && <>
                    {snapshots.length === 0 && loadingSnapshots === 'loaded' && <p> Снапшоты не найдены</p>}
                    {filteredSnapshots.map(snapshot =>
                        <SnapshotCard id={snapshot.id}
                            datetime={snapshot.datetime}
                            picked={pickedSnapshot.id === snapshot.id && true || false}
                            onClick={() => { setPickedSnapshot(snapshot); setIsChangeModalOpen(true) }}>
                        </SnapshotCard>)
                    }
                </>}

                <Modal isOpen={isChangeModalOpen} onClose={closeChangeModal}>

                    {pickedSnapshot && projectType == 'common' &&
                        <div className="snapshotModal">
                            <div className="snapshotModalInfo">
                                <div className="snapshotModalNoteLabel"> Информация о снапшоте</div>
                                <p> <b>Проект: </b>{pickedProject.name}</p>
                                <p> <b>Время создания: </b>{pickedSnapshot.datetime}</p>
                                {pickedSnapshot.components &&
                                    <p><b>Компоненты: </b>{pickedSnapshot.components.map(component =>
                                        <>
                                            <br />
                                            Название: {component.address} <br />
                                            Статус: {component.status}<br />
                                        </>)}</p>
                                    || <p><b>Компоненты: </b>Не найдено</p>
                                }
                            </div>

                            <div className="snapshotReport">
                                <div className="snapshotModalNoteLabel"> Создание отчета
                                    <button
                                        onClick={() => {
                                            setShowHint((prev) => !prev);
                                        }}
                                        className={showHint ? "showHintActivated" : "showHint"}
                                    >
                                        ?
                                    </button>
                                </div>
                                {showHint &&
                                    <div className="hintBox">
                                        <p>
                                            В отчет попадут только компоненты со статусом confirmed
                                        </p>
                                        <p>
                                            В отчет не попадут компоненты без уязвимостей
                                        </p>
                                    </div>
                                }
                                <div className="snapshotModalNote"> Выберите уровни критичности уязвимостей, которые попадут в отчет:</div>
                                <div className="snapshotCheckboxes">
                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Critical')}
                                            onChange={() => handleCheckboxChange('Critical')}
                                        />
                                        Critical
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('High')}
                                            onChange={() => handleCheckboxChange('High')}
                                        />
                                        High
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Medium')}
                                            onChange={() => handleCheckboxChange('Medium')}
                                        />
                                        Medium
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Low')}
                                            onChange={() => handleCheckboxChange('Low')}
                                        />
                                        Low
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Without')}
                                            onChange={() => handleCheckboxChange('Without')}
                                        />
                                        Without
                                    </label>
                                </div>
                                <div className="snapshotModalButtons">
                                    <Button style={"componentVulnerabilities"} onClick={() => getOsvReport()}> Создать отчет OSV </Button>
                                    <Button style={"componentVulnerabilities"} onClick={() => getBduReport()}> Создать отчет БДУ </Button>

                                </div>
                                {/* <div className="snapshotModalNote"> *в отчет попадут только компоненты со статусом confirmed</div>
                                <div className="snapshotModalNote"> *в отчет не попадут компоненты без уязвимостей</div> */}
                            </div>

                            <div className="snapshotModalButtons">
                                <Button style={"projectReject"} onClick={() => openAcceptModalWithAction(deleteSnapshot)}> Удалить </Button>
                                <Button style={"projectClose"} onClick={() => { setSelectedSeverities([]); setPickedSnapshot(''); closeChangeModal() }}> Закрыть </Button>
                            </div>
                        </div>
                    }
                    {pickedSnapshot && projectType == 'bitbake' &&
                        <div className="bitbakeSnapshotModal">
                            <div className="bitbakeSnapshotModalInfo">
                                <div className="snapshotModalNoteLabel"> Информация о снапшоте</div>
                                <p> <b>Проект: </b>{pickedProject.name}</p>
                                <p> <b>Время создания: </b>{pickedSnapshot.datetime}</p>
                                {pickedSnapshot.components &&
                                    <p><b>Компоненты: </b>{pickedSnapshot.components.map(component =>
                                        <>
                                            <br />
                                            Название: {component.name} <br />
                                            Версия: {component.version}<br />
                                            Слой: {component.layer}<br />
                                        </>)}</p>
                                    || <p><b>Компоненты: </b>Не найдено</p>
                                }
                            </div>

                            <div className="bitbakeSnapshotReport">
                                <div className="snapshotModalNoteLabel"> Создание отчета
                                    <button
                                        onClick={() => {
                                            setShowHint((prev) => !prev);
                                        }}
                                        className={showHint ? "showHintActivated" : "showHint"}
                                    >
                                        ?
                                    </button>
                                </div>
                                {showHint &&
                                    <div className="hintBox">
                                        <p>
                                            В отчёт попадут только компоненты из выбранных слоёв
                                        </p>
                                        <p>
                                            В отчёт попадут только уязвимости с выбранными уровнями критичности и статусом Unpatched
                                        </p>
                                        <p>
                                            Компонент не попадёт в отчёт, если у него нет Unpatched уязвимостей, либо выбранные уровни критичности имеют только уязвимости со статусом Patched
                                        </p>
                                    </div>
                                }
                                {pickedProject.layers && <>
                                    Выберете слои, которые попадут в отчёт:
                                    <div className="snapshotCheckboxes">
                                        {pickedProject.layers.map(layer =>
                                            <>

                                                <label>
                                                    <input
                                                        type="checkbox"
                                                        checked={selectedLayers.includes(layer)}
                                                        onChange={() => handleLayerCheckboxChange(layer)}
                                                    />
                                                    {layer}
                                                </label>
                                            </>)}
                                    </div>
                                </> || <p>Слои не найдены</p>}


                                <br />
                                <div className="snapshotModalNote"> Выберите уровни критичности уязвимостей, которые попадут в отчет:</div>
                                <div className="snapshotCheckboxes">
                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Critical')}
                                            onChange={() => handleCheckboxChange('Critical')}
                                        />
                                        Critical
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('High')}
                                            onChange={() => handleCheckboxChange('High')}
                                        />
                                        High
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Medium')}
                                            onChange={() => handleCheckboxChange('Medium')}
                                        />
                                        Medium
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Low')}
                                            onChange={() => handleCheckboxChange('Low')}
                                        />
                                        Low
                                    </label>

                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('None')}
                                            onChange={() => handleCheckboxChange('None')}
                                        />
                                        None
                                    </label>
                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={selectedSeverities.includes('Unknown')}
                                            onChange={() => handleCheckboxChange('Unknown')}
                                        />
                                        Unknown
                                    </label>
                                </div>
                                <div className="snapshotModalButtons">
                                    <Button style={"componentVulnerabilities"} onClick={() => getBitbakeReport()}> Создать отчет CVE </Button>
                                    <Button style={"componentVulnerabilities"} onClick={() => getBitbakeBduReport()}> Создать отчет БДУ </Button>

                                </div>
                            </div>

                            <div className="snapshotModalButtons">
                                <Button style={"projectReject"} onClick={() => openAcceptModalWithAction(deleteSnapshot)}> Удалить </Button>
                                <Button style={"projectClose"} onClick={() => { setSelectedSeverities([]); setPickedSnapshot(''); closeChangeModal() }}> Закрыть </Button>
                            </div>
                        </div>
                    }
                </Modal>

                <AcceptModal isOpen={isAcceptModalOpen} onClose={closeAcceptModal}>
                    <div className="acceptModalProjects">
                        <div className="acceptModalProjectsText">
                            Вы уверены?
                        </div>
                        <div className="acceptModalProjectsButtons">
                            <Button style={"projectAccept"} onClick={() => { actionFunction(); closeAcceptModal(); }}> Да </Button>
                            <Button style={"projectReject"} onClick={closeAcceptModal}> Нет </Button>
                        </div>
                    </div>
                </AcceptModal>
            </div>
        </>
    );
}
