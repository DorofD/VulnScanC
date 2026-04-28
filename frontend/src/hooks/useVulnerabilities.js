import { useState, useEffect } from "react";
import { apiGetComponentVulnerabilities } from "../services/apiVulnerabilities";
import { apiGetBduComponentVulns } from "../services/apiBduFstec";
import { useNotificationContext } from "../hooks/useNotificationContext";

export function useVulnerabilities(pickedComponentId) {
    const [componentVulnerabilities, setComponentVulnerabilities] = useState([]);
    const [showedVunls, setShowedVunls] = useState(null); // 'osv' | 'bdu' | null
    const [filterVulnerabilities, setFilterVulnerabilities] = useState({ osv_id: '' });
    const [filterVulnerabilitiesBdu, setFilterVulnerabilitiesBdu] = useState({ bdu_id: '' });
    const { notificationData, toggleNotificationFunc } = useNotificationContext();

    async function showComponentVulnerabilities() {
        try {
            const vulnerabilities = await apiGetComponentVulnerabilities(pickedComponentId);
            setComponentVulnerabilities(vulnerabilities);
        } catch (err) {
            setComponentVulnerabilities([]);
            notificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' });
            toggleNotificationFunc();
        }
    }

    async function showComponentVulnerabilitiesBdu() {
        try {
            const vulnerabilities = await apiGetBduComponentVulns(pickedComponentId, 'common');
            setComponentVulnerabilities(vulnerabilities);
        } catch (err) {
            setComponentVulnerabilities([]);
            notificationData({ message: `Проблема с бекендом: ${err}`, type: 'error' });
            toggleNotificationFunc();
        }
    }

    const filteredVulnerabilities = componentVulnerabilities.filter(item => {
        if (showedVunls === 'osv') {
            return (
                (filterVulnerabilities.osv_id === '' || item.osv_id.includes(filterVulnerabilities.osv_id))
            );
        }
        if (showedVunls === 'bdu') {
            return (
                (filterVulnerabilitiesBdu.bdu_id === '' || item.bdu_id.includes(filterVulnerabilitiesBdu.bdu_id))
            );
        }
        return true;
    });

    return {
        componentVulnerabilities,
        showedVunls,
        setShowedVunls,
        filterVulnerabilities,
        setFilterVulnerabilities,
        filterVulnerabilitiesBdu,
        setFilterVulnerabilitiesBdu,
        filteredVulnerabilities,
        showComponentVulnerabilities,
        showComponentVulnerabilitiesBdu
    };
}
