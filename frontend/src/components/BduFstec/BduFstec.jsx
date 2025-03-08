import React, { version } from "react";
import { useState, useEffect, useContext} from "react";
import "./BduFstec.css";
import Button from "../Button/Button";
import { apiGetProjectComponents, apiChangeComponentStatus } from "../../services/apiComponents";
import { apiGetComponentVulnerabilities } from "../../services/apiVulnerabilities";
import { apiGetBduInfo, apiGetBduComponentVulns, apiUpdateBdu, apiUpdateBduVulns} from "../../services/apiBduFstec";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import Loader from "../Loader/Loader";

export default function BduFstec() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
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
        }
    }

    async function updateBdu() {
        setNotificationData({message:'Выполняется обновление БДУ', type: 'success'})
        toggleNotificationFunc()
        setLoaderActive(true)
        setDisableButtons(true)

        try {
            const response = await apiUpdateBdu()
            if (response.status == 200) {
                setLoaderActive(false)
                getBduInfo()
                setNotificationData({message:'БДУ обновлена', type: 'success'})
                toggleNotificationFunc()
                setDisableButtons(false)
            } else {
                setLoaderActive(false)
                setNotificationData({message:'Не удалось обновить БДУ', type: 'error'})
                toggleNotificationFunc()
                setDisableButtons(false)
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
            setDisableButtons(false)
        }
    }

    async function updateBduVulns() {
        setNotificationData({message:'Выполняется поиск уязвимостей, ожидайте', type: 'success'})
        toggleNotificationFunc()
        setLoaderActive(true)
        setDisableButtons(true)
        try {
            const response = await apiUpdateBduVulns()
            if (response.status == 200) {
                setLoaderActive(false)
                getBduInfo()
                setNotificationData({message:'Поиск завершен', type: 'success'})
                toggleNotificationFunc()
                setDisableButtons(false)
            } else {
                setLoaderActive(false)
                setNotificationData({message:'Не удалось выполнить поиск', type: 'error'})
                toggleNotificationFunc()
                setDisableButtons(false)
            }
        } catch (error) {
            setLoaderActive(false)
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
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
