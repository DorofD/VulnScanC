import React, { useState, useEffect } from "react";
import "./AiRagConf.css";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import Filter from "../Filter/Filter";
import Loader from "../Loader/Loader";
import AiRagDocumentCard from "./AiRagDocumentCard/AiRagDocumentCard";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import {
  apiGetRagDocuments,
  apiAddRagDocument,
  apiChangeRagDocument,
  apiDeleteRagDocument,
} from "../../services/apiRagDocuments";

export default function AiRagConf() {
  const { addMessage } = useTimedMessagesContext();

  const [loading, setLoading] = useState("loading");
  const [documents, setDocuments] = useState([]);

  const [pickedDoc, setPickedDoc] = useState({ id: '', name: '', file_path: '' });
  const [newDoc, setNewDoc] = useState({ name: '', file_path: '' });
  const [changedDoc, setChangedDoc] = useState({ id: '', name: '', file_path: '' });

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
  const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);
  const [actionFunction, setActionFunction] = useState(null);

  const [filter, setFilter] = useState({ name: '', file_path: '' });

  const openAcceptModalWithAction = (action) => {
    setActionFunction(() => action);
    setIsAcceptModalOpen(true);
  };

  function closeAddModal() {
    setIsAddModalOpen(false);
    setNewDoc({ name: '', file_path: '' });
  }

  function closeChangeModal() {
    setIsChangeModalOpen(false);
    setChangedDoc({ id: '', name: '', file_path: '' });
  }

  function closeAcceptModal() {
    setIsAcceptModalOpen(false);
  }

  async function loadDocuments() {
    try {
      setLoading('loading')
      const resp = await apiGetRagDocuments()
      if (resp.ok) {
        const data = await resp.json()
        setDocuments(data.rag_documents || [])
        setLoading('loaded')
      } else {
        setLoading('error')
      }
    } catch (err) {
      setLoading('error')
    }
  }

  async function addDocument() {
    if (!newDoc.name || !newDoc.file_path) {
      addMessage('Заполните имя и путь к файлу', 'warning', 3000)
      return
    }
    const resp = await apiAddRagDocument(newDoc)
    if (resp.ok) {
      addMessage('Документ добавлен', 'success', 3000)
      loadDocuments()
      closeAddModal()
    } else {
      addMessage('Не удалось добавить документ', 'error', 3000)
    }
  }

  async function changeDocument(changes) {
    try {
      const resp = await apiChangeRagDocument(changedDoc.id, changes)
      if (resp.ok) {
        addMessage('Документ изменён', 'success', 3000)
        loadDocuments()
        closeChangeModal()
        closeAcceptModal()
      } else {
        addMessage('Не удалось изменить документ', 'error', 3000)
      }
    } catch (err) {
      addMessage(`Ошибка: ${err.message}`, 'error', 5000)
    }
  }

  async function deleteDocument() {
    const resp = await apiDeleteRagDocument(changedDoc.id)
    if (resp.ok) {
      addMessage('Документ удалён', 'success', 3000)
      loadDocuments()
      closeChangeModal()
      closeAcceptModal()
    } else {
      addMessage('Не удалось удалить документ', 'error', 3000)
    }
  }

  const filtered = documents.filter(item => {
    return (
      (filter.name === '' || (item.name || '').includes(filter.name)) &&
      (filter.file_path === '' || (item.file_path || '').includes(filter.file_path))
    )
  })

  useEffect(() => { loadDocuments() }, [])

  return (
    <div className="ragConfMain">
    <div className="ragConfLeft">
        <div className="ragConfHeader">
          <button onClick={() => { setPickedDoc({ id: 0, name: '', file_path: '' }); setIsAddModalOpen(true) }}>Добавить</button>
        </div>
          <Filter onClick={() => setFilter({ name: '', file_path: '' })}>
            <input type="text" className="filter" placeholder="Имя" onChange={e => setFilter({ ...filter, name: e.target.value })} value={filter.name} />
            <input type="text" className="filter" placeholder="Путь к файлу" onChange={e => setFilter({ ...filter, file_path: e.target.value })} value={filter.file_path} />
          </Filter>

        {loading === 'loading' && <Loader />}
        {loading === 'error' && <p>Ошибка загрузки</p>}
        {loading === 'loaded' && <div className="ragConfNotes">
          {filtered.map(doc => (
            <div key={doc.id}>
              <AiRagDocumentCard
                id={doc.id}
                name={doc.name}
                filePath={doc.file_path}
                picked={pickedDoc.id === doc.id && true || false}
                onClick={() => { setPickedDoc(doc); setChangedDoc({ id: doc.id, name: doc.name, file_path: doc.file_path }); setIsChangeModalOpen(true) }}
              >
              </AiRagDocumentCard>
            </div>
          ))}
        </div>}

        <Modal isOpen={isAddModalOpen} onClose={() => closeAddModal()}>
          <div className="ragConfModal">
            <h3>Добавить документ</h3>
            <div className="ragConfInputs">
              <input type="text" placeholder="Имя" onChange={e => setNewDoc({ ...newDoc, name: e.target.value })} value={newDoc.name} />
              <input type="text" placeholder="Путь к файлу" onChange={e => setNewDoc({ ...newDoc, file_path: e.target.value })} value={newDoc.file_path} />
            </div>
            <div className="ragConfModalButtons">
              <button onClick={() => addDocument()}>Добавить</button>
              <button onClick={() => closeAddModal()}>Закрыть</button>
            </div>
          </div>
        </Modal>

        <Modal isOpen={isChangeModalOpen} onClose={() => closeChangeModal()}>
          <div className="ragConfModal">
            <h3>Изменить документ</h3>
            <div className="ragConfInputs">
              <input type="text" placeholder="Имя" onChange={e => setChangedDoc({ ...changedDoc, name: e.target.value })} value={changedDoc.name} />
              <input type="text" placeholder="Путь к файлу" onChange={e => setChangedDoc({ ...changedDoc, file_path: e.target.value })} value={changedDoc.file_path} />
            </div>
            <div className="ragConfModalButtons">
              <button onClick={() => { const changes = {}; if (changedDoc.name !== pickedDoc.name) changes.name = changedDoc.name; if (changedDoc.file_path !== pickedDoc.file_path) changes.file_path = changedDoc.file_path; if (Object.keys(changes).length === 0) { addMessage('Вы ничего не изменили', 'warning', 3000); return } openAcceptModalWithAction(() => changeDocument(changes)) }}>Изменить</button>
              <button onClick={() => openAcceptModalWithAction(deleteDocument)}>Удалить</button>
              <button onClick={() => closeChangeModal()}>Закрыть</button>
            </div>
          </div>
        </Modal>
        <AcceptModal isOpen={isAcceptModalOpen} onClose={closeAcceptModal}>
          <div className="acceptModal">
            <div className="acceptModalText">
              <p>Вы уверены?</p>
            </div>
            <div className="acceptModalButtons">
              <button className={"positive acceptModal"} onClick={() => { actionFunction(); closeAcceptModal(); }}>Да</button>
              <button className={"critical acceptModal"} onClick={closeAcceptModal}>Нет</button>
            </div>
          </div>
        </AcceptModal>
    </div>
    </div>
  );
}
