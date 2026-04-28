import { useState, useEffect } from "react";
import { apiGetProjects } from "../services/apiProjects";

export const useProjects = () => {
    const [loadingProjects, setLoadingProjects] = useState('loading');
    const [projects, setProjects] = useState([]);
    const [pickedProject, setPickedProject] = useState({ id: '', name: '' });

    const getProjects = async () => {
        try {
            setLoadingProjects('loading');
            const data = await apiGetProjects();
            setProjects(data);
            setLoadingProjects('loaded');
        } catch (err) {
            setLoadingProjects('error');
        }
    };

    useEffect(() => {
        getProjects();
    }, []);

    return {
        loadingProjects,
        projects,
        pickedProject,
        setPickedProject,
        getProjects
    };
};
