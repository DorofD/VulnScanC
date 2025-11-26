import React from "react";
import { useState, useEffect, useContext } from "react";
import { apiGetLogsJson, apiGetLogsFile, apiClearLogs } from "../../services/apiLogs";
import Button from "../Button/Button";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";

import LogCard from "./LogCard/LogCard";
import "./Logs.css"
import Filter from "../Filter/Filter";
import Loader from "../Loader/Loader";
import { useAuthContext } from "../../hooks/useAuthContext";
import AcceptModal from "../AcceptModal/AcceptModal";

export default function Logs() {
    const { accessToken } = useAuthContext();

    const { messages, addMessage } = useTimedMessagesContext();
    const [loaderActive, setLoaderActive] = useState(false)

    const [loadingLogs, setLoadingLogs] = useState('loading')
    const [logs, setLogs] = useState([])
    const [pickedLogId, setPickedLogId] = useState(0)
    const [filterLogs, setFilterLogs] = useState({ datetime: '', status: '', note: '' });
    const [logLevel, setLogLevel] = useState('')
    const [logLevels, setLogLevels] = useState([])
    const [logCount, setLogCount] = useState('')
    const [logFileSize, setLogFileSize] = useState('')
    const [dbFileSize, setDbFileSize] = useState('')
    const [actionFunction, setActionFunction] = useState(null);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);


    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    function closeAcceptModal() {
        setIsAcceptModalOpen(false);
    };

    async function getLogsJson() {
        try {
            setLoadingLogs('loading')
            const logs = await apiGetLogsJson(accessToken)
            const logsWithId = logs.logs.map((log, index) => ({
                ...log,
                id: index + 1
            }));
            setLogs(logsWithId);
            setLogCount(logs.count)
            setLogLevel(logs.level)
            setLogLevels(logs.levels)
            setLogFileSize(logs.log_file_size)
            setDbFileSize(logs.db_file_size)
            setLoadingLogs('loaded')
        } catch (err) {
            setLoadingLogs('error')
            console.log(err)
        }
    }

    async function getLogsFile() {
        try {
            const report = await apiGetLogsFile(accessToken)
        } catch (err) {
            addMessage('Не удалось загрузить отчет', 'error', 3000)
        }
    }

    async function clearLogs() {
        const response = await apiClearLogs()
        if (response.status == 200) {
            getLogsJson()
            addMessage('Логи очищены', 'success', 3000)
            closeAcceptModal()

        } else {
            closeAcceptModal()
            addMessage('Не удалось очистить логи', 'error', 3000)
        }
    }

    const filteredLogs = logs.filter(item => {
        return (
            (filterLogs.datetime === '' || item.datetime.includes(filterLogs.datetime)) &&
            (filterLogs.status === '' || item.status.includes(filterLogs.status)) &&
            (filterLogs.note === '' || item.note.includes(filterLogs.note))
        );
    }
    )

    useEffect(() => {
        getLogsJson()
    }, [])

    return (
        <>
            <div className="logs">
                <div className="logsLeft">
                    <Filter onClick={() => setFilterLogs({ datetime: '', status: '', note: '' })}>
                        <input type="text" className="filter" placeholder="Время" onChange={e => setFilterLogs({ ...filterLogs, datetime: e.target.value })} value={filterLogs.datetime} />
                        <select className='filter' onChange={e => setFilterLogs({ ...filterLogs, status: e.target.value })}>
                            {loadingLogs === 'loaded' && <>{<option className='' value="" selected={filterLogs.status === '' && true || false}>All </option>}
                                {logLevels.map((level, index) => <option id={index} value={level}>{level}</option>)}</>}
                            {loadingLogs === 'error' && <>{<option value="" selected={filterLogs.status === '' && true || false}>Бекенд отвалился</option>}</>}
                        </select>
                        <input type="text" className="filter" placeholder="Текст записи" onChange={e => setFilterLogs({ ...filterLogs, note: e.target.value })} value={filterLogs.note} />
                    </Filter>
                    {loadingLogs === 'loading' && <Loader />}
                    {loadingLogs === 'error' && <p> бекенд отвалился</p>}
                    {loadingLogs === 'loaded' && <>
                        <div className="logsNotes">
                            {filteredLogs.map(log =>
                                <LogCard
                                    id={log.id}
                                    datetime={log.datetime}
                                    status={log.status}
                                    note={log.note}
                                    picked={pickedLogId === log.id}
                                    onClick={() => {
                                        if (pickedLogId === log.id) {
                                            setPickedLogId(0);
                                        } else {
                                            setPickedLogId(log.id);
                                        }
                                    }}
                                />)}
                        </div>

                    </>}
                </div>
                <div className="logsRight">
                    <div className="logsInfo">
                        <p className="logsCount">Кол-во записей: {logCount}</p>
                        <p className="logsCount">Размер лог-файла: {logFileSize}</p>
                        <p className="logsLevel">Уровень логирования: {logLevel}</p>
                        <p className="logsLevel">Доступные статусы: |{logLevels.map((level, index) => (
                            <>
                                <div id={index} className="logsStatus"> {level} | </div>
                            </>
                        ))}</p>
                    </div>
                    <div className="logsActions">
                        <button onClick={() => getLogsFile()}>Скачать файл</button>
                        <button onClick={() => openAcceptModalWithAction(clearLogs)}>Очистить логи</button>
                    </div>
                </div>
            </div>
            <AcceptModal isOpen={isAcceptModalOpen} onClose={closeAcceptModal}>
                <div className="acceptModal">
                    <div className="acceptModalText">
                        <p>Все записи лога будут стёрты </p>
                        <p>Вы уверены?</p>
                    </div>
                    <div className="acceptModalButtons">
                        <button className={"positive acceptModal"} onClick={() => { actionFunction(); closeAcceptModal(); }}> Да </button>
                        <button className={"critical acceptModal"} onClick={closeAcceptModal}> Нет </button>
                    </div>
                </div>
            </AcceptModal>
        </>
    );
}