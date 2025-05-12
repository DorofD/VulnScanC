import React from "react";
import { useState, useEffect, useContext } from "react";
import "./Projects.css";
import Button from "../Button/Button";
import { apiAddProject, apiGetProjects, apiDeleteProject, apiChangeProject } from "../../services/apiProjects";
import { apiAddBitbakeProject, apiGetBitbakeProjects, apiDeleteBitbakeProject, apiChangeBitbakeProject } from "../../services/apiBitbake";
import ProjectCard from "./ProjectCard/ProjectCard";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import Loader from "../Loader/Loader";

export default function Projects() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
    const [loaderActive, setLoaderActive] = useState(false)

    const [loadingProjects, setLoadingProjects] = useState('loading')
    const [projects, setProjects] = useState([])
    const [bitbakeProjects, setBitbakeProjects] = useState([])
    const [pickedProject, setPickedProject] = useState({ id: '0', name: '', type: '' })


    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);


    const [actionFunction, setActionFunction] = useState(null);


    const changeProjectName = (event) => {
        setPickedProject({ id: pickedProject['id'], name: event.target.value, type: pickedProject['type'] });
    };


    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    function closeChangeModal() {
        setPickedProject({ id: '0', name: '' })
        setIsChangeModalOpen(false);
    }

    function closeAddModal() {
        setPickedProject({ id: '0', name: '' })
        setIsAddModalOpen(false);
    }

    function closeAcceptModal() {
        setIsAcceptModalOpen(false);
    }


    async function getProjects() {
        try {
            setLoadingProjects('loading')
            const projects = await apiGetProjects()
            setProjects(projects)
            const bitbakeProjects = await apiGetBitbakeProjects()
            setBitbakeProjects(bitbakeProjects)
            setLoadingProjects('loaded')
        } catch (err) {
            setLoadingProjects('error')
        }
    }

    async function addProject() {
        try {
            const apiFunctions = {
                common: apiAddProject,
                bitbake: apiAddBitbakeProject,
            };
            const apiFunction = apiFunctions[pickedProject['type']];
            const response = await apiFunction(pickedProject['name'])
            if (response.status == 200) {
                getProjects()
                setPickedProject({ id: '0', name: 'default' })
                setNotificationData({ message: 'Проект добавлен', type: 'success' })
                toggleNotificationFunc()
                closeAddModal()

            } else {
                setNotificationData({ message: 'Не удалось добавить проект', type: 'error' })
                toggleNotificationFunc()
            }
        } catch (err) {
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
        }

    }

    async function deleteProject() {
        try {
            const apiFunctions = {
                common: apiDeleteProject,
                bitbake: apiDeleteBitbakeProject,
            };
            const apiFunction = apiFunctions[pickedProject['type']];
            const response = await apiFunction(pickedProject['id'])
            if (response.status == 200) {
                getProjects()
                setPickedProject({ id: '0', name: 'default' })
                setNotificationData({ message: 'Проект удален', type: 'success' })
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()

            } else {
                setNotificationData({ message: 'Не удалось удалить проект', type: 'error' })
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()
            }
        } catch (err) {
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
        }
    }

    async function changeProject() {
        try {
            const apiFunctions = {
                common: apiChangeProject,
                bitbake: apiChangeBitbakeProject,
            };
            const apiFunction = apiFunctions[pickedProject['type']];
            const response = await apiFunction(pickedProject['id'], pickedProject['name'])
            if (response.status == 200) {
                getProjects()
                setPickedProject({ id: '0', name: 'default' })
                setNotificationData({ message: 'Проект изменен', type: 'success' })
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()

            } else {
                setNotificationData({ message: 'Не удалось изменить проект', type: 'error' })
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()
            }
        } catch (err) {
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
        }
    }

    useEffect(() => {
        getProjects()
    }, [])


    return (
        <>
            <div className="mainProjects">
                <p className="projectsTitle">Обычные проекты</p>
                <ProjectCard id={0}
                    name={'Добавить проект'}
                    picked={(pickedProject.type === 'common' && pickedProject.id === 0) ? true : false}
                    onClick={() => { setPickedProject({ id: 0, name: '', type: 'common' }); setIsAddModalOpen(true) }}>
                </ProjectCard>
                {loadingProjects === 'loading' && <Loader />}
                {loadingProjects === 'error' && <p> бекенд отвалился</p>}
                {loadingProjects === 'loaded' && <>
                    {projects.map(project =>
                        <ProjectCard id={project.id}
                            name={project.name}
                            picked={(pickedProject.type === 'common' && pickedProject.id === project.id) ? true : false}
                            onClick={() => { setPickedProject({ id: project.id, name: project.name, type: 'common' }); setIsChangeModalOpen(true) }}>
                        </ProjectCard>)}
                </>}
            </div>
            <div className="mainProjects">
                <p className="projectsTitle">Проекты BitBake</p>
                <ProjectCard id={0}
                    name={'Добавить проект'}
                    picked={(pickedProject.type === 'bitbake' && pickedProject.id === 0) ? true : false}
                    onClick={() => { setPickedProject({ id: 0, name: '', type: 'bitbake' }); setIsAddModalOpen(true) }}>
                </ProjectCard>
                {loadingProjects === 'loading' && <Loader />}
                {loadingProjects === 'error' && <p> бекенд отвалился</p>}
                {loadingProjects === 'loaded' && <>
                    {bitbakeProjects.map(project =>
                        <ProjectCard id={project.id}
                            name={project.name}
                            picked={(pickedProject.type === 'bitbake' && pickedProject.id === project.id) ? true : false}
                            onClick={() => { setPickedProject({ id: project.id, name: project.name, type: 'bitbake' }); setIsChangeModalOpen(true) }}>
                        </ProjectCard>)}
                </>}
            </div>
            <Modal isOpen={isChangeModalOpen} onClose={closeChangeModal}>
                <div className="changeModalProjects">
                    <div className="changeModalProjectsName">
                        <textarea name="projectName"
                            id={pickedProject['id']}
                            placeholder='Название проекта'
                            className="projects"
                            value={pickedProject['name']}
                            onChange={changeProjectName}> </textarea>
                    </div>
                    <div className="changeModalProjectsButtons">
                        <Button style={"projectAccept"} onClick={() => openAcceptModalWithAction(changeProject)}> Изменить </Button>
                        <Button style={"projectReject"} onClick={() => openAcceptModalWithAction(deleteProject)}> Удалить </Button>
                        <Button style={"projectClose"} onClick={closeChangeModal}> Закрыть </Button>
                    </div>
                </div>
            </Modal>

            <Modal isOpen={isAddModalOpen} onClose={closeAddModal}>
                <div className="changeModalProjects">
                    <div className="changeModalProjectsName">
                        <textarea name="projectName"
                            id={pickedProject['id']}
                            placeholder='Название проекта'
                            className="projects"
                            value={pickedProject['name']}
                            onChange={changeProjectName}> </textarea>
                    </div>
                    <div className="changeModalProjectsButtons">
                        <Button style={"projectAccept"} onClick={() => addProject()}> Добавить </Button>
                        <Button style={"projectClose"} onClick={closeAddModal}> Закрыть </Button>
                    </div>
                </div>
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
        </>
    );
}
