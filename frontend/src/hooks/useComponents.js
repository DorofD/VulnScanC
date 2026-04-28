import { useState, useEffect } from "react";
import { apiGetProjectComponents, apiChangeComponentStatus } from "../services/apiComponents";
import { apiCheckLicenses } from "../services/apiLicenses";
import { useNotificationContext } from "../hooks/useNotificationContext";

export const useComponents = (pickedProject, setLoaderActive) => {
    const { notificationData, setNotificationData, toggleNotificationFunc } = useNotificationContext();
    
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
            setNotificationData({ message: 'Выберете новый статус', type: 'error' });
            toggleNotificationFunc();
            return;
        }
        try {
            const response = await apiChangeComponentStatus(pickedComponent.id, newComponentStatus);
            if (response.status === 200) {
                await getProjectComponents(pickedProject.id);
                setNewComponentStatus('');
                setNotificationData({ message: 'Статус изменен', type: 'success' });
                toggleNotificationFunc();
            } else {
                setNotificationData({ message: 'Не удалось изменить статус', type: 'error' });
                setNewComponentStatus('');
                toggleNotificationFunc();
            }
        } catch (error) {
            setNotificationData({ message: `Проблема с бекендом: ${error.message || error}`, type: 'error' });
            toggleNotificationFunc();
            setNewComponentStatus('');
        }
    };

    const checkLicenses = async () => {
        if (!pickedProject.id) return;
        setNotificationData({ message: 'Выполняется поиск лицензий', type: 'success' });
        toggleNotificationFunc();
        setLoaderActive(true);

        try {
            const response = await apiCheckLicenses(pickedProject.id);
            if (response.status === 200) {
                setLoaderActive(false);
                await getProjectComponents(pickedProject.id);
                setNotificationData({ message: 'Поиск завершен', type: 'success' });
                toggleNotificationFunc();
            } else {
                setLoaderActive(false);
                setNotificationData({ message: 'Не удалось выполнить поиск лицензий', type: 'error' });
                toggleNotificationFunc();
            }
        } catch (error) {
            setLoaderActive(false);
            setNotificationData({ message: `Проблема с бекендом: ${error.message || error}`, type: 'error' });
            toggleNotificationFunc();
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
