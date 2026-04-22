import React, { version } from "react";
import { useState, useEffect, useContext} from "react";
import "./BduFstec.css";
import Button from "../Button/Button";
import { apiGetProjectComponents, apiChangeComponentStatus } from "../../services/apiComponents";
import { apiGetComponentVulnerabilities } from "../../services/apiVulnerabilities";
import { apiGetBduInfo, apiGetBduComponentVulns, apiUpdateBdu, apiUpdateBduVulns} from "../../services/apiBduFstec";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import Loader from "../Loader/Loader";

export default function BduFstec() {

    const { addMessage } = useTimedMessagesContext();
    const [ loaderActive, setLoaderActive ] = useState(false)
    const [ disableButtons, setDisableButtons ] = useState(false)
    
    const [bduInfo, setBduInfo] = useState('')
    const [loading, setLoading] = useState('loading')


    async function getBduInfo() {
        try {
            setLoading('loading')
            const bduInfo = await apiGetBduInfo()
            setBduInfo(bduInfo)
            setLoading('loaded')
        } catch (err) {
            setLoading('error')
            addMessage('Ошибка при загрузке БДУ: ' + err.message, 'error', 5000)
        }
    }

    async function updateBdu() {
        addMessage('Выполняется обновление БДУ', 'info', 3000)
        setLoaderActive(true)
        setDisableButtons(true)

        try {
            const response = await apiUpdateBdu()
            if (response.status == 200) {
                setLoaderActive(false)
                getBduInfo()
                addMessage('БДУ обновлена', 'success', 3000)
                setDisableButtons(false)
            } else {
                setLoaderActive(false)
                addMessage('Не удалось обновить БДУ', 'error', 3000)
                setDisableButtons(false)
            }
        } catch (error) {
            setLoaderActive(false)
            addMessage(`Ошибка при обновлении БДУ: ${error.message}`, 'error', 5000)
            setDisableButtons(false)
        }
    }

    async function updateBduVulns() {
        addMessage('Выполняется поиск уязвимостей, ожидайте', 'info', 3000)
        setLoaderActive(true)
        setDisableButtons(true)
        try {
            const response = await apiUpdateBduVulns()
            if (response.status == 200) {
                setLoaderActive(false)
                getBduInfo()
                addMessage('Поиск завершен', 'success', 3000)
                setDisableButtons(false)
            } else {
                setLoaderActive(false)
                addMessage('Не удалось выполнить поиск', 'error', 3000)
                setDisableButtons(false)
            }
        } catch (error) {
            setLoaderActive(false)
            addMessage(`Ошибка при поиске уязвимостей: ${error.message}`, 'error', 5000)
            setDisableButtons(false)
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
            addMessage('Ошибка при загрузке компонентов проекта: ' + err.message, 'error', 5000)
        }
    }

    async function showComponentVulnerabilities() {
        try {
            const vulnerabilities = await apiGetComponentVulnerabilities(pickedComponent.id)
            setcomponentVulnerabilities(vulnerabilities)
        } catch (err) {
            setcomponentVulnerabilities([])
            addMessage(`Ошибка при загрузке уязвимостей компонента: ${err.message}`, 'error', 5000)
        }
        closeChangeModal()
    }

    async function changeComponentStatus() {
        console.log(pickedComponent.id)
        console.log(newComponentStatus)
        if (newComponentStatus == '') {
            addMessage('Выберете новый статус', 'error', 3000)
            return 0
        }
        try {
            const response = await apiChangeComponentStatus(pickedComponent.id, newComponentStatus)
            if (response.status == 200) {
                getProjectComponents(pickedProject.id)
                setNewComponentStatus('')
                addMessage('Статус изменен', 'success', 3000)
                closeChangeModal()
                closeAcceptModal()
            } else {
                setNewComponentStatus('')
                addMessage('Не удалось изменить статус', 'error', 3000)
                closeChangeModal()
                closeAcceptModal()
            }
        } catch (error) {
            addMessage(`Ошибка при изменении статуса: ${error.message}`, 'error', 5000)
            setNewComponentStatus('')
        }
    }





    useEffect(() => {
        getBduInfo()
        }, [])


    return (
        <>
            {loaderActive && <Loader />}
            <div className="main-bdu">
                {loading === 'loading' && <Loader />}
                {loading === 'error' && <p> бекенд отвалился</p>}
                {loading === 'loaded' && <>
                        <div className="bduInfo">
                            <p>Последняя синхронизация БДУ: <b>{bduInfo.last_update}</b></p>
                            <p>Уязвимостей из БДУ найдено: <b>{bduInfo.vuln_count}</b></p>
                            <Button 
                                style={disableButtons ? "componentVulnerabilities-disabled" : "componentVulnerabilities"} 
                                onClick={() => updateBdu()} 
                                disabled={disableButtons || false}
                            >
                                Обновить БДУ
                            </Button>
                        <br />
                            <Button 
                                style={disableButtons ? "componentVulnerabilities-disabled" : "componentVulnerabilities"} 
                                onClick={() => updateBduVulns()} 
                                disabled={disableButtons || false}
                            >
                                Найти  уязвимости
                            </Button>
                        </div>
                        </>}
            </div> 
        </>
    );
}
