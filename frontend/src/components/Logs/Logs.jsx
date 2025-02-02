import React from "react";
import { useState, useEffect, useContext} from "react";
import { apiGetLogsJson, apiGetLogsFile } from "../../services/apiLogs";
import Button from "../Button/Button";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import LogCard from "./LogCard/LogCard";
import "./Logs.css"
import filterLogo from './filter.png'

export default function Logs() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();

    const [loadingLogs, setLoadingLogs] = useState('loading')
    const [logs, setLogs] = useState([])
    const [pickedLogId, setPickedLogId] = useState(0) 
    const [filterLogs, setFilterLogs] = useState({ datetime: '', status: '', note: '' });


    async function getLogsJson() {
        try {
            setLoadingLogs('loading')
            const logs = await apiGetLogsJson()
            const logsWithId = logs.map((log, index) => ({
                ...log,
                id: index + 1
            }));
            setLogs(logsWithId);
            setLoadingLogs('loaded')
        } catch (err) {
            setLoadingLogs('error')
        }
    }

    async function getLogsFile() {
        try {
            const report = await apiGetLogsFile()
        } catch (err) {
            setNotificationData({message:'Не удалось загрузить отчет', type: 'error'})
            toggleNotificationFunc()
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

            <div className="logsHeader">
                Записей в логе: {logs.length} 
                <Button style={"logsDownload"} onClick={() => getLogsFile()}> Скачать </Button>
            </div>

            <div className="logsFilterContainer">
                    <img src={filterLogo} alt="" className="filterLogo"/>
                    <input type="text" className="logsFilter" placeholder="Время" onChange={e => setFilterLogs({...filterLogs, datetime: e.target.value})} value={filterLogs.datetime}/>
                    <input type="text" className="logsFilter" placeholder="Статус" onChange={e => setFilterLogs({...filterLogs, status: e.target.value})} value={filterLogs.status}/>
                    <input type="text" className="logsFilter" placeholder="Текст записи" onChange={e => setFilterLogs({...filterLogs, note: e.target.value})} value={filterLogs.note}/>
                    <button onClick={() => setFilterLogs({ datetime: '', status: '', note: '' })} className="clearFilter">Очистить</button>
            </div>
            {loadingLogs === 'loading' && <p> Loading ...</p>}
            {loadingLogs === 'error' && <p> бекенд отвалился</p>}
            {loadingLogs === 'loaded' && <>
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
                    </>}
        </div>
    </>
    );
}