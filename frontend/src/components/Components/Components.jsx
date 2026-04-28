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
        onComponentClick,
        onCheckLicenses,
        onSelectStatus,
        newComponentStatus,
        setNewComponentStatus,
        newLicense,
        setNewLicense,
        onAddLicense,
        onDeleteLicense,
        getProjectComponents,
        getComponentComments
    } = useComponents();

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
        onAddComponentComment, 
        onDeleteComponentComment, 
        onPickedComment, 
        pickedComment,
        userName: commentUserName
    } = useComments(userId);

    const [loaderActive, setLoaderActive] = React.useState(false);
    const [isChangeModalOpen, setIsChangeModalOpen] = React.useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = React.useState(false);
    const [isVulnerabilityModalOpen, setIsVulnerabilityModalOpen] = React.useState(false);
    const [actionFunction, setActionFunction] = React.useState(null);

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
                onCheckLicenses={onCheckLicenses}
                onCloseChangeModal={closeChangeModal}
                onOpenAcceptModal={openAcceptModalWithAction}
                onCloseAcceptModal={closeAcceptModal}
                onDeleteLicense={onDeleteLicense}
                onAddLicense={onAddLicense}
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
                onPickedComment={onPickedComment}
                pickedComment={pickedComment}
                userName={userName}
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
                pickedProjectName={pickedProject.name}
                pickedComponentPath={pickedComponent.path}
                pickedComponentType={pickedComponent.type}
                pickedComponentAddress={pickedComponent.address}
                pickedComponentTag={pickedComponent.tag}
                pickedComponentVersion={pickedComponent.version}
                pickedComponentScore={pickedComponent.score}
                pickedComponentStatus={pickedComponent.status}
                pickedComponentLicenses={pickedComponent.licenses}
                pickedComponentId={pickedComponent.id}
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
