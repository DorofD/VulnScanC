import React from "react";
import Filter from "../../Filter/Filter";
import ComponentCard from "../ComponentCard/ComponentCard";
import Modal from "../../../components/Modal/Modal";
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
    onShowComponentVulnerabilities,
    onShowComponentVulnerabilitiesBdu,
    setShowedVunls,
    onOpenVulnerabilityModal,
    closeChangeModal,
    closeVulnerabilityModal,
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

            <Filter onClick={() => setFilterComponents({ address: '', status: '' })}>
                <input type="text" className="filter" placeholder="Название" onChange={e => setFilterComponents({ ...filterComponents, address: e.target.value })} value={filterComponents.address} />
                <input type="text" className="filter" placeholder="Статус" onChange={e => setFilterComponents({ ...filterComponents, status: e.target.value })} value={filterComponents.status} />
            </Filter>

            {pickedProject.id === '' && <p> Выберете проект</p>}
            {pickedProject.id !== '' && loadingComponents === 'loading' && <p> Loading components...</p>}
            {loadingComponents === 'error' && <p> бекенд отвалился</p>}
            {loadingComponents === 'loaded' && (
                <>
                    <button onClick={onCheckLicenses}> Проверить лицензии </button>

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
                    <div className="changeModalComponentsLeft">
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
                        </div>
                        <div className="changeModalComponentsFooter">
                            <div className="changeModalComponentVulnerabilitiesButton">
                                <button onClick={() => { setShowedVunls('osv'); onShowComponentVulnerabilities(pickedComponent.id); }}> Показать уязвимости CVE </button>
                            </div>
                            <div className="changeModalComponentVulnerabilitiesButton">
                                <button onClick={() => { setShowedVunls('bdu'); onShowComponentVulnerabilitiesBdu(pickedComponent.id); }}> Показать уязвимости БДУ </button>
                            </div>
                            <div className="changeModalProjectsButtons">
                                <select className="componentSelect" name="" id="" onChange={onSelectStatus}>
                                    <option value="" disabled selected hidden>Изменить статус</option>
                                    <option value="none">none</option>
                                    <option value="confirmed">confirmed</option>
                                    <option value="denied">denied</option>
                                </select>
                                <button onClick={() => onOpenAcceptModal(onChangeComponentStatus)}> Изменить </button>
                                <button onClick={onCloseChangeModal}> Закрыть </button>
                            </div>
                        </div>
                    </div>
                    <div className="changeModalComponentsRight">
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
                </div>
            </Modal>

            {/* AcceptModal is already handled above inside the Modal for some reason in original code, 
                but I will keep it as per original structure to avoid breaking logic */}
        </div>
    );
};

export default ComponentSection;

