import React, { version } from "react";
import { useState, useEffect, useContext } from "react";
import "./Bitbake.css";
import Button from "../Button/Button";
import { apiGetBitbakeProjects, apiGetBitbakeProjectComponents, apiGetBitbakeComponentVulnerabilities } from "../../services/apiBitbake";
import { apiGetBduComponentVulns } from "../../services/apiBduFstec";
import { apiCheckLicenses, apiAddLicense, apiDeleteLicense } from "../../services/apiLicenses";
import { apiGetComponentComments, apiAddComponentComment, apiDeleteComponentComment } from "../../services/apiComments";
import ProjectCard from "../Projects/ProjectCard/ProjectCard";
import LayerCard from "./LayerCard/LayerCard";
import BitbakeComponentCard from "./BitbakeComponentCard/ComponentCard";
import CommentCard from "./CommentCard/CommentCard";
import BitbakeVulnerabilityCard from "./BitbakeVulnerabilityCard/BitbakeVulnerabilityCard";
import VulnerabilityCardBdu from "./VulnerabilityCardBdu/VulnerabilityCardBdu";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import filterLogo from './filter.png'
import sendLogo from './send.png'
import Loader from "../Loader/Loader";
import { useAuthContext } from "../../hooks/useAuthContext";

export default function Bitbake() {
    const { userName, userId } = useAuthContext();
    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
    const [loaderActive, setLoaderActive] = useState(false)

    const [loadingProjects, setLoadingProjects] = useState('loading')
    const [projects, setProjects] = useState([])
    const [pickedProject, setPickedProject] = useState({ id: '', name: '' })
    const [pickedLayer, setPickedLayer] = useState('')


    const [loadingComponents, setLoadingComponents] = useState('loading')
    const [components, setComponents] = useState([{ address: '' }])
    const [pickedComponent, setPickedComponent] = useState({ id: '' })
    const [newLicense, setNewLicense] = useState({ component_id: '', key: '', name: '', spdx_id: '', url: '' })
    const [componentVulnerabilities, setcomponentVulnerabilities] = useState([])
    const [pickedVulnerability, setPickedVulnerability] = useState('')
    const [showedVunls, setShowedVunls] = useState(false)

    const [componentComments, setComponentComments] = useState([{ id: 0 }])
    const [componentComment, setComponentComment] = useState({ user_id: userId, comment: '' })
    const [pickedComment, setPickedComment] = useState({ id: '' })

    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);
    const [isVulnerabilityModalOpen, setIsVulnerabilityModalOpen] = useState(false);
    const [showHint, setShowHint] = useState(false);


    const [actionFunction, setActionFunction] = useState(null);


    const [filterComponents, setFilterComponents] = useState({ name: '' });
    const [hidePatched, setHidePatched] = useState(false);
    const [filterVulnerabilities, setFilterVulnerabilities] = useState({ cve: '' });
    const [filterVulnerabilitiesBdu, setFilterVulnerabilitiesBdu] = useState({ bdu_id: '' });


    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    function closeChangeModal() {
        setIsChangeModalOpen(false);
        setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' })
        setComponentComment({ user_id: userId, comment: '' })
    }

    function closeAcceptModal() {
        setPickedVulnerability('')
        setIsAcceptModalOpen(false);
        setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' })
    }

    function closeVulnerabilityModal() {
        setPickedVulnerability('')
        setIsVulnerabilityModalOpen(false);
        setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' })
    }

    async function getProjects() {
        try {
            setLoadingProjects('loading')
            const projects = await apiGetBitbakeProjects()
            setProjects(projects)
            setLoadingProjects('loaded')
        } catch (err) {
            setLoadingProjects('error')
        }
    }

    async function getProjectComponents(id, layer) {
        try {
            setLoadingComponents('loading');
            const components = await apiGetBitbakeProjectComponents(id, layer);
            const sortedComponents = components.sort((a, b) => b.cve_count - a.cve_count);
            setComponents(sortedComponents);
            setLoadingComponents('loaded');
        } catch (err) {
            setComponents([]);
            setLoadingComponents('error');
        }
    }

    async function showComponentVulnerabilities() {
        try {
            const vulnerabilities = await apiGetBitbakeComponentVulnerabilities(pickedComponent.id)
            setcomponentVulnerabilities(vulnerabilities)
        } catch (err) {
            setcomponentVulnerabilities([])
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
        }
        closeChangeModal()
    }

    async function showComponentVulnerabilities() {
        try {
            const vulnerabilities = await apiGetBitbakeComponentVulnerabilities(pickedComponent.id)
            setcomponentVulnerabilities(vulnerabilities)
        } catch (err) {
            setcomponentVulnerabilities([])
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
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
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
        }
        closeChangeModal()
    }


    async function checkLicenses() {
        setNotificationData({ message: 'Выполняется поиск лицензий', type: 'success' })
        toggleNotificationFunc()
        setLoaderActive(true)

        try {
            const response = await apiCheckLicenses(pickedProject.id)
            if (response.status == 200) {
                setLoaderActive(false)
                getProjectComponents(pickedProject.id)
                setNotificationData({ message: 'Поиск завершен', type: 'success' })
                toggleNotificationFunc()
            } else {
                setLoaderActive(false)
                setNotificationData({ message: 'Не удалось выполнить поиск лицензий', type: 'error' })
                toggleNotificationFunc()
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
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
                setNotificationData({ message: 'Лицензия удалена', type: 'success' })
                toggleNotificationFunc()
            } else {
                setLoaderActive(false)
                setNotificationData({ message: 'Не удалось удалить лицензию', type: 'error' })
                toggleNotificationFunc()
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
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
                setNotificationData({ message: 'Лицензия добавлена', type: 'success' })
                toggleNotificationFunc()
                setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' })
            } else {
                setLoaderActive(false)
                setNotificationData({ message: 'Не удалось добавить лицензию', type: 'error' })
                toggleNotificationFunc()
                setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' })
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
            setNewLicense({ component_id: '', key: '', name: '', spdx_id: '', url: '' })
        }
    }

    async function getComponentComments(component_id) {
        try {
            const comments = await apiGetComponentComments(component_id)
            setComponentComments(comments)
            console.log(comments)
        } catch (err) {
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
            setComponentComments([{ id: 0 }])
        }
    }

    async function addComponentComment() {
        if (componentComment.comment === '') {
            setNotificationData({ message: 'Введите комментарий', type: 'error' })
            toggleNotificationFunc()
            return 1
        }
        setLoaderActive(true)
        try {
            const response = await apiAddComponentComment(userId, pickedComponent.id, componentComment.comment)
            if (response.status == 200) {
                setLoaderActive(false)
                getComponentComments(pickedComponent.id)
                setNotificationData({ message: 'Комментарий добавлен', type: 'success' })
                toggleNotificationFunc()
                setComponentComment({ user_id: userId, comment: '' })
                setPickedComment({ id: '' })
            } else {
                setLoaderActive(false)
                setNotificationData({ message: 'Не удалось добавить комментарий', type: 'error' })
                toggleNotificationFunc()
                setComponentComment({ user_id: userId, comment: '' })
                setPickedComment({ id: '' })
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
            setComponentComment({ user_id: userId, comment: '' })
            setPickedComment({ id: '' })
        }
    }

    async function deleteComponentComment() {
        setLoaderActive(true)
        try {
            const response = await apiDeleteComponentComment(pickedComment.id)
            if (response.status == 200) {
                setLoaderActive(false)
                getComponentComments(pickedComponent.id)
                setNotificationData({ message: 'Комментарий удален', type: 'success' })
                toggleNotificationFunc()
                setComponentComment({ user_id: userId, comment: '' })
                setPickedComment({ id: '' })
            } else {
                setLoaderActive(false)
                setNotificationData({ message: 'Не удалось удалить комментарий', type: 'error' })
                toggleNotificationFunc()
                setComponentComment({ user_id: userId, comment: '' })
                setPickedComment({ id: '' })
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' })
            toggleNotificationFunc()
            setComponentComment({ user_id: userId, comment: '' })
            setPickedComment({ id: '' })
        }
    }

    const filteredComponents = components.filter(item => {
        return (
            (filterComponents.name === '' || item.name.includes(filterComponents.name))
        );
    }
    )

    const filteredVulnerabilities = componentVulnerabilities.filter(item => {
        if (showedVunls == 'cve') {
            return (
                (filterVulnerabilities.cve === '' || item.cve.includes(filterVulnerabilities.cve)) &&
                (!hidePatched || item.status !== "Patched")
            );
        }
        if (showedVunls == 'bdu') {
            return (
                (filterVulnerabilitiesBdu.bdu_id === '' || item.bdu_id.includes(filterVulnerabilitiesBdu.bdu_id))
            );
        }
    });
    useEffect(() => {
        getProjects()
    }, [])


    return (
        <>
            {loaderActive && <Loader />}
            <div className="bitbakeProjects">
                <p>Проекты</p>
                {loadingProjects === 'loading' && <Loader />}
                {loadingProjects === 'error' && <p> бекенд отвалился</p>}
                {loadingProjects === 'loaded' && <>
                    {projects.map(project =>
                        <ProjectCard id={project.id}
                            name={project.name}
                            picked={pickedProject.id === project.id && true || false}
                            onClick={() => { setcomponentVulnerabilities([]); setPickedLayer(''); setPickedProject(project) }}>
                        </ProjectCard>)}
                </>}
            </div>
            <div className="bitbakeLayers">
                <p>Слои</p>
                {!pickedProject.id && <p> Выберете проект </p>}
                {pickedProject.id && <>
                    {pickedProject.layers.map(layer =>
                        <LayerCard id={layer}
                            name={layer}
                            picked={pickedLayer === layer && true || false}
                            onClick={() => { setcomponentVulnerabilities([]); setPickedLayer(layer); getProjectComponents(pickedProject.id, layer) }}>
                        </LayerCard>)}
                </>}

            </div>

            <div className="bitbakeComponents">
                <p>Компоненты</p>

                <div >
                    <img src={filterLogo} alt="" className="filterLogo" />
                    <input type="text" className="componentFilter" placeholder="Название" onChange={e => setFilterComponents({ ...filterComponents, name: e.target.value })} value={filterComponents.name} />
                    <button onClick={() => setFilterComponents({ name: '' })} className="bitbakeClearFilter">Очистить</button>
                </div>

                {pickedProject.id && !pickedLayer && <p> Выберете слой</p>}
                {pickedLayer && loadingComponents === 'loading' && <p> Loading components...</p>}
                {loadingComponents === 'error' && <p> бекенд отвалился</p>}
                {loadingComponents === 'loaded' && <>

                    {filteredComponents.length === 0 && loadingComponents === 'loaded' && <p> Компоненты не найдены</p>}
                    {filteredComponents.map(component =>
                        <BitbakeComponentCard id={component.id}
                            name={component.name}
                            license_number={component.licenses ? component.licenses.length : 0}
                            osv_vuln_number={component.cve_count}
                            bdu_vuln_number={component.bdu_vuln_count}
                            picked={pickedComponent.id === component.id && true || false}
                            onClick={() => { setcomponentVulnerabilities([]); setPickedComponent(component); getComponentComments(component.id); setIsChangeModalOpen(true) }}>
                        </BitbakeComponentCard>)}
                </>}

                <Modal isOpen={isChangeModalOpen} onClose={closeChangeModal}>
                    <div className="changeModalComponents">
                        <div className="changeModalComponentsParams">
                            <p>Проект: {pickedProject.name}</p>
                            <p>Название: {pickedComponent.name}</p>
                            <p>Версия: {pickedComponent.version}</p>
                            <p>Слой: {pickedComponent.layer}</p>
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
                                <p>Добавление лицензий для Bitbake в разработке</p>
                                <textarea name="newLicense"
                                    id={pickedComponent.id}
                                    placeholder='Название'
                                    className="license"
                                    value={newLicense.name}
                                    onChange={e => setNewLicense({ ...newLicense, name: e.target.value })}
                                >
                                </textarea>
                                <textarea name="newLicense"
                                    id={pickedComponent.id}
                                    placeholder='Ключ'
                                    className="license"
                                    value={newLicense.key}
                                    onChange={e => setNewLicense({ ...newLicense, key: e.target.value })}
                                >
                                </textarea>
                                <textarea name="newLicense"
                                    id={pickedComponent.id}
                                    placeholder='SPDX ID'
                                    className="license"
                                    value={newLicense.spdx_id}
                                    onChange={e => setNewLicense({ ...newLicense, spdx_id: e.target.value })}
                                >
                                </textarea>
                                <textarea name="newLicense"
                                    id={pickedComponent.id}
                                    placeholder='URL'
                                    className="license"
                                    value={newLicense.url}
                                    onChange={e => setNewLicense({ ...newLicense, url: e.target.value })}
                                >
                                </textarea>
                                {/* <p><Button style={"projectAccept"} onClick={() => addLicense()}> Добавить </Button></p> */}
                            </div>
                        </div>
                        <div className="changeModalComponentVulnerabilitiesButton">
                            <Button style={"componentVulnerabilities"} onClick={() => { setShowedVunls('cve'); showComponentVulnerabilities() }}> Показать уязвимости CVE </Button>
                        </div>
                        {/* <div className="changeModalComponentVulnerabilitiesButton">
                            <Button style={"componentVulnerabilities"} onClick={() => { setShowedVunls('bdu'); showComponentVulnerabilitiesBdu() }}> Показать уязвимости БДУ </Button>
                        </div> */}
                        <div className="changeModalProjectsButtons">
                            <Button style={"projectClose"} onClick={closeChangeModal}> Закрыть </Button>
                        </div>
                    </div>
                    <div className="changeModalComments">Комментарии
                        <div className="comments">
                            {componentComments.map(comment =>
                                <CommentCard
                                    id={comment.id}
                                    onClick={() => { if (pickedComment.id == !comment.id) { setPickedComment(comment) } else { setPickedComment({ id: '' }) } }}
                                    picked={pickedComment.id === comment.id && true || false}
                                    user={comment.user_name}
                                    datetime={comment.datetime}
                                    text={comment.comment}
                                    deleteFunction={() => deleteComponentComment()}
                                    owner={comment.user_name === userName && true || false}
                                >
                                </CommentCard>
                            )}
                        </div>
                        <textarea className="comments"
                            id={pickedComponent.id}
                            // placeholder='Комментарий'
                            placeholder='Комментарии для Bitbake в разработке'
                            value={componentComment.comment}
                            onChange={e => setComponentComment({ ...componentComment, comment: e.target.value })}>
                        </textarea>
                        {/* <div className="sendLogo">
                            <img src={sendLogo} alt="" className="sendLogo" onClick={addComponentComment} />
                        </div> */}
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

            <div className="bitbakeVulnerabilities">

                <p>Уязвимости</p>

                {/* {pickedProject.id !== '' && pickedComponent.id !== '' && componentVulnerabilities.length === 0 && showedVunls && <p> Уязвимости не найдены</p>} */}
                {showedVunls == 'cve' && <>
                    <div >
                        <img src={filterLogo} alt="" className="filterLogo" />
                        <input type="text" className="bitbakeVulnerabilityFilter" placeholder="CVE id" onChange={e => setFilterVulnerabilities({ ...filterVulnerabilities, cve: e.target.value })} value={filterVulnerabilities.cve} />
                        <button onClick={() => setFilterVulnerabilities({ cve: '' })} className="bitbakeClearFilter">Очистить</button>
                    </div>
                    <div className="custom-checkbox">
                        <input
                            type="checkbox"
                            id="checkbox1"
                            checked={console.log('checked')}
                            onChange={() => {
                                setHidePatched((prev) => !prev);
                            }}
                        />
                        <label htmlFor="checkbox1">Скрыть Patched</label>
                        <button
                            onClick={() => {
                                setShowHint((prev) => !prev);
                            }}
                            className={showHint ? "showHintActivated" : "showHint"}
                        >
                            ?
                        </button>
                        {showHint &&
                            <div className="hintBox">
                                <p>
                                    Статус <strong>Patched</strong> означает, что был применен файл
                                    исправления для устранения проблемы безопасности.
                                </p>
                                <p>
                                    Статус <strong>Unpathed</strong> означает, что исправления
                                    для устранения проблемы не применялись и что проблему необходимо
                                    изучить.
                                </p>
                                <p>
                                    Статус <strong>Ignored</strong> означает, что после
                                    анализа было решено игнорировать проблему, поскольку она, например,
                                    затрагивает программный компонент на другой платформе операционной
                                    системы.
                                </p>
                            </div>
                        }
                    </div>

                    {filteredVulnerabilities.map(vuln =>
                        <BitbakeVulnerabilityCard id={vuln.id}
                            name={vuln.cve}
                            onClick={() => { setPickedVulnerability(vuln); setIsVulnerabilityModalOpen(true) }}
                            picked={pickedVulnerability.id === vuln.id && true || false}
                            severity={vuln.severity}
                            status={vuln.status}
                        >
                        </BitbakeVulnerabilityCard>)}
                </>}
                {showedVunls == 'bdu' && <>
                    <div >
                        <img src={filterLogo} alt="" className="filterLogo" />
                        <input type="text" className="vulnerabilityFilter" placeholder="BDU id" onChange={e => setFilterVulnerabilitiesBdu({ ...filterVulnerabilities, bdu_id: e.target.value })} value={filterVulnerabilitiesBdu.bdu_id} />
                        <button onClick={() => setFilterVulnerabilitiesBdu({ bdu_id: '' })} className="bitbakeClearFilter">Очистить</button>
                    </div>
                    {filteredVulnerabilities.map(vuln =>
                        <VulnerabilityCardBdu id={vuln.id}
                            name={vuln.bdu_id}
                            onClick={() => { setPickedVulnerability(vuln); setIsVulnerabilityModalOpen(true) }}
                            picked={pickedVulnerability.id === vuln.id && true || false}
                            severity={vuln.severity}
                        >
                        </VulnerabilityCardBdu>)}
                </>}
            </div>
            <Modal isOpen={isVulnerabilityModalOpen} onClose={closeVulnerabilityModal}>
                {pickedVulnerability && showedVunls == 'cve' && <div className="vulnerabilityModal">
                    <div className="vulnerabilityModalInfo">
                        <p> <b>CVE id: </b>{pickedVulnerability.cve}</p>
                        <p> <b>Статус: </b>{pickedVulnerability.status}</p>
                        <p> <b>Описание: </b>{pickedVulnerability.summary}</p>
                        <p> <b>CVSS v3: </b>{pickedVulnerability.cvss_v3}</p>
                        <p> <b>Severity: </b>{pickedVulnerability.severity}</p>
                        <p> <b>Вектор: </b>{pickedVulnerability.vector}</p>
                        <p><b>Больше информации: </b>{pickedVulnerability.more_information}</p>

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
