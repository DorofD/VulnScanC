import React from "react";
import { useProjects } from "../../hooks/useProjects";
import { useComponents } from "../../hooks/useComponents";
import { useVulnerabilities } from "../../hooks/useVulnerabilities";
import { useComments } from "../../hooks/useComments";
import { useAuthContext } from "../../hooks/useAuthContext";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";

import ProjectCard from "../Projects/ProjectCard/ProjectCard";
import ComponentSection from "./SubComponents/ComponentSection";
import VulnerabilitySection from "./SubComponents/VulnerabilitySection";
import Loader from "../Loader/Loader";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import Button from "../Button/Button";

export default function Components() {
    const { userName, userId } = useAuthContext();
    const { messages, addMessage } = useTimedMessagesContext();

    const { 
        projects, 
        loadingProjects, 
        pickedProject, 
        setPickedProject, 
        getProjects 
    } = useProjects();

    const { 
        components, 
        loadingComponents, 
        pickedComponent, 
        setPickedComponent, 
        filterComponents, 
        setFilterComponents, 
        newComponentStatus,
        setNewComponentStatus,
        getProjectComponents
    } = useComponents(pickedProject, setLoaderActive);

    const { 
        componentVulnerabilities, 
        setComponentVulnerabilities,
        showedVunls,
        setShowedVunls,
        pickedVulnerability,
        setPickedVulnerability,
        filterVulnerabilities,
        setFilterVulnerabilities,
        filterVulnerabilitiesBdu,
        setFilterVulnerabilitiesBdu,
        showComponentVulnerabilities,
        showComponentVulnerabilitiesBdu,
        onOpenVulnerabilityModal,
        closeVulnerabilityModal
    } = useVulnerabilities();

    const { 
        componentComments, 
        componentComment, 
        setComponentComment, 
        pickedComment,
        setPickedComment,
        addComponentComment: onAddComponentComment, 
        deleteComponentComment: onDeleteComponentComment, 
        getComponentComments
    } = useComments(pickedComponent?.id, userId);

    const [loaderActive, setLoaderActive] = React.useState(false);
    const [isChangeModalOpen, setIsChangeModalOpen] = React.useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = React.useState(false);
    const [isVulnerabilityModalOpen, setIsVulnerabilityModalOpen] = React.useState(false);
    const [actionFunction, setActionFunction] = React.useState(null);
    const [newLicense, setNewLicense] = React.useState({ component_id: '', key: '', name: '', spdx_id: '', url: '' });

    React.useEffect(() => {
        getProjects();
    }, []);

    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    const closeChangeModal = () => {
        setIsChangeModalOpen(false);
        setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' });
        setComponentComment({ user_id: userId, comment: '' });
    };

    const closeAcceptModal = () => {
        setPickedVulnerability('');
        setIsAcceptModalOpen(false);
        setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' });
    };

    const closeVulnerabilityModalInternal = () => {
        setPickedVulnerability('');
        setIsVulnerabilityModalOpen(false);
        setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' });
    };

    const handleSelectStatus = (event) => {
        setNewComponentStatus(event.target.value);
    };

    const handleChangeComponentStatus = async () => {
        if (newComponentStatus === '') {
            addMessage('Выберете новый статус', 'error', 3000);
            return;
        }
        try {
            const { apiChangeComponentStatus } = await import('../../services/apiComponents');
            const response = await apiChangeComponentStatus(pickedComponent.id, newComponentStatus);
            if (response.status === 200) {
                await getProjectComponents(pickedProject.id);
                setNewComponentStatus('');
                addMessage('Статус изменен', 'success', 3000);
            } else {
                addMessage('Не удалось изменить статус', 'error', 3000);
                setNewComponentStatus('');
            }
        } catch (error) {
            addMessage(`Проблема с бекендом: ${error.message || error}`, 'error', 5000);
            setNewComponentStatus('');
        }
    };

    const handleCheckLicenses = async () => {
        if (!pickedProject.id) return;
        addMessage('Выполняется поиск лицензий', 'success', 3000);
        setLoaderActive(true);

        try {
            const { apiCheckLicenses } = await import('../../services/apiLicenses');
            const response = await apiCheckLicenses(pickedProject.id);
            if (response.status === 200) {
                setLoaderActive(false);
                await getProjectComponents(pickedProject.id);
                addMessage('Поиск завершен', 'success', 3000);
            } else {
                setLoaderActive(false);
                addMessage('Не удалось выполнить поиск лицензий', 'error', 3000);
            }
        } catch (error) {
            setLoaderActive(false);
            addMessage(`Проблема с бекендом: ${error.message || error}`, 'error', 5000);
        }
    };

    const handleAddLicense = async () => {
        if (!pickedComponent.id) return;
        try {
            const { apiAddLicense } = await import('../../services/apiLicenses');
            const response = await apiAddLicense(
                pickedComponent.id,
                newLicense.key,
                newLicense.name,
                newLicense.spdx_id,
                newLicense.url
            );
            if (response.status === 200) {
                setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' });
                await getProjectComponents(pickedProject.id);
                addMessage('Лицензия добавлена', 'success', 3000);
            } else {
                addMessage('Не удалось добавить лицензию', 'error', 3000);
            }
        } catch (error) {
            addMessage(`Проблема с бекендом: ${error.message || error}`, 'error', 5000);
        }
    };

    const handleDeleteLicense = async (licenseId) => {
        try {
            const { apiDeleteLicense } = await import('../../services/apiLicenses');
            const response = await apiDeleteLicense(licenseId);
            if (response.status === 200) {
                await getProjectComponents(pickedProject.id);
                addMessage('Лицензия удалена', 'success', 3000);
            } else {
                addMessage('Не удалось удалить лицензию', 'error', 3000);
            }
        } catch (error) {
            addMessage(`Проблема с бекендом: ${error.message || error}`, 'error', 5000);
        }
    };

    return (
        <>
            {loaderActive && <Loader />}
            <div className="componentsProjects">
                <p>Проекты</p>
                {loadingProjects === 'loading' && <Loader />}
                {loadingProjects === 'error' && <p> бекенд отвалился</p>}
                {loadingProjects === 'loaded' && (
                    <>
                        {projects.map(project => (
                            <ProjectCard 
                                key={project.id}
                                id={project.id}
                                name={project.name}
                                picked={pickedProject.id === project.id}
                                onClick={() => { 
                                    setComponentVulnerabilities([]); 
                                    setPickedProject(project); 
                                    getProjectComponents(project.id);
                                }} 
                            />
                        ))}
                    </>
                )}
            </div>

            <ComponentSection 
                components={components}
                loadingComponents={loadingComponents}
                pickedProject={pickedProject}
                pickedComponent={pickedComponent}
                filterComponents={filterComponents}
                setFilterComponents={setFilterComponents}
                onComponentClick={(comp) => {
                    setPickedComponent(comp);
                    getComponentComments(comp.id);
                    setIsChangeModalOpen(true);
                }}
                onCheckLicenses={handleCheckLicenses}
                onCloseChangeModal={closeChangeModal}
                onOpenAcceptModal={openAcceptModalWithAction}
                onCloseAcceptModal={closeAcceptModal}
                onDeleteLicense={handleDeleteLicense}
                onAddLicense={handleAddLicense}
                onChangeComponentStatus={handleChangeComponentStatus}
                onSelectStatus={handleSelectStatus}
                newComponentStatus={newComponentStatus}
                setNewComponentStatus={setNewComponentStatus}
                newLicense={newLicense}
                setNewLicense={setNewLicense}
                componentComments={componentComments}
                componentComment={componentComment}
                setComponentComment={setComponentComment}
                onAddComponentComment={onAddComponentComment}
                onDeleteComponentComment={onDeleteComponentComment}
                pickedComment={pickedComment}
                onPickedComment={setPickedComment}
                showComponentVulnerabilities={showComponentVulnerabilities}
                showComponentVulnerabilitiesBdu={showComponentVulnerabilitiesBdu}
                setShowedVunls={setShowedVunls}
                onOpenVulnerabilityModal={onOpenVulnerabilityModal}
                isChangeModalOpen={isChangeModalOpen}
                isAcceptModalOpen={isAcceptModalOpen}
                closeChangeModal={closeChangeModal}
                closeAcceptModal={closeAcceptModal}
                closeVulnerabilityModal={closeVulnerabilityModal}
                actionFunction={actionFunction}
                pickedProjectName={pickedProject?.name || ''}
                pickedComponentPath={pickedComponent?.path || ''}
                pickedComponentType={pickedComponent?.type || ''}
                pickedComponentAddress={pickedComponent?.address || ''}
                pickedComponentTag={pickedComponent?.tag || ''}
                pickedComponentVersion={pickedComponent?.version || ''}
                pickedComponentScore={pickedComponent?.score || ''}
                pickedComponentStatus={pickedComponent?.status || ''}
                pickedComponentLicenses={pickedComponent?.licenses || []}
                pickedComponentId={pickedComponent?.id || ''}
            />

            <VulnerabilitySection 
                componentVulnerabilities={componentVulnerabilities}
                showedVunls={showedVunls}
                pickedProject={pickedProject}
                pickedComponent={pickedComponent}
                filterVulnerabilities={filterVulnerabilities}
                setFilterVulnerabilities={setFilterVulnerabilities}
                filterVulnerabilitiesBdu={filterVulnerabilitiesBdu}
                setFilterVulnerabilitiesBdu={setFilterVulnerabilitiesBdu}
                pickedVulnerability={pickedVulnerability}
                setPickedVulnerability={setPickedVulnerability}
                setIsVulnerabilityModalOpen={setIsVulnerabilityModalOpen}
                onOpenVulnerabilityModal={onOpenVulnerabilityModal}
                closeVulnerabilityModal={closeVulnerabilityModalInternal}
                filterLogo="" 
            />

            <AcceptModal isOpen={isAcceptModalOpen} onClose={closeAcceptModal}>
                <div className="acceptModalProjects">
                    <div className="acceptModalProjectsText">Вы уверены?</div>
                    <div className="acceptModalProjectsButtons">
                        <Button style={"projectAccept"} onClick={() => { actionFunction(); closeAcceptModal(); }}> Да </Button>
                        <Button style={"projectReject"} onClick={closeAcceptModal}> Нет </Button>
                    </div>
                </div>
            </AcceptModal>

            <Modal isOpen={isVulnerabilityModalOpen} onClose={closeVulnerabilityModalInternal}>
                 {/* Content handled by VulnerabilitySection */}
            </Modal>
        </>
    );
}
