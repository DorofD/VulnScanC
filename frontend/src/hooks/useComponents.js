import { useState, useEffect } from "react";
import { apiGetProjectComponents, apiChangeComponentStatus } from "../services/apiComponents";
import { apiCheckLicenses } from "../services/apiLicenses";
import { useTimedMessagesContext } from "../hooks/useTimedMessagesContext";

export const useComponents = (pickedProject, setLoaderActive) => {
    const { addMessage } = useTimedMessagesContext();
    
    const [loadingComponents, setLoadingComponents] = useState('loading');
    const [components, setComponents] = useState([{ address: '' }]);
    const [pickedComponent, setPickedComponent] = useState({ id: '' });
    const [newComponentStatus, setNewComponentStatus] = useState('');
    const [filterComponents, setFilterComponents] = useState({ address: '', status: '' });

    const getProjectComponents = async (projectId) => {
        if (!projectId) return;
        try {
            setLoadingComponents('loading');
            const data = await apiGetProjectComponents(projectId);

            const order = { 'none': 0, 'confirmed': 1, 'denied': 2 };
            const sortedComponents = data.sort((a, b) => {
                return order[a.status] - order[b.status];
            });
            setComponents(sortedComponents);
            setLoadingComponents('loaded');
        } catch (err) {
            setComponents([]);
            setLoadingComponents('error');
        }
    };

    const changeComponentStatus = async () => {
        if (newComponentStatus === '') {
            addMessage('Выберете новый статус', 'error', 3000);
            return;
        }
        try {
            const response = await apiChangeComponentStatus(pickedComponent.id, newComponentStatus);
            if (response.status === 200) {
                await getProjectComponents(pickedProject.id);
                setNewComponentStatus('');
                addMessage('Статус изменен', 'success', 3000);
            } else {
                addMessage('Не удалось изменить статус', 'error', 3000);
                setNewComponentStatus('');
            }
        } catch (error) {
            addMessage(`Проблема с бекендом: ${error.message || error}`, 'error', 5000);
            setNewComponentStatus('');
        }
    };

    const checkLicenses = async () => {
        if (!pickedProject.id) return;
        addMessage('Выполняется поиск лицензий', 'success', 3000);
        setLoaderActive(true);

        try {
            const response = await apiCheckLicenses(pickedProject.id);
            if (response.status === 200) {
                setLoaderActive(false);
                await getProjectComponents(pickedProject.id);
                addMessage('Поиск завершен', 'success', 3000);
            } else {
                setLoaderActive(false);
                addMessage('Не удалось выполнить поиск лицензий', 'error', 3000);
            }
        } catch (error) {
            setLoaderActive(false);
            addMessage(`Проблема с бекендом: ${error.message || error}`, 'error', 5000);
        }
    };

    const filteredComponents = components.filter(item => {
        return (
            (filterComponents.address === '' || item.address.includes(filterComponents.address)) &&
            (filterComponents.status === '' || item.status.includes(filterComponents.status))
        );
    });

    return {
        loadingComponents,
        components,
        pickedComponent,
        setPickedComponent,
        newComponentStatus,
        setNewComponentStatus,
        filterComponents,
        setFilterComponents,
        filteredComponents,
        getProjectComponents,
        changeComponentStatus,
        checkLicenses
    };
};
