import React from "react";
import Button from "../../../components/Button/Button";
import Modal from "../../../components/Modal/Modal";

const LicenseModalContent = ({
    pickedComponentLicenses,
    onOpenAcceptModal,
    onDeleteLicense,
    newLicense,
    setNewLicense,
    onAddLicense,
    pickedComponentId
}) => {
    return (
        <div className="changeModalComponents">
            <div className="changeModalComponentsParams">
                <p>Лицензии:</p>
                {pickedComponentLicenses && pickedComponentLicenses.length > 0 ? (
                    <ul className="license">
                        {pickedComponentLicenses.map((license) => (
                            <li className="license" key={license.id}>
                                <p>Название: {license.name}</p>
                                <p>Ключ: {license.key}</p>
                                <p>SPDX ID: {license.spdx_id}</p>
                                <p>URL: {license.url !== "None" ? <a href={license.url} target="_blank" rel="noopener noreferrer">{license.url}</a> : "Нет ссылки"}</p>
                                <p><Button style={"projectReject"} onClick={() => onOpenAcceptModal(() => onDeleteLicense(license.id))}> Удалить </Button></p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <> Лицензий не найдено</>
                )}
                <p>Добавить лицензию</p>
                <textarea name="newLicense" id={pickedComponentId} placeholder='Название' className="license" value={newLicense.name} onChange={e => setNewLicense({ ...newLicense, name: e.target.value })}></textarea>
                <textarea name="newLicense" id={pickedComponentId} placeholder='Ключ' className="license" value={newLicense.key} onChange={e => setNewLicense({ ...newLicense, key: e.target.value })}></textarea>
                <textarea name="newLicense" id={pickedComponentId} placeholder='SPDX ID' className="license" value={newLicense.spdx_id} onChange={e => setNewLicense({ ...newLicense, spdx_id: e.target.value })}></textarea>
                <textarea name="newLicense" id={pickedComponentId} placeholder='URL' className="license" value={newLicense.url} onChange={e => setNewLicense({ ...newLicense, url: e.target.value })}></textarea>
                <p><Button style={"projectAccept"} onClick={onAddLicense}> Добавить </Button></p>
            </div>
        </div>
    );
};

export default LicenseModalContent;
