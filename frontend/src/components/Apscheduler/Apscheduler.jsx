import React, { Component, useState, useEffect } from "react";
import { apiGetSchedulerInfo } from "../../services/apiScheduler";

export default function Apscheduler() {
    const [schedulerInfo, setSchedulerInfo] = useState([])
    const [loading, setLoading] = useState('loading')

    async function getSchedulerInfo() {
        try {
            setLoading('loading')
            const schedulerInfo = await apiGetSchedulerInfo()
            setSchedulerInfo(schedulerInfo)
            console.log(schedulerInfo.status)
            setLoading('loaded')
        } catch (err) {
            setLoading('error')
        }
    }

    useEffect(() => {
        getSchedulerInfo()  
    }, [])
    return (
        <div>
            {loading === 'loading' && <p> Loading ...</p>}
            {loading === 'error' && <p> бекенд отвалился</p>}
            {loading === 'loaded' && <>
                        <div>Scheduler status: {schedulerInfo.status.toString()}</div>
                        <div>Jobs:</div>
                        {schedulerInfo.jobs.map(job =>
                        <div>
                            {/*job.id*/} {job.name} Next run: {job.next_run} | trigger: {job.trigger}
                        </div>)}
                        </>}
      </div>
    );
}