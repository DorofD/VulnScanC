import React, { useState, useEffect } from "react";
import "./Projects.css";
import { apiAddProject, apiGetProjects, apiDeleteProject, apiChangeProject } from "../../services/apiProjects";
import ProjectCard from "./ProjectCard/ProjectCard";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import AcceptModal from "../AcceptModal/AcceptModal";
import Loader from "../Loader/Loader";

export default function Projects() {
    const { addMessage } = useTimedMessagesContext();
    const [loadingProjects, setLoadingProjects] = useState('loading');
    const [projects, setProjects] = useState([]);
    const [pickedProject, setPickedProject] = useState({ id: '0', name: '', type: 'common', description: '' });
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);
    const [actionFunction, setActionFunction] = useState(null);
    const [viewMode, setViewMode] = useState('list'); // 'list', 'add', 'edit', 'details'

    const changeProjectName = (event) => {
        setPickedProject({ ...pickedProject, name: event.target.value });
    };

    const changeProjectDescription = (event) => {
        setPickedProject({ ...pickedProject, description: event.target.value });
    };

    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    const resetPickedProject = () => {
        setPickedProject({ id: '0', name: '', type: 'common', description: '' });
        setViewMode('list');
    };

    async function getProjects() {
        try {
            setLoadingProjects('loading');
            const projects = await apiGetProjects();
            setProjects(projects);
            setLoadingProjects('loaded');
        } catch (err) {
            setLoadingProjects('error');
            addMessage('Ошибка при загрузке проектов: ' + err.message, 'error', 5000);
        }
    }

    async function addProject() {
        try {
            const response = await apiAddProject(pickedProject.name, pickedProject.description);
            if (response.status === 200) {
                getProjects();
                resetPickedProject();
                addMessage('Проект добавлен', 'success', 3000);
            } else {
                addMessage('Не удалось добавить проект', 'error', 3000);
            }
        } catch (err) {
            addMessage(`Проблема с бекендом: ${err.message}`, 'error', 5000);
        }
    }

    async function deleteProject() {
        try {
            const response = await apiDeleteProject(pickedProject.id);
            if (response.status === 200) {
                getProjects();
                resetPickedProject();
                addMessage('Проект удален', 'success', 3000);
                setIsAcceptModalOpen(false);
            } else {
                addMessage('Не удалось удалить проект', 'error', 3000);
                setIsAcceptModalOpen(false);
            }
        } catch (err) {
            addMessage(`Проблема с бекендом: ${err.message}`, 'error', 5000);
            setIsAcceptModalOpen(false);
        }
    }

    async function changeProject() {
        try {
            const response = await apiChangeProject(pickedProject.id, pickedProject.name, pickedProject.description);
            if (response.status === 200) {
                getProjects();
                resetPickedProject();
                addMessage('Проект изменен', 'success', 3000);
                setIsAcceptModalOpen(false);
            } else {
                addMessage('Не удалось изменить проект', 'error', 3000);
                setIsAcceptModalOpen(false);
            }
        } catch (err) {
            addMessage(`Проблема с бекендом: ${err.message}`, 'error', 5000);
            setIsAcceptModalOpen(false);
        }
    }

    useEffect(() => {
        getProjects();
    }, []);

    return (
        <>
            <div className="projects">
                <div className="projectsLeft">
                    <div className="projectsLeft1">
                        Обычные проекты
                        <br />
                        <button onClick={() => {
                            setPickedProject({ id: '0', name: '', type: 'common', description: '' });
                            setViewMode('add');
                        }}>
                            Добавить
                        </button>
                    </div>
                    <div className="projectsLeft2">
                        {loadingProjects === 'loading' && <Loader />}
                        {loadingProjects === 'error' && <p>бекенд отвалился</p>}
                        {loadingProjects === 'loaded' && (
                            <>
                                {projects.map(project => (
                                    <ProjectCard
                                        key={project.id}
                                        id={project.id}
                                        name={project.name}
                                        picked={pickedProject.id === project.id}
                                        onClick={() => {
                                            setPickedProject({
                                                id: project.id,
                                                name: project.name,
                                                type: 'common',
                                                description: project.description || ''
                                            });
                                            setViewMode('details');
                                        }}
                                    />
                                ))}
                            </>
                        )}
                    </div>
                </div>
                <div className="projectsRight">
                    {viewMode === 'add' || viewMode === 'edit' ? (
                        <div className="projectsRightForm">
                            <h3 className="projectsRightTitle">{viewMode === 'add' ? 'Добавить проект' : 'Редактировать проект'}</h3>
                            <div className="formGroup">
                                <label className="formLabel">Название:</label>
                                <input
                                    type="text"
                                    value={pickedProject.name}
                                    onChange={changeProjectName}
                                    className="formInput"
                                />
                            </div>
                            <div className="formGroup">
                                <label className="formLabel">Описание:</label>
                                <textarea
                                    value={pickedProject.description}
                                    onChange={changeProjectDescription}
                                    className="formInput"
                                    placeholder="Описание проекта..."
                                />
                            </div>
                            <div className="formButtons">
                                {viewMode === 'add' ? (
                                    <button className="formButton primary" onClick={addProject}>Добавить</button>
                                ) : (
                                    <>
                                        <button className="formButton primary" onClick={() => openAcceptModalWithAction(changeProject)}>Изменить</button>
                                        <button className="formButton critical" onClick={() => openAcceptModalWithAction(deleteProject)}>Удалить</button>
                                    </>
                                )}
                                <button className="formButton" onClick={resetPickedProject}>Отмена</button>
                            </div>
                        </div>
                    ) : viewMode === 'details' ? (
                        <div className="projectsRightDetails">
                            {pickedProject.id !== '0' ? (
                                <div className="detailsContent">
                                    <h2 className="detailsTitle">{pickedProject.name}</h2>
                                    <div className="detailsDescription">
                                        <p>{pickedProject.description || "Описание отсутствует"}</p>
                                    </div>
                                    <div className="detailsActions">
                                        <button className="detailsButton" onClick={() => setViewMode('edit')}>
                                            Редактировать
                                        </button>
                                    </div>
                                </div>
                            ) : (
                                <div className="emptyDetails">
                                    <p>Выберите проект для просмотра деталей</p>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="emptyRight">
                            <p>Выберите проект или добавьте новый</p>
                        </div>
                    )}
                </div>
            </div>

            <AcceptModal isOpen={isAcceptModalOpen} onClose={() => setIsAcceptModalOpen(false)}>
                <div className="acceptModal">
                    <div className="acceptModalText">Вы уверены?</div>
                    <div className="acceptModalButtons">
                        <button className="positive acceptModal" onClick={() => { actionFunction(); setIsAcceptModalOpen(false); }}>Да</button>
                        <button className="critical acceptModal" onClick={() => setIsAcceptModalOpen(false)}>Нет</button>
                    </div>
                </div>
            </AcceptModal>
        </>
    );
}
