import React, { version } from "react";
import { useState, useEffect, useContext} from "react";
import "./Svacer.css";
import { apiGetSvacerReport } from "../../services/apiReports";
import { apiGetSvacerProjects, apiGetSvacerSnapshots } from "../../services/apiSvacer";
import SvacerProjectCard from "./SvacerProjectCard/SvacerProjectCard";
import SvacerBranchCard from "./SvacerBranchCard/SvacerBranchCard";
import SvacerSnapshotCard from "./SvacerSnapshotCard/SvacerSnapshotCard";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import filterLogo from './filter.png'

export default function Svacer() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();

    
    const [loadingProjects, setLoadingProjects] = useState('loading')
    const [projects, setProjects] = useState([])
    const [pickedProject, setPickedProject] = useState({project: {id: '', name: ''}})
    const [pickedBranch, setPickedBranch] = useState({id:''})
    
    const [loadingSnapshots, setLoadingSnapshots] = useState('loading')
    const [snapshots, setSnapshots] = useState([])
    const [pickedSnapshot, setPickedSnapshot] = useState({id: '0'})

    const [filter, setFilter] = useState({ name: '' });

    async function getProjects() {
        try {
            setLoadingProjects('loading')
            const projects = await apiGetSvacerProjects()
            setProjects(projects)
            setLoadingProjects('loaded')
        } catch (err) {
            setLoadingProjects('error')
        }
    }

    async function getSvacerSnapshots(project_id, branch_id) {
        try {
            setLoadingSnapshots('loading')
            const snapshots = await apiGetSvacerSnapshots(project_id, branch_id)
            setSnapshots(snapshots)
            setLoadingSnapshots('loaded')
        } catch (err) {
            setSnapshots([])
            setLoadingSnapshots('error')
        }
    }
    
    async function getSvacerReport(snapshot_id, snapshot_name) {
        try {
            const report = await apiGetSvacerReport(pickedProject.project.name, pickedProject.project.id, pickedBranch.id, snapshot_id, snapshot_name)
            setPickedSnapshot('')
        } catch (err) {
            setSnapshots([])
            setNotificationData({message:'Не удалось загрузить отчет', type: 'error'})
            toggleNotificationFunc()
        }
    }
    const filteredSnapshots = snapshots.filter(item => {
        return (
          (filter.name === '' || item.name.includes(filter.name))
        );
      }
    )

    useEffect(() => {
        getProjects()
    }, [])
    

    return (
        <>
            <div className="svacerProjects">
                <div className="svacerLabel">Проекты Svacer</div>
                {loadingProjects === 'loading' && <p> Loading ...</p>}
                {loadingProjects === 'error' && <p> бекенд отвалился или сервер Svacer недоступен</p>}
                {loadingProjects === 'loaded' && <>
                        {projects.map(project =>
                            <SvacerProjectCard id={project.project.id} 
                            name={project.project.name}
                            picked={pickedProject.project.id === project.project.id && true || false}
                            onClick={() => {setPickedProject(project); setPickedBranch({id: '0'}); setSnapshots([]); setLoadingSnapshots('')}}>
                            </SvacerProjectCard>)}
                        </>}
            </div>

            <div className="svacerProjects">
                <div className="svacerLabel">
                    Ветки
                    {pickedProject.project.id === '' && <p> Выберете проект</p>}
                </div>
                
                {pickedProject.project.id && <>
                        {pickedProject.branches.map(branch =>
                            <SvacerBranchCard id={branch.id} 
                            name={branch.name}
                            picked={pickedBranch.id === branch.id && true || false}
                            onClick={() => {setPickedBranch(branch); getSvacerSnapshots(pickedProject.project.id, branch.id); setSnapshots([]);}}>
                            </SvacerBranchCard>)
                            }
                        </>}
            </div>

            <div className="svacerSnapshots">
                <div className="svacerLabel">Снапшоты</div>
                <br />

                <div >
                    <img src={filterLogo} alt="" className="filterLogo"/>
                    <input type="text" className="svacerFilter" placeholder="Название" onChange={e => setFilter({...filter, name: e.target.value})} value={filter.name}/>
                    <button onClick={() => setFilter({ name: '' })} className="clearFilter">Очистить</button>
                </div>

                {pickedBranch.id !== '' && pickedProject.project.id === '' && loadingSnapshots === 'loading' && <p> Loading snapshots...</p>}
                {pickedBranch.id && pickedProject.project.id !== '' && loadingSnapshots === 'loading' && <p> Loading snapshots...</p>}
                {loadingSnapshots === 'error' && <p> бекенд отвалился или сервер Svacer недоступен</p>}
                {loadingSnapshots === 'loaded' && <>
                {snapshots.length === 0 && loadingSnapshots === 'loaded' && <p> Снапшоты не найдены</p>}
                        {filteredSnapshots.map(snapshot =>
                            <SvacerSnapshotCard id={snapshot.id} 
                            name={snapshot.name}
                            picked={pickedSnapshot.id === snapshot.id && true || false}
                            onClick={() => {getSvacerReport(snapshot.id, snapshot.name)}}>
                            </SvacerSnapshotCard>)
                            }
                        </>}
            </div>
        </>
    );
}
