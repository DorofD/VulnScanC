import { useState, useEffect } from "react";
import { apiGetComponentVulnerabilities } from "../services/apiVulnerabilities";
import { apiGetBduComponentVulns } from "../services/apiBduFstec";
import { useTimedMessagesContext } from "../hooks/useTimedMessagesContext";

export function useVulnerabilities(pickedComponentId) {
    const [componentVulnerabilities, setComponentVulnerabilities] = useState([]);
    const [showedVunls, setShowedVunls] = useState(null); // 'osv' | 'bdu' | null
    const [filterVulnerabilities, setFilterVulnerabilities] = useState({ osv_id: '' });
    const [filterVulnerabilitiesBdu, setFilterVulnerabilitiesBdu] = useState({ bdu_id: '' });
    const [pickedVulnerability, setPickedVulnerability] = useState(null);
    const { addMessage } = useTimedMessagesContext();

    async function showComponentVulnerabilities() {
        try {
            const vulnerabilities = await apiGetComponentVulnerabilities(pickedComponentId);
            setComponentVulnerabilities(vulnerabilities);
        } catch (err) {
            setComponentVulnerabilities([]);
            addMessage(`Проблема с бекендом: ${err}`, 'error', 5000);
        }
    }

    async function showComponentVulnerabilitiesBdu() {
        try {
            const vulnerabilities = await apiGetBduComponentVulns(pickedComponentId, 'common');
            setComponentVulnerabilities(vulnerabilities);
        } catch (err) {
            setComponentVulnerabilities([]);
            addMessage(`Проблема с бекендом: ${err}`, 'error', 5000);
        }
    }

    function onOpenVulnerabilityModal() {
        // placeholder - modal open handled by parent
    }

    function closeVulnerabilityModal() {
        setPickedVulnerability(null);
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
        pickedVulnerability,
        setPickedVulnerability,
        filterVulnerabilities,
        setFilterVulnerabilities,
        filterVulnerabilitiesBdu,
        setFilterVulnerabilitiesBdu,
        filteredVulnerabilities,
        showComponentVulnerabilities,
        showComponentVulnerabilitiesBdu,
        onOpenVulnerabilityModal,
        closeVulnerabilityModal,
        setComponentVulnerabilities
    };
}
