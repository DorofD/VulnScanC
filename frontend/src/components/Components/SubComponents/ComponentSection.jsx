import React from "react";
import Button from "../../../components/Button/Button";
import ComponentCard from "../ComponentCard/ComponentCard";
import Modal from "../../../components/Modal/Modal";
import AcceptModal from "../../../components/AcceptModal/AcceptModal";
import LicenseModalContent from "./LicenseModalContent";
import CommentModalContent from "./CommentModalContent";

const ComponentSection = ({
    components,
    loadingComponents,
    pickedProject,
    pickedComponent,
    filterComponents,
    setFilterComponents,
    onComponentClick,
    onCheckLicenses,
    onCloseChangeModal,
    isChangeModalOpen,
    onOpenAcceptModal,
    isAcceptModalOpen,
    onCloseAcceptModal,
    onDeleteLicense,
    onAddLicense,
    onSelectStatus,
    onChangeComponentStatus,
    newComponentStatus,
    setNewComponentStatus,
    newLicense,
    setNewLicense,
    componentComments,
    componentComment,
    setComponentComment,
    onAddComponentComment,
    onDeleteComponentComment,
    onPickedComment,
    pickedComment,
    userName,
    showComponentVulnerabilities,
    showComponentVulnerabilitiesBdu,
    setShowedVunls,
    onOpenVulnerabilityModal,
    closeChangeModal,
    closeAcceptModal,
    closeVulnerabilityModal,
    actionFunction,
    pickedProjectName,
    pickedComponentPath,
    pickedComponentType,
    pickedComponentAddress,
    pickedComponentTag,
    pickedComponentVersion,
    pickedComponentScore,
    pickedComponentStatus,
    pickedComponentLicenses,
    pickedComponentId
}) => {
    const filteredComponents = components.filter(item => {
        return (
            (filterComponents.address === '' || item.address.includes(filterComponents.address)) &&
            (filterComponents.status === '' || item.status.includes(filterComponents.status))
        );
    });

    return (
        <div className="componentsComponents">
            <p>Компоненты</p>

            <div>
                <img src="" alt="" className="filterLogo" /> {/* filterLogo was not imported in original but used */}
                <input 
                    type="text" 
                    className="componentFilter" 
                    placeholder="Название" 
                    onChange={e => setFilterComponents({ ...filterComponents, address: e.target.value })} 
                    value={filterComponents.address} 
                />
                <input 
                    type="text" 
                    className="componentFilter" 
                    placeholder="Статус" 
                    onChange={e => setFilterComponents({ ...filterComponents, status: e.target.value })} 
                    value={filterComponents.status} 
                />
                <button onClick={() => setFilterComponents({ address: '', status: '' })} className="clearFilter">Очистить</button>
            </div>

            {pickedProject.id === '' && <p> Выберете проект</p>}
            {pickedProject.id !== '' && loadingComponents === 'loading' && <p> Loading components...</p>}
            {loadingComponents === 'error' && <p> бекенд отвалился</p>}
            {loadingComponents === 'loaded' && (
                <>
                    <Button style={"componentVulnerabilities"} onClick={onCheckLicenses}> Проверить лицензии </Button>

                    {components.length === 0 && loadingComponents === 'loaded' && <p> Компоненты не найдены</p>}
                    {filteredComponents.map(component => (
                        <ComponentCard 
                            key={component.id}
                            id={component.id}
                            name={component.address}
                            status={component.status}
                            license_number={component.licenses ? component.licenses.length : 0}
                            osv_vuln_number={component.osv_vuln_count}
                            bdu_vuln_number={component.bdu_vuln_count}
                            picked={pickedComponent.id === component.id}
                            onClick={() => onComponentClick(component)}
                        />
                    ))}
                </>
            )}

<Modal isOpen={isChangeModalOpen} onClose={onCloseChangeModal}>
                <div className="changeModalComponents">
                    <div className="changeModalComponentsParams">
                        <p>Проект: {pickedProjectName}</p>
                        <p>Путь в проекте: {pickedComponentPath}</p>
                        <p>Тип: {pickedComponentType}</p>
                        <p>Адрес: {pickedComponentAddress}</p>
                        <p>Тег: {pickedComponentTag}</p>
                        <p>Версия: {pickedComponentVersion}</p>
                        <p>Score: {pickedComponentScore}</p>
                        <p>Статус: {pickedComponentStatus}</p>
                        
                        <LicenseModalContent 
                            pickedComponentLicenses={pickedComponentLicenses}
                            onOpenAcceptModal={onOpenAcceptModal}
                            onDeleteLicense={onDeleteLicense}
                            newLicense={newLicense}
                            setNewLicense={setNewLicense}
                            onAddLicense={onAddLicense}
                            pickedComponentId={pickedComponentId}
                        />

                        <div className="changeModalComponentVulnerabilitiesButton">
                            <Button style={"componentVulnerabilities"} onClick={() => { setShowedVunls('osv'); showComponentVulnerabilities(); }}> Показать уязвимости CVE </Button>
                        </div>
                        <div className="changeModalComponentVulnerabilitiesButton">
                            <Button style={"componentVulnerabilities"} onClick={() => { setShowedVunls('bdu'); showComponentVulnerabilitiesBdu(); }}> Показать уязвимости БДУ </Button>
                        </div>
                        <div className="changeModalProjectsButtons">
                            <select className="componentSelect" name="" id="" onChange={onSelectStatus}>
                                <option value="" disabled selected hidden>Изменить статус</option>
                                <option value="none">none</option>
                                <option value="confirmed">confirmed</option>
                                <option value="denied">denied</option>
                            </select>
                            <Button style={"projectAccept"} onClick={() => onOpenAcceptModal(onChangeComponentStatus)}> Изменить </Button>
                            <Button style={"projectClose"} onClick={onCloseChangeModal}> Закрыть </Button>
                        </div>
                    </div>
                    
                    <CommentModalContent 
                        componentComments={componentComments}
                        userName={userName}
                        pickedComment={pickedComment}
                        onPickedComment={onPickedComment}
                        onDeleteComponentComment={onDeleteComponentComment}
                        componentComment={componentComment}
                        setComponentComment={setComponentComment}
                        onAddComponentComment={onAddComponentComment}
                        pickedComponentId={pickedComponentId}
                    />
                </div>

                <AcceptModal isOpen={isAcceptModalOpen} onClose={onCloseAcceptModal}>
                    <div className="acceptModalProjects">
                        <div className="acceptModalProjectsText">Вы уверены?</div>
                        <div className="acceptModalProjectsButtons">
                            <Button style={"projectAccept"} onClick={() => { actionFunction(); onCloseAcceptModal(); }}> Да </Button>
                            <Button style={"projectReject"} onClick={onCloseAcceptModal}> Нет </Button>
                        </div>
                    </div>
                </AcceptModal>
            </Modal>

            {/* AcceptModal is already handled above inside the Modal for some reason in original code, 
                but I will keep it as per original structure to avoid breaking logic */}
        </div>
    );
};

export default ComponentSection;

