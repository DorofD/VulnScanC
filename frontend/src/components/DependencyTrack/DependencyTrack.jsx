import React from "react";
import { useState, useEffect } from "react";
import "./DependencyTrack.css";
import Button from "../Button/Button";
import { apiGetProjects, apiGetComponents } from "../../services/apiDependencyTrack";
import { apiGetDependencyTrackReport } from "../../services/apiReports";
import ProjectCard from "../Projects/ProjectCard/ProjectCard";
import ComponentCard from "./ComponentCard/ComponentCard";
import VulnerabilityCard from "./VulnerabilityCard/VulnerabilityCard";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import Modal from "../Modal/Modal";
import filterLogo from './filter.png'
import Loader from "../Loader/Loader";

export default function Components() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
    const [loaderActive, setLoaderActive] = useState(false)

    const [loadingProjects, setLoadingProjects] = useState('loading')
    const [projects, setProjects] = useState([])
    const [pickedProject, setPickedProject] = useState({ id: '', name: '' })

    const [loadingComponents, setLoadingComponents] = useState('loading')
    const [components, setComponents] = useState([{ address: '' }])
    const [pickedComponent, setPickedComponent] = useState({ id: '' })
    const [newComponentStatus, setNewComponentStatus] = useState('')
    const [componentVulnerabilities, setComponentVulnerabilities] = useState([])
    const [pickedVulnerability, setPickedVulnerability] = useState('')


    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isVulnerabilityModalOpen, setIsVulnerabilityModalOpen] = useState(false);

    const [filterComponents, setFilterComponents] = useState({ name: '' });
    const [filterVulnerabilities, setFilterVulnerabilities] = useState({ vulnId: '' });


    function closeChangeModal() {
        setIsChangeModalOpen(false);
    }

    function closeVulnerabilityModal() {
        setPickedVulnerability('')
        setIsVulnerabilityModalOpen(false);
    }

    async function getProjects() {
        try {
            setLoadingProjects('loading')
            const projects = await apiGetProjects()
            console.log(projects)
            setProjects(projects)
            setLoadingProjects('loaded')
        } catch (err) {
            setLoadingProjects('error')
        }
    }

    async function getComponents(uuid) {
        try {
            setLoadingComponents('loading')
            const components = await apiGetComponents(uuid)
            setComponents(components)
            setLoadingComponents('loaded')
        } catch (err) {
            setComponents([])
            setLoadingComponents('error')
        }
    }

    async function getDependencyTrackReport() {
        try {
            const report = await apiGetDependencyTrackReport(pickedProject.uuid, pickedProject.name)
            if (report) {
                setNotificationData({ message: 'Отчёт загружен', type: 'success' })
                toggleNotificationFunc()
            }
        } catch (err) {
            setNotificationData({ message: 'Не удалось загрузить отчет', type: 'error' })
            toggleNotificationFunc()
        }
    }

    async function showComponentVulnerabilities() {
        setComponentVulnerabilities(pickedComponent.vulnerabilities)
        closeChangeModal()
    }


    const filteredComponents = components.filter(item => {
        return (
            (filterComponents.name === '' || item.name.includes(filterComponents.name))
        );
    }
    )

    const filteredVulnerabilities = componentVulnerabilities.filter(item => {
        return (
            (filterVulnerabilities.vulnId === '' || item.vulnId.includes(filterVulnerabilities.vulnId))
        );
    }
    )

    useEffect(() => {
        getProjects()
    }, [])


    return (
        <>
            <div className="componentsProjects">
                <p>Проекты</p>
                {loadingProjects === 'loading' && <Loader />}
                {loadingProjects === 'error' && <p> бекенд отвалился или сервер Dependency-Track недоступен</p>}
                {loadingProjects === 'loaded' && <>
                    {projects.map(project =>
                        <ProjectCard id={project.id}
                            name={project.name}
                            picked={pickedProject.id === project.id && true || false}
                            onClick={() => { setPickedComponent(''); setPickedComponent(''); setPickedProject(project); getComponents(project.uuid) }}>
                        </ProjectCard>)}
                </>}
            </div>

            <div className="componentsComponents">
                <p>Компоненты с уязвимостями</p>

                <div >
                    <img src={filterLogo} alt="" className="filterLogo" />
                    <input type="text" className="componentFilter" placeholder="Название" onChange={e => setFilterComponents({ ...filterComponents, name: e.target.value })} value={filterComponents.name} />
                    <button onClick={() => setFilterComponents({ name: '' })} className="clearFilter">Очистить</button>
                </div>

                {pickedProject.id === '' && <p> Выберете проект</p>}
                {pickedProject.id !== '' && loadingComponents === 'loading' && <Loader />}
                {loadingComponents === 'error' && <p> бекенд отвалился</p>}
                {loadingComponents === 'loaded' && <>
                    <Button style={"componentVulnerabilities"} onClick={() => getDependencyTrackReport()}> Создать отчет </Button>
                    {components.length === 0 && loadingComponents === 'loaded' && <p> Компоненты не найдены</p>}
                    {filteredComponents.map(component =>
                        <ComponentCard id={component.id}
                            name={component.name}
                            version={component.version}
                            picked={pickedComponent.uuid === component.uuid && true || false}
                            onClick={() => { setComponentVulnerabilities([]); setPickedComponent(component); setIsChangeModalOpen(true) }}>
                        </ComponentCard>)}
                </>}
                <Modal isOpen={isChangeModalOpen} onClose={closeChangeModal}>
                    <div className="DTmodalComponents">
                        <div className="changeModalComponentsParamsDT">
                            <p>Проект: {pickedProject.name}</p>
                            <p>Название: {pickedComponent.name}</p>
                            <p>Тип: {pickedComponent.classifier}</p>
                            <p>Описание: {pickedComponent.description}</p>
                            <p>Версия: {pickedComponent.version}</p>
                        </div>
                        <div className="changeModalComponentVulnerabilitiesButton">
                            <Button style={"componentVulnerabilities"} onClick={() => showComponentVulnerabilities()}> Показать уязвимости </Button>
                            <Button style={"projectClose"} onClick={closeChangeModal}> Закрыть </Button>
                        </div>
                    </div>
                </Modal>

            </div>

            <div className="componentsVulnerabilities">

                <p>Уязвимости</p>

                <div >
                    <img src={filterLogo} alt="" className="filterLogo" />
                    <input type="text" className="vulnerabilityFilter" placeholder="CVE id" onChange={e => setFilterVulnerabilities({ ...filterVulnerabilities, vulnId: e.target.value })} value={filterVulnerabilities.vulnId} />
                    <button onClick={() => setFilterVulnerabilities({ vulnId: '' })} className="clearFilter">Очистить</button>
                </div>
                {pickedProject.id !== '' && pickedComponent.id !== '' && componentVulnerabilities.length === 0 && <p> Выберете компонент</p>}
                {filteredVulnerabilities.map(vuln =>
                    <VulnerabilityCard id={vuln.uuid}
                        name={vuln.vulnId}
                        onClick={() => { setPickedVulnerability(vuln); setIsVulnerabilityModalOpen(true) }}
                        picked={pickedVulnerability.uuid === vuln.uuid && true || false}
                        severity={vuln.severity}
                    >
                    </VulnerabilityCard>)}
            </div>
            <Modal isOpen={isVulnerabilityModalOpen} onClose={closeVulnerabilityModal}>
                {pickedVulnerability && <div className="vulnerabilityModalDT">
                    <div className="vulnerabilityModalInfoDT">
                        <p> <b>CVE id: </b>{pickedVulnerability.vulnId}</p>
                        <p> <b>Severity: </b>{pickedVulnerability.severity}</p>
                        <p> <b>Описание: </b>{pickedVulnerability.description}</p>
                        <p> <b>Ссылки: </b>{pickedVulnerability.references}</p>

                    </div>
                    <div className="changeModalProjectsButtonsDT">

                        <Button style={"projectClose"} onClick={closeVulnerabilityModal}> Закрыть </Button>
                    </div>
                </div>}
            </Modal>
        </>
    );
}
