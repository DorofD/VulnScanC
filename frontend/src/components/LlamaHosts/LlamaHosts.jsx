import React, { Component } from "react";
import { useState, useEffect } from "react";
import "./LlamaHosts.css";
import LlamaHostCard from "./LlamaHostCard/LlamaHostCard";
import Button from "../Button/Button";
import Filter from "../Filter/Filter";
import { apiGetLlamaHosts, apiAddLlamaHost, apiChangeLlamaHost, apiDeleteLlamaHost } from "../../services/apiLlamaHosts";
// // import { useNotificationContext } from "../../hooks/useNotificationContext";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import Loader from "../Loader/Loader";

export default function LlamaHosts() {
    const { messages, addMessage } = useTimedMessagesContext();

    const [loaderActive, setLoaderActive] = useState(false)

    const [hosts, setHosts] = useState([])
    const [loading, setLoading] = useState('loading')
    const [pickedHost, setPickedHost] = useState({ id: '', name: '', api_url: '', model_type: '', description: '' })
    const [newHost, setNewHost] = useState({ name: '', api_url: '', model_type: '', description: '' })
    const [changedHost, setChangedHost] = useState({ id: '', name: '', api_url: '', model_type: '', description: '' })

    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);

    const [actionFunction, setActionFunction] = useState(null);
    const [filterHosts, setFilterHosts] = useState({ name: '', model_type: '', api_url: '' });
    const [additionalText, setAdditionalText] = useState([]);

    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    function closeAddModal() {
        setIsAddModalOpen(false);
        setNewHost({ name: '', api_url: '', model_type: '', description: '' })
    }

    function closeChangeModal() {
        setIsChangeModalOpen(false);
        setChangedHost({ id: '', name: '', api_url: '', model_type: '', description: '' })
        setAdditionalText([])
    }

    function closeAcceptModal() {
        setIsAcceptModalOpen(false);
    }


    async function getHosts() {
        try {
            setLoading('loading')
            const response = await apiGetLlamaHosts()
            const data = await response.json()
            const hosts = data.llama_hosts || []
            setHosts(hosts)
            setLoading('loaded')
        } catch (err) {
            setLoading('error')
        }
    }

    async function addHost() {
        if (!newHost.api_url) {
            addMessage('Введите API URL', 'warning', 3000)
            return false
        }

        if (!newHost.model_type) {
            addMessage('Выберите тип модели', 'warning', 3000)
            return false
        }

        const response = await apiAddLlamaHost(newHost)
        if (response.status == 200) {
            getHosts()
            closeAddModal()
            addMessage('Хост добавлен', 'success', 3000)

        } else {
            addMessage('Не удалось добавить хост', 'error', 3000)
        }
    }


    function validateChanges() {
        let changesDict = {}
        let textList = []
        if (changedHost.name !== pickedHost.name) {
            changesDict.name = changedHost.name
            textList.push(`Имя: ${pickedHost.name} => ${changedHost.name}`)
        }
        if (changedHost.api_url !== pickedHost.api_url) {
            changesDict.api_url = changedHost.api_url
            textList.push(`API URL: ${pickedHost.api_url} => ${changedHost.api_url}`)
        }
        if (changedHost.model_type !== pickedHost.model_type) {
            changesDict.model_type = changedHost.model_type
            textList.push(`Тип модели: ${pickedHost.model_type} => ${changedHost.model_type}`)
        }
        if (changedHost.description !== pickedHost.description) {
            changesDict.description = changedHost.description
            textList.push(`Описание изменено`)
        }
        if (Object.keys(changesDict).length === 0) {
            addMessage('Вы ничего не изменили', 'warning', 3000)
            setAdditionalText([])
            return false
        }

        textList.unshift("Следующие изменения будут применены:")
        setAdditionalText(textList)
        openAcceptModalWithAction(() => changeHost(changesDict))
    }

    async function changeHost(changesDict) {
        try {
            const response = await apiChangeLlamaHost(pickedHost.id, changesDict)
            if (response.status == 200) {
                getHosts()
                closeAcceptModal()
                closeChangeModal()
                addMessage('Хост изменён', 'success', 3000)
                setAdditionalText([])
            } else {
                closeAcceptModal()
                addMessage('Не удалось изменить хост', 'warning', 3000)
                setAdditionalText([])
            }
        }catch (err) {
            setLoaderActive(false)
            console.log(err)
            addMessage(`Что-то пошло не так: ${err.message}`, 'error', 5000)
        }
    }

    async function deleteHost() {
        const response = await apiDeleteLlamaHost(changedHost.id)
        if (response.status == 200) {
            getHosts()
            closeAcceptModal()
            closeChangeModal()
            addMessage('Хост удалён', 'success', 3000)

        } else {
            closeAcceptModal()
            addMessage('Не удалось удалить хост', 'error', 3000)
        }
    }

    const filteredHosts = hosts.filter(item => {
        return (
            (filterHosts.name === '' || (item.name || '').includes(filterHosts.name)) &&
            (filterHosts.model_type === '' || (item.model_type || '').includes(filterHosts.model_type)) &&
            (filterHosts.api_url === '' || (item.api_url || '').includes(filterHosts.api_url))
        );
    })

    useEffect(() => {
        getHosts()
    }, [])

    return (
        <div className="usersContainer">
            <div className="usersHeader">
                <button onClick={() => { setPickedHost({ id: 0, name: '', api_url: '', model_type: '', description: '' }); setIsAddModalOpen(true) }}>Добавить хост</button>
            </div>
            <Filter onClick={() => setFilterHosts({ name: '', model_type: '', api_url: '' })}>
                <input type="text" className="filter" placeholder="Имя" onChange={e => setFilterHosts({ ...filterHosts, name: e.target.value })} value={filterHosts.name} />
                <input type="text" className="filter" placeholder="Тип модели" onChange={e => setFilterHosts({ ...filterHosts, model_type: e.target.value })} value={filterHosts.model_type} />
                <input type="text" className="filter" placeholder="API URL" onChange={e => setFilterHosts({ ...filterHosts, api_url: e.target.value })} value={filterHosts.api_url} />
            </Filter>

            <div className="usersNotes">


                {loading === 'loading' && <Loader />}
                {loading === 'error' && <p> бекенд отвалился</p>}
                {loading === 'loaded' && <>
                    {filteredHosts.map(host =>
                        <LlamaHostCard
                            key={host.id}
                            id={host.id}
                            name={host.name}
                            apiUrl={host.api_url}
                            modelType={host.model_type}
                            picked={pickedHost.id === host.id && true || false}
                            onClick={() => { setPickedHost(host); setChangedHost({ id: host.id, name: host.name, api_url: host.api_url, model_type: host.model_type, description: host.description }); setAdditionalText([]); setIsChangeModalOpen(true) }}>
                        </LlamaHostCard>
                    )}
                </>}
            </div>

            <Modal isOpen={isAddModalOpen} onClose={() => closeAddModal()}>
                <div className="addModalUsers">

                    <div className="addModalUsersHeader">
                        Добавить хост
                    </div>

                    <div className="addModalUsersParams">
                        <div className="addModalUsersParamsValues">
                            <input type="text" className="addModalUsers" placeholder="Имя" onChange={e => setNewHost({ ...newHost, name: e.target.value })} value={newHost.name} />
                            <input type="text" className="addModalUsers" placeholder="API URL" onChange={e => setNewHost({ ...newHost, api_url: e.target.value })} value={newHost.api_url} />
                            <input type="text" className="addModalUsers" placeholder="Тип модели" onChange={e => setNewHost({ ...newHost, model_type: e.target.value })} value={newHost.model_type} />
                            <input type="text" className="addModalUsers" placeholder="Описание" onChange={e => setNewHost({ ...newHost, description: e.target.value })} value={newHost.description} />
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <button onClick={() => addHost()}>Добавить</button>
                        <button onClick={closeAddModal}> Закрыть</button>
                    </div>
                </div>
            </Modal>

            <Modal isOpen={isChangeModalOpen} onClose={() => closeChangeModal()}>
                <div className="addModalUsers">

                    <div className="addModalUsersHeader">
                        Изменить хост
                    </div>

                    <div className="addModalUsersParams">
                        <div className="addModalUsersParamsValues">
                            <input type="text" className="addModalUsers" placeholder="Имя" onChange={e => setChangedHost({ ...changedHost, name: e.target.value })} value={changedHost.name} />
                            <input type="text" className="addModalUsers" placeholder="API URL" onChange={e => setChangedHost({ ...changedHost, api_url: e.target.value })} value={changedHost.api_url} />
                            <input type="text" className="addModalUsers" placeholder="Тип модели" onChange={e => setChangedHost({ ...changedHost, model_type: e.target.value })} value={changedHost.model_type} />
                            <input type="text" className="addModalUsers" placeholder="Описание" onChange={e => setChangedHost({ ...changedHost, description: e.target.value })} value={changedHost.description} />
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <button onClick={() => { validateChanges() }}>Изменить</button>
                        <button onClick={() => openAcceptModalWithAction(deleteHost)}>Удалить </button>
                        <button onClick={closeChangeModal}> Закрыть </button>
                    </div>
                </div>
            </Modal >

            <AcceptModal isOpen={isAcceptModalOpen} onClose={closeAcceptModal}>
                <div className="acceptModal">
                    <div className="acceptModalText">
                        {additionalText && <>
                            {additionalText.map(note =>
                                <p>{note}</p>
                            )}
                        </>}
                        <p>Вы уверены?</p>
                    </div>
                    <div className="acceptModalButtons">
                        <button className={"positive acceptModal"} onClick={() => { actionFunction(); closeAcceptModal(); }}> Да </button>
                        <button className={"critical acceptModal"} onClick={closeAcceptModal}> Нет </button>
                    </div>
                </div>
            </AcceptModal>
        </div >
    );
}