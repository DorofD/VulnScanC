import React, { Component } from "react";
import { useState, useEffect } from "react";
import "./LlamaNodes.css";
import LlamaNodeCard from "./LlamaNodeCard/LlamaNodeCard";
import Button from "../Button/Button";
import Filter from "../Filter/Filter";
import {
    apiGetChatNodes,
    apiGetEmbeddingNodes,
    apiAddChatNode,
    apiAddEmbeddingNode,
    apiChangeChatNode,
    apiChangeEmbeddingNode,
    apiDeleteChatNode,
    apiDeleteEmbeddingNode,
    apiChangeLlamaNode,
    apiDeleteLlamaNode,
    apiGetLlamaNodes,
    apiAddLlamaNode,
} from "../../services/apiLlamaNodes";
// // import { useNotificationContext } from "../../hooks/useNotificationContext";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import Loader from "../Loader/Loader";

export default function LlamaNodes() {
    const { messages, addMessage } = useTimedMessagesContext();

    const [loaderActive, setLoaderActive] = useState(false)

    const [chatNodes, setChatNodes] = useState([])
    const [embeddingNodes, setEmbeddingNodes] = useState([])
    const [selectedTab, setSelectedTab] = useState('chat')
    const [loading, setLoading] = useState('loading')
    const [pickedNode, setPickedNode] = useState({ id: '', name: '', base_api_url: '', description: '' })
    const [newNode, setNewNode] = useState({ name: '', base_api_url: '', description: '' })
    const [changedNode, setChangedNode] = useState({ id: '', name: '', base_api_url: '', description: '' })

    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);

    const [actionFunction, setActionFunction] = useState(null);
    const [filterNodes, setFilterNodes] = useState({ name: '', base_api_url: '' });
    const [additionalText, setAdditionalText] = useState([]);

    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    function closeAddModal() {
        setIsAddModalOpen(false);
        setNewNode({ name: '', base_api_url: '', description: '' })
    }

    function closeChangeModal() {
        setIsChangeModalOpen(false);
        setChangedNode({ id: '', name: '', base_api_url: '', description: '' })
        setAdditionalText([])
    }

    function closeAcceptModal() {
        setIsAcceptModalOpen(false);
    }


    async function getNodes() {
        try {
            setLoading('loading')
            const [rc, re] = await Promise.allSettled([apiGetChatNodes(), apiGetEmbeddingNodes()])
            if (rc.status === 'fulfilled' && rc.value.ok) {
                const data = await rc.value.json()
                setChatNodes(data.chat_nodes || [])
            } else if (rc.status === 'fulfilled') {
                // fallback to legacy combined endpoint
                const legacy = await apiGetLlamaNodes()
                if (legacy.ok) {
                    const data = await legacy.json()
                    if (Array.isArray(data.llama_nodes)) {
                        // separate by injected model_type if available
                        const chat = data.filter(h => h.model_type === 'chat')
                        setChatNodes(chat)
                        const emb = data.filter(h => h.model_type === 'embedding')
                        setEmbeddingNodes(emb)
                    }
                }
            }
            if (re.status === 'fulfilled' && re.value.ok) {
                const data = await re.value.json()
                setEmbeddingNodes(data.embedding_nodes || [])
            }
            setLoading('loaded')
        } catch (err) {
            setLoading('error')
        }
    }

    async function addNode() {
        if (!newNode.base_api_url) {
            addMessage('Введите API URL', 'warning', 3000)
            return false
        }

        let response
        if (selectedTab === 'chat') {
            response = await apiAddChatNode(newNode)
        } else {
            response = await apiAddEmbeddingNode(newNode)
        }
        if (response.status == 200) {
            getNodes()
            closeAddModal()
            addMessage('Узел добавлен', 'success', 3000)
        } else {
            addMessage('Не удалось добавить узел', 'error', 3000)
        }
    }


    function validateChanges() {
        let changesDict = {}
        let textList = []
        if (changedNode.name !== pickedNode.name) {
            changesDict.name = changedNode.name
            textList.push(`Имя: ${pickedNode.name} => ${changedNode.name}`)
        }
        if (changedNode.base_api_url !== pickedNode.base_api_url) {
            changesDict.base_api_url = changedNode.base_api_url
            textList.push(`API URL: ${pickedNode.base_api_url} => ${changedNode.base_api_url}`)
        }
        if (changedNode.description !== pickedNode.description) {
            changesDict.description = changedNode.description
            textList.push(`Описание изменено`)
        }
        if (Object.keys(changesDict).length === 0) {
            addMessage('Вы ничего не изменили', 'warning', 3000)
            setAdditionalText([])
            return false
        }

        textList.unshift("Следующие изменения будут применены:")
        setAdditionalText(textList)
        openAcceptModalWithAction(() => changeNode(changesDict))
    }

    async function changeNode(changesDict) {
        try {
            let response
            if (pickedNode && pickedNode.id) {
                if (pickedNode.model_type === 'embedding' || selectedTab === 'embedding') {
                    response = await apiChangeEmbeddingNode(pickedNode.id, changesDict)
                } else {
                    response = await apiChangeChatNode(pickedNode.id, changesDict)
                }
            }
            if (response && response.status == 200) {
                getNodes()
                closeAcceptModal()
                closeChangeModal()
                addMessage('Узел изменён', 'success', 3000)
                setAdditionalText([])
            } else {
                closeAcceptModal()
                addMessage('Не удалось изменить узел', 'warning', 3000)
                setAdditionalText([])
            }
        }catch (err) {
            setLoaderActive(false)
            console.log(err)
            addMessage(`Что-то пошло не так: ${err.message}`, 'error', 5000)
        }
    }

    async function deleteNode() {
        let response
        if (selectedTab === 'embedding') {
            response = await apiDeleteEmbeddingNode(changedNode.id)
        } else {
            response = await apiDeleteChatNode(changedNode.id)
        }
        if (response.status == 200) {
            getNodes()
            closeAcceptModal()
            closeChangeModal()
            addMessage('Узел удалён', 'success', 3000)

        } else {
            closeAcceptModal()
            addMessage('Не удалось удалить узел', 'error', 3000)
        }
    }

    const nodes = selectedTab === 'chat' ? chatNodes : embeddingNodes
    const filteredNodes = nodes.filter(item => {
        return (
            (filterNodes.name === '' || (item.name || '').includes(filterNodes.name)) &&
            (filterNodes.base_api_url === '' || (item.base_api_url || '').includes(filterNodes.base_api_url))
        );
    })

    useEffect(() => {
        getNodes()
    }, [])

    return (
        <div className="usersContainer">
            <div className="usersHeader">
                <div className="nodesTabs">
                    <button className={selectedTab === 'chat' ? 'active' : ''} onClick={() => setSelectedTab('chat')}>Chat Nodes</button>
                    <button className={selectedTab === 'embedding' ? 'active' : ''} onClick={() => setSelectedTab('embedding')}>Embedding Nodes</button>
                </div>
                <button onClick={() => { setPickedNode({ id: 0, name: '', base_api_url: '', description: '' }); setIsAddModalOpen(true) }}>Добавить узел</button>
            </div>
            <Filter onClick={() => setFilterNodes({ name: '', base_api_url: '' })}>
                <input type="text" className="filter" placeholder="Имя" onChange={e => setFilterNodes({ ...filterNodes, name: e.target.value })} value={filterNodes.name} />
                <input type="text" className="filter" placeholder="API URL" onChange={e => setFilterNodes({ ...filterNodes, base_api_url: e.target.value })} value={filterNodes.base_api_url} />
            </Filter>

            <div className="usersNotes">


                {loading === 'loading' && <Loader />}
                {loading === 'error' && <p> бекенд отвалился</p>}
                {loading === 'loaded' && <>
                    {filteredNodes.map(node =>
                        <LlamaNodeCard
                            key={node.id}
                            id={node.id}
                            name={node.name}
                            apiUrl={node.base_api_url}
                            modelType={selectedTab}
                            picked={pickedNode.id === node.id && true || false}
                            onClick={() => { setPickedNode(node); setChangedNode({ id: node.id, name: node.name, base_api_url: node.base_api_url, description: node.description }); setAdditionalText([]); setIsChangeModalOpen(true) }}>
                        </LlamaNodeCard>
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
                            <input type="text" className="addModalUsers" placeholder="Имя" onChange={e => setNewNode({ ...newNode, name: e.target.value })} value={newNode.name} />
                            <input type="text" className="addModalUsers" placeholder="API URL" onChange={e => setNewNode({ ...newNode, base_api_url: e.target.value })} value={newNode.base_api_url} />
                            <div className="addModalUsersType">Тип: {selectedTab}</div>
                            <input type="text" className="addModalUsers" placeholder="Описание" onChange={e => setNewNode({ ...newNode, description: e.target.value })} value={newNode.description} />
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <button onClick={() => addNode()}>Добавить</button>
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
                            <input type="text" className="addModalUsers" placeholder="Имя" onChange={e => setChangedNode({ ...changedNode, name: e.target.value })} value={changedNode.name} />
                            <input type="text" className="addModalUsers" placeholder="API URL" onChange={e => setChangedNode({ ...changedNode, base_api_url: e.target.value })} value={changedNode.base_api_url} />
                            <div className="addModalUsersType">Тип: {selectedTab}</div>
                            <input type="text" className="addModalUsers" placeholder="Описание" onChange={e => setChangedNode({ ...changedNode, description: e.target.value })} value={changedNode.description} />
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <button onClick={() => { validateChanges() }}>Изменить</button>
                        <button onClick={() => openAcceptModalWithAction(deleteNode)}>Удалить </button>
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
