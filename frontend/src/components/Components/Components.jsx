import React, { version } from "react";
import { useState, useEffect, useContext} from "react";
import "./Components.css";
import Button from "../Button/Button";
import { apiGetProjects } from "../../services/apiProjects";
import { apiGetProjectComponents, apiChangeComponentStatus } from "../../services/apiComponents";
import { apiGetComponentVulnerabilities } from "../../services/apiVulnerabilities";
import { apiGetBduComponentVulns } from "../../services/apiBduFstec";
import { apiCheckLicenses, apiAddLicense, apiDeleteLicense } from "../../services/apiLicenses";
import ProjectCard from "../Projects/ProjectCard/ProjectCard";
import ComponentCard from "./ComponentCard/ComponentCard";
import VulnerabilityCard from "./VulnerabilityCard/VulnerabilityCard";
import VulnerabilityCardBdu from "./VulnerabilityCardBdu/VulnerabilityCardBdu";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import filterLogo from './filter.png'
import Loader from "../Loader/Loader";

export default function Components() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
    const [ loaderActive, setLoaderActive ] = useState(false)
    
    const [loadingProjects, setLoadingProjects] = useState('loading')
    const [projects, setProjects] = useState([])
    const [pickedProject, setPickedProject] = useState({id: '', name: ''})
    
    
    const [loadingComponents, setLoadingComponents] = useState('loading')
    const [components, setComponents] = useState([{address:''}])
    const [pickedComponent, setPickedComponent] = useState({id: ''})
    const [newComponentStatus, setNewComponentStatus] = useState('')
    const [newLicense, setNewLicense] = useState({component_id:'', key:'', name:'', spdx_id:'', url:''})
    const [componentVulnerabilities, setcomponentVulnerabilities] = useState([])
    const [pickedVulnerability, setPickedVulnerability] = useState('')
    const [showedVunls, setShowedVunls] = useState(false)


    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);
    const [isVulnerabilityModalOpen, setIsVulnerabilityModalOpen] = useState(false);


    const [actionFunction, setActionFunction] = useState(null);

  
    const [filterComponents, setFilterComponents] = useState({ address: '', status:'' });
    const [filterVulnerabilities, setFilterVulnerabilities] = useState({ osv_id: '' });
    const [filterVulnerabilitiesBdu, setFilterVulnerabilitiesBdu] = useState({ bdu_id: '' });


    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
      };

    function closeChangeModal(){
        setIsChangeModalOpen(false);
        setNewLicense({component_id:'', key:'', name:'', spdx_id:'', url:''})
    } 

    function closeAcceptModal(){
        setPickedVulnerability('')
        setIsAcceptModalOpen(false);
        setNewLicense({component_id:'', key:'', name:'', spdx_id:'', url:''})
    } 

    function closeVulnerabilityModal(){
        setPickedVulnerability('')
        setIsVulnerabilityModalOpen(false);
        setNewLicense({component_id:'', key:'', name:'', spdx_id:'', url:''})
    } 
    
    const handleSelectStatus = (event) => {
        setNewComponentStatus(event.target.value);
      };

    async function getProjects() {
        try {
            setLoadingProjects('loading')
            const projects = await apiGetProjects()
            setProjects(projects)
            setLoadingProjects('loaded')
        } catch (err) {
            setLoadingProjects('error')
        }
    }

    async function getProjectComponents(id) {
        try {
            setLoadingComponents('loading')
            const components = await apiGetProjectComponents(id)

            const order = { 'none': 0, 'confirmed': 1, 'denied': 2 };
            const sortedComponents = components.sort((a, b) => {
                return order[a.status] - order[b.status];
            });
            setComponents(sortedComponents)
            setLoadingComponents('loaded')
        } catch (err) {
            setComponents([])
            setLoadingComponents('error')
        }
    }

    async function showComponentVulnerabilities() {
        try {
            const vulnerabilities = await apiGetComponentVulnerabilities(pickedComponent.id)
            setcomponentVulnerabilities(vulnerabilities)
        } catch (err) {
            setcomponentVulnerabilities([])
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
        }
        closeChangeModal()
    }

    async function showComponentVulnerabilities() {
        try {
            const vulnerabilities = await apiGetComponentVulnerabilities(pickedComponent.id)
            setcomponentVulnerabilities(vulnerabilities)
        } catch (err) {
            setcomponentVulnerabilities([])
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
        }
        closeChangeModal()
    }

    async function showComponentVulnerabilitiesBdu() {
        try {
            const vulnerabilities = await apiGetBduComponentVulns(pickedComponent.id)
            setcomponentVulnerabilities(vulnerabilities)
        } catch (err) {
            setcomponentVulnerabilities([])
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
        }
        closeChangeModal()
    }

    async function changeComponentStatus() {
        console.log(pickedComponent.id)
        console.log(newComponentStatus)
        if (newComponentStatus == '') {
            setNotificationData({message:'Выберете новый статус', type: 'error'})
            toggleNotificationFunc()
            return 0
        }
        try {
            const response = await apiChangeComponentStatus(pickedComponent.id, newComponentStatus)
            if (response.status == 200) {
                getProjectComponents(pickedProject.id)
                setNewComponentStatus('')
                setNotificationData({message:'Статус изменен', type: 'success'})
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()
            } else {
                setNotificationData({message:'Не удалось изменить статус', type: 'error'})
                setNewComponentStatus('')
                toggleNotificationFunc()
                closeChangeModal()
                closeAcceptModal()
            }
        } catch (error) {
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
            setNewComponentStatus('')
        }
    }
    
    async function checkLicenses() {
        setNotificationData({message:'Выполняется поиск лицензий', type: 'success'})
        toggleNotificationFunc()
        setLoaderActive(true)

        try {
            const response = await apiCheckLicenses(pickedProject.id)
            if (response.status == 200) {
                setLoaderActive(false)
                getProjectComponents(pickedProject.id)
                setNotificationData({message:'Поиск завершен', type: 'success'})
                toggleNotificationFunc()
            } else {
                setLoaderActive(false)
                setNotificationData({message:'Не удалось выполнить поиск лицензий', type: 'error'})
                toggleNotificationFunc()
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
        }
    }

    async function deleteLicense(license_id) {
        try {
            const response = await apiDeleteLicense(license_id)
            if (response.status == 200) {
                setLoaderActive(false)
                getProjectComponents(pickedProject.id)
                closeChangeModal()
                setNotificationData({message:'Лицензия удалена', type: 'success'})
                toggleNotificationFunc()
            } else {
                setLoaderActive(false)
                setNotificationData({message:'Не удалось удалить лицензию', type: 'error'})
                toggleNotificationFunc()
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
        }
    }

    async function addLicense() {
        try {
            const response = await apiAddLicense(pickedComponent.id, newLicense.key, newLicense.name, newLicense.spdx_id, newLicense.url)
            if (response.status == 200) {
                setLoaderActive(false)
                getProjectComponents(pickedProject.id)
                closeChangeModal()
                setNotificationData({message:'Лицензия добавлена', type: 'success'})
                toggleNotificationFunc()
                setNewLicense({component_id:'', key:'', name:'', spdx_id:'', url:''})
            } else {
                setLoaderActive(false)
                setNotificationData({message:'Не удалось добавить лицензию', type: 'error'})
                toggleNotificationFunc()
                setNewLicense({component_id:'', key:'', name:'', spdx_id:'', url:''})
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
            setNewLicense({component_id:'', key:'', name:'', spdx_id:'', url:''})
        }
    }

    const filteredComponents = components.filter(item => {
        return (
          (filterComponents.address === '' || item.address.includes(filterComponents.address)) &&
          (filterComponents.status === '' || item.status.includes(filterComponents.status))
        );
      }
    )

    const filteredVulnerabilities = componentVulnerabilities.filter(item => {
        if (showedVunls == 'osv') {
            return (
              (filterVulnerabilities.osv_id === '' || item.osv_id.includes(filterVulnerabilities.osv_id))
            );
        }
        if (showedVunls == 'bdu'){
            return (
              (filterVulnerabilitiesBdu.bdu_id === '' || item.bdu_id.includes(filterVulnerabilitiesBdu.bdu_id))
            );
        }
      }
    )

    useEffect(() => {
        getProjects()
    }, [])
    

    return (
        <>
            {loaderActive && <Loader />}
            <div className="componentsProjects">
                <p>Проекты</p>
                {loadingProjects === 'loading' && <Loader />}
                {loadingProjects === 'error' && <p> бекенд отвалился</p>}
                {loadingProjects === 'loaded' && <>
                        {projects.map(project =>
                            <ProjectCard id={project.id} 
                            name={project.name}
                            picked={pickedProject.id === project.id && true || false}
                            onClick={() => {setcomponentVulnerabilities([]); setPickedProject(project); getProjectComponents(project.id)}}>
                            </ProjectCard>)}
                        </>}
            </div>

            <div className="componentsComponents">
                <p>Компоненты</p>

                <div >
                    <img src={filterLogo} alt="" className="filterLogo"/>
                    <input type="text" className="componentFilter" placeholder="Название" onChange={e => setFilterComponents({...filterComponents, address: e.target.value})} value={filterComponents.address}/>
                    <input type="text" className="componentFilter" placeholder="Статус" onChange={e => setFilterComponents({...filterComponents, status: e.target.value})} value={filterComponents.status}/>
                    <button onClick={() => setFilterComponents({ address: '', status:'' })} className="clearFilter">Очистить</button>
                </div>

                {pickedProject.id === '' && <p> Выберете проект</p>}
                {pickedProject.id !== '' && loadingComponents === 'loading' && <p> Loading components...</p>}
                {loadingComponents === 'error' && <p> бекенд отвалился</p>}
                {loadingComponents === 'loaded' && <>
                <Button style={"componentVulnerabilities"} onClick={() => checkLicenses() }> Проверить лицензии </Button>

                {components.length === 0 && loadingComponents === 'loaded' && <p> Компоненты не найдены</p>}
                        {filteredComponents.map(component =>
                            <ComponentCard id={component.id} 
                            name={component.address}
                            status={component.status}
                            license_number={component.licenses ? component.licenses.length : 0}
                            osv_vuln_number={component.osv_vuln_count}
                            bdu_vuln_number={component.bdu_vuln_count}
                            picked={pickedComponent.id === component.id && true || false}
                            onClick={() => {setcomponentVulnerabilities([]); setPickedComponent(component); setIsChangeModalOpen(true)}}>
                            </ComponentCard>)}
                        </>}
            <Modal isOpen={isChangeModalOpen} onClose={closeChangeModal}> 
                <div className="changeModalComponents">
                    <div className="changeModalComponentsParams">
                        <p>Проект: {pickedProject.name}</p>
                        <p>Путь в проекте: {pickedComponent.path}</p>
                        <p>Тип: {pickedComponent.type}</p>
                        <p>Адрес: {pickedComponent.address}</p>
                        <p>Тег: {pickedComponent.tag}</p>
                        <p>Версия: {pickedComponent.version}</p>
                        <p>Score: {pickedComponent.score}</p>
                        <p>Статус: {pickedComponent.status}</p>
                            <div>
                            Лицензии: 
                            {pickedComponent.licenses && pickedComponent.licenses.length > 0 ? (
                                <ul className="license">
                                    {pickedComponent.licenses.map((license) => (
                                        <li className="license" key={license.id}>
                                            <p>Название: {license.name}</p>
                                            <p>Ключ: {license.key}</p>
                                            <p>SPDX ID: {license.spdx_id}</p>
                                            <p>URL: {license.url !== "None" ? <a href={license.url} target="_blank" rel="noopener noreferrer">{license.url}</a> : "Нет ссылки"}</p>
                                            <p><Button style={"projectReject"} onClick={() => openAcceptModalWithAction(() => deleteLicense(license.id))}> Удалить </Button></p>
                                        </li>
                                        
                                    ))}
                                </ul>
                            ) : (
                                <> Лицензий не найдено</>
                            )}
                            <p>Добавить лицензию</p>
                        <textarea name="newLicense"
                            id={pickedComponent.id}
                            placeholder='Название'
                            className="license"
                            value={newLicense.name}
                            onChange={e => setNewLicense({...newLicense, name: e.target.value})}
                            > 
                        </textarea>
                        <textarea name="newLicense"
                            id={pickedComponent.id}
                            placeholder='Ключ'
                            className="license"
                            value={newLicense.key}
                            onChange={e => setNewLicense({...newLicense, key: e.target.value})}
                            > 
                        </textarea>
                        <textarea name="newLicense"
                            id={pickedComponent.id}
                            placeholder='SPDX ID'
                            className="license"
                            value={newLicense.spdx_id}
                            onChange={e => setNewLicense({...newLicense, spdx_id: e.target.value})}
                            > 
                        </textarea>
                        <textarea name="newLicense"
                            id={pickedComponent.id}
                            placeholder='URL'
                            className="license"
                            value={newLicense.url}
                            onChange={e => setNewLicense({...newLicense, url: e.target.value})}
                            > 
                        </textarea>
                        <p><Button style={"projectAccept"} onClick={() => addLicense()}> Добавить </Button></p>
                        </div>
                    </div>
                    <div className="changeModalComponentVulnerabilitiesButton">
                        <Button style={"componentVulnerabilities"} onClick={() => {setShowedVunls('osv'); showComponentVulnerabilities()} }> Показать уязвимости OSV </Button>
                    </div>
                    <div className="changeModalComponentVulnerabilitiesButton">
                        <Button style={"componentVulnerabilities"} onClick={() => {setShowedVunls('bdu'); showComponentVulnerabilitiesBdu()} }> Показать уязвимости БДУ </Button>
                    </div>
                    <div className="changeModalProjectsButtons">
                        
                        <select className="componentSelect" name="" id="" onChange={handleSelectStatus}>
                            <option value="" disabled selected hidden>Изменить статус</option>
                            <option value="none">none</option>
                            <option value="confirmed">confirmed</option>
                            <option value="denied">denied</option>
                        </select>
                        <Button style={"projectAccept"} onClick={() => openAcceptModalWithAction(changeComponentStatus)}> Изменить </Button>
                        <Button style={"projectClose"} onClick={closeChangeModal}> Закрыть </Button>
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
            </div>

            <div className="componentsVulnerabilities">

                    <p>Уязвимости</p>

                    {pickedProject.id !== '' && pickedComponent.id !== '' && componentVulnerabilities.length === 0 && <p> Уязвимости не найдены</p>}
                    {showedVunls == 'osv' && <>
                    <div >
                        <img src={filterLogo} alt="" className="filterLogo"/>
                        <input type="text" className="vulnerabilityFilter" placeholder="OSV id" onChange={e => setFilterVulnerabilities({...filterVulnerabilities, osv_id: e.target.value})} value={filterVulnerabilities.osv_id}/>
                        <button onClick={() => setFilterVulnerabilities({ osv_id: '' })} className="clearFilter">Очистить</button>
                    </div>
                    {filteredVulnerabilities.map(vuln =>
                            <VulnerabilityCard id={vuln.id} 
                            name={vuln.osv_id}
                            onClick={() => {setPickedVulnerability(vuln); setIsVulnerabilityModalOpen(true)}}
                            picked={pickedVulnerability.id === vuln.id && true || false}
                            severity={vuln.full_data.severity && 
                                [vuln.full_data.severity[0].calculated_severities.base_severity, 
                                 vuln.full_data.severity[0].calculated_severities.environmental_severity,
                                 vuln.full_data.severity[0].calculated_severities.temporal_severity] || []}
                            >
                            </VulnerabilityCard>)}
                            </>}
                    {showedVunls == 'bdu' && <>
                    <div >
                        <img src={filterLogo} alt="" className="filterLogo"/>
                        <input type="text" className="vulnerabilityFilter" placeholder="BDU id" onChange={e => setFilterVulnerabilitiesBdu({...filterVulnerabilities, bdu_id: e.target.value})} value={filterVulnerabilitiesBdu.bdu_id}/>
                        <button onClick={() => setFilterVulnerabilitiesBdu({ bdu_id: '' })} className="clearFilter">Очистить</button>
                    </div>
                    {filteredVulnerabilities.map(vuln =>
                            <VulnerabilityCardBdu id={vuln.id} 
                            name={vuln.bdu_id}
                            onClick={() => {setPickedVulnerability(vuln); setIsVulnerabilityModalOpen(true)}}
                            picked={pickedVulnerability.id === vuln.id && true || false}
                            severity={vuln.severity}
                            >
                            </VulnerabilityCardBdu>)}
                            </>}
            </div>
            <Modal isOpen={isVulnerabilityModalOpen} onClose={closeVulnerabilityModal}> 
                {pickedVulnerability && showedVunls == 'osv' && <div className="vulnerabilityModal">
                    <div className="vulnerabilityModalInfo">
                        <p> <b>OSV id: </b>{pickedVulnerability.full_data.id}</p>
                        <p> <b>Описание: </b>{pickedVulnerability.full_data.details}</p>
                        {pickedVulnerability.full_data.severity && <p><b>Severity: </b>
                            <br /> base_severity: {pickedVulnerability.full_data.severity[0].calculated_severities.base_severity} 
                            <br /> environmental_severity: {pickedVulnerability.full_data.severity[0].calculated_severities.environmental_severity}
                            <br /> temporal_severity: {pickedVulnerability.full_data.severity[0].calculated_severities.temporal_severity}
                            <br /> score: {pickedVulnerability.full_data.severity[0].score}</p>
                        || <p><b>Severity: </b>Не найдено</p>}
                        <p><b>Ссылки: </b>{pickedVulnerability.full_data.references.map(reference => 
                            <>
                            <br />
                            Тип: {reference.type} <br />
                            Url: {reference.url}<br />
                            </>)}</p>
                        <p><b>Подверженные версии: </b>{pickedVulnerability.full_data.affected[0].versions && pickedVulnerability.full_data.affected[0].versions.map(version => <>| {version} </>) || "Не найдено"}</p>

                    </div>
                    <div className="changeModalProjectsButtons">
                        
                        <Button style={"projectClose"} onClick={closeVulnerabilityModal}> Закрыть </Button>
                    </div>
                </div>}
                {pickedVulnerability && showedVunls == 'bdu' && <div className="vulnerabilityModal">
                    <div className="vulnerabilityModalInfo">
                        <p> <b>BDU id: </b>{pickedVulnerability.bdu_id}</p>
                        <p> <b>CVE id: </b>{pickedVulnerability.cve_id}</p>
                        <p> <b>Название: </b>{pickedVulnerability.name}</p>
                        <p> <b>Описание: </b>{pickedVulnerability.description}</p>
                        <p> <b>Статус: </b>{pickedVulnerability.status}</p>
                        <p> <b>Severity: </b>{pickedVulnerability.bdu_severity}</p>
                    </div>
                    <div className="changeModalProjectsButtons">
                        <Button style={"projectClose"} onClick={closeVulnerabilityModal}> Закрыть </Button>
                    </div>
                </div>}
            </Modal>
        </>
    );
}
