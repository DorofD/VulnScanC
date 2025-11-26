import React, { Component } from "react";
import { useState, useEffect } from "react";
import "./Users.css";
import UserCard from "./UserCard/UserCard";
import Button from "../Button/Button";
import Filter from "../Filter/Filter";
import { apiGetUsers, apiAddUser, apiChangeUser, apiDeleteUser } from "../../services/apiUsers";
// // import { useNotificationContext } from "../../hooks/useNotificationContext";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import Loader from "../Loader/Loader";

export default function Users() {
    const { messages, addMessage } = useTimedMessagesContext();

    const [loaderActive, setLoaderActive] = useState(false)

    const [users, setUsers] = useState([])
    const [loading, setLoading] = useState('loading')
    const [pickedUser, setPickedUser] = useState({ id: '', login: '', role: '' })
    const [newUser, setNewUser] = useState({ login: '', auth_type: '', role: '', password: '', confirmPassword: '' })
    const [changedUser, setChangedUser] = useState({ id: '', login: '', auth_type: '', role: '', password: '', confirmPassword: '' })

    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);

    const [actionFunction, setActionFunction] = useState(null);
    const [filterUsers, setFilterUsers] = useState({ login: '', role: '', auth_type: '' });
    const [additionalText, setAdditionalText] = useState([]);

    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
    };

    function closeAddModal() {
        setIsAddModalOpen(false);
        setNewUser({ id: '', login: '', auth_type: '', role: '', password: '', confirmPassword: '' })
    }

    function closeChangeModal() {
        setIsChangeModalOpen(false);
        setChangedUser({ id: '', login: '', auth_type: '', role: '', password: '', confirmPassword: '' })
        setAdditionalText([])
    }

    function closeAcceptModal() {
        setIsAcceptModalOpen(false);
    }


    async function getUsers() {
        try {
            setLoading('loading')
            const response = await apiGetUsers()
            const users = await response.json()
            setUsers(users)
            setLoading('loaded')
        } catch (err) {
            setLoading('error')
        }
    }

    async function addUser() {
        if (!newUser.login) {
            addMessage('Введите имя пользователя', 'warning', 3000)
            return false
        }

        if (!newUser.role) {
            addMessage('Выберете роль пользователя', 'warning', 3000)
            return false
        }

        if (!newUser.auth_type) {
            addMessage('Выберете тип авторизации пользователя', 'warning', 3000)
            return false
        }

        if (!newUser.password && newUser.auth_type === 'local') {
            addMessage('Введите пароль', 'warning', 3000)
            return false
        }

        if (newUser.password != newUser.confirmPassword) {
            addMessage('Пароли не совпадают', 'warning', 3000)
            return false
        }


        const response = await apiAddUser(newUser.login, newUser.role, newUser.auth_type, newUser.password)
        if (response.status == 200) {
            getUsers()
            closeAddModal()
            addMessage('Пользователь добавлен', 'success', 3000)

        } else {
            addMessage('Не удалось добавить пользователя', 'error', 3000)
        }
    }


    function validateChanges() {
        let changesDict = {}
        let textList = []
        if (changedUser.role !== pickedUser.role) {
            changesDict.role = changedUser.role
            textList.push(`Роль: ${pickedUser.role} => ${changedUser.role}`)
        }
        if (changedUser.login !== pickedUser.login) {
            changesDict.login = changedUser.login
            textList.push(`Логин: ${pickedUser.login} => ${changedUser.login}`)
        }
        if (changedUser.password != changedUser.confirmPassword) {
            addMessage('Пароли не совпадают', 'warning', 3000)
            return false
        }
        if (changedUser.password) {
            changesDict.password = changedUser.password
            textList.push(`Новый пароль`)
        }
        if (Object.keys(changesDict).length === 0) {
            addMessage('Вы ничего не изменили', 'warning', 3000)
            setAdditionalText([])
            return false
        }

        textList.unshift("Следующие изменения будут применены:")
        setAdditionalText(textList)
        console.log(changesDict)
        openAcceptModalWithAction(() => changeUser(changesDict))
    }

    async function changeUser(changesDict) {
        const response = await apiChangeUser(pickedUser.id, changesDict)
        if (response.status == 200) {
            getUsers()
            closeAcceptModal()
            closeChangeModal()
            addMessage('Пользователь изменен', 'success', 3000)
            setAdditionalText([])

        } else {
            closeAcceptModal()
            addMessage('Не удалось изменить пользователя', 'warning', 3000)
            setAdditionalText([])
        }
    }

    async function deleteUser() {

        const response = await apiDeleteUser(changedUser.id)
        if (response.status == 200) {
            getUsers()
            closeAcceptModal()
            closeChangeModal()
            addMessage('Пользователь изменен', 'success', 3000)

        } else {
            closeAcceptModal()
            addMessage('Не удалось изменить пользователя', 'error', 3000)
        }
    }

    const filteredUsers = users.filter(item => {
        return (
            (filterUsers.login === '' || item.login.includes(filterUsers.login)) &&
            (filterUsers.role === '' || item.role.includes(filterUsers.role)) &&
            (filterUsers.auth_type === '' || item.auth_type.includes(filterUsers.auth_type))
        );
    }
    )

    useEffect(() => {
        getUsers()
    }, [])

    return (
        <div className="usersContainer">
            <div className="usersHeader">
                <button onClick={() => { setPickedUser({ id: 0, login: '', role: '' }); setIsAddModalOpen(true) }}>Добавить пользователя</button>
            </div>
            <Filter onClick={() => setFilterUsers({ login: '', role: '', auth_type: '' })}>
                <input type="text" className="filter" placeholder="Пользователь" onChange={e => setFilterUsers({ ...filterUsers, login: e.target.value })} value={filterUsers.login} />
                <input type="text" className="filter" placeholder="Роль" onChange={e => setFilterUsers({ ...filterUsers, role: e.target.value })} value={filterUsers.role} />
                <input type="text" className="filter" placeholder="Авторизация" onChange={e => setFilterUsers({ ...filterUsers, auth_type: e.target.value })} value={filterUsers.auth_type} />
            </Filter>

            <div className="usersNotes">


                {loading === 'loading' && <Loader />}
                {loading === 'error' && <p> бекенд отвалился</p>}
                {loading === 'loaded' && <>
                    {filteredUsers.map(user =>
                        <UserCard
                            key={user.id}
                            id={user.id}
                            login={user.login}
                            authType={user.auth_type}
                            role={user.role}
                            picked={pickedUser.id === user.id && true || false}
                            onClick={() => { setPickedUser(user); setChangedUser({ id: user.id, login: user.login, role: user.role, password: '', confirmPassword: '' }); setAdditionalText([]); setIsChangeModalOpen(true) }}>
                        </UserCard>
                    )}
                </>}
            </div>

            <Modal isOpen={isAddModalOpen} onClose={() => closeAddModal()}>
                <div className="addModalUsers">

                    <div className="addModalUsersHeader">
                        Добавить пользователя
                    </div>

                    <div className="addModalUsersParams">
                        <div className="addModalUsersParamsValues">
                            <input type="text" className="addModalUsers" placeholder="Имя пользователя" onChange={e => setNewUser({ ...newUser, login: e.target.value })} value={newUser.login} />
                            <select className="addModalUsers" name="" id="" onChange={e => setNewUser({ ...newUser, role: e.target.value })}>
                                <option value="" disabled selected hidden>Роль</option>
                                <option value="admin">admin</option>
                                <option value="user">user</option>
                            </select>
                            <select className="addModalUsers" name="" id="" onChange={e => setNewUser({ ...newUser, auth_type: e.target.value, password: '', confirmPassword: '' })}>
                                <option value="" disabled selected hidden>Авторизация</option>
                                <option value="ldap">LDAP</option>
                                <option value="local">Local</option>
                            </select>
                            <input type="password" disabled={newUser.auth_type !== 'local'} className="addModalUsers" placeholder="Пароль" onChange={e => setNewUser({ ...newUser, password: e.target.value })} value={newUser.password} />
                            <input type="password" disabled={newUser.auth_type !== 'local'} className="addModalUsers" placeholder="Подтвердите пароль" onChange={e => setNewUser({ ...newUser, confirmPassword: e.target.value })} value={newUser.confirmPassword} />
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <button onClick={() => addUser()}>Добавить</button>
                        <button onClick={closeAddModal}> Закрыть</button>
                    </div>
                </div>
            </Modal>

            <Modal isOpen={isChangeModalOpen} onClose={() => closeChangeModal()}>
                <div className="addModalUsers">

                    <div className="addModalUsersHeader">
                        Изменить пользователя
                    </div>

                    <div className="addModalUsersParams">
                        <div className="addModalUsersParamsValues">
                            <input type="text" className="addModalUsers" placeholder="Имя пользователя" onChange={e => setChangedUser({ ...changedUser, login: e.target.value })} value={changedUser.login} />
                            <select className="addModalUsers" name="" id="" onChange={e => setChangedUser({ ...changedUser, role: e.target.value })}>
                                <option value="" disabled={true}>Роль</option>
                                <option value="admin" selected={changedUser.role === 'admin' && true || false}>admin</option>
                                <option value="user" selected={changedUser.role === 'user' && true || false}>user</option>
                            </select>
                            <select className="addModalUsers" disabled={true} name="" id="">
                                <option value="" disabled selected hidden>{pickedUser.auth_type}</option>
                            </select>
                            <input type="password" disabled={pickedUser.auth_type !== 'local'} className="addModalUsers" placeholder="Новый пароль" onChange={e => setChangedUser({ ...changedUser, password: e.target.value })} value={changedUser.password} />
                            <input type="password" disabled={pickedUser.auth_type !== 'local'} className="addModalUsers" placeholder="Подтвердите пароль" onChange={e => setChangedUser({ ...changedUser, confirmPassword: e.target.value })} value={changedUser.confirmPassword} />
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <button onClick={() => { validateChanges() }}>Изменить</button>
                        <button onClick={() => openAcceptModalWithAction(deleteUser)}>Удалить </button>
                        <button onClick={closeChangeModal}> Закрыть </button>
                    </div>
                </div>
            </Modal >

            <AcceptModal isOpen={isAcceptModalOpen} onClose={closeAcceptModal}>
                <div className="acceptModal">
                    <div className="acceptModalText">
                        {additionalText && <>
                            {additionalText.map(note =>
                                <p>{note}</p>
                            )}
                        </>}
                        <p>Вы уверены?</p>
                    </div>
                    <div className="acceptModalButtons">
                        <button className={"positive acceptModal"} onClick={() => { actionFunction(); closeAcceptModal(); }}> Да </button>
                        <button className={"critical acceptModal"} onClick={closeAcceptModal}> Нет </button>
                    </div>
                </div>
            </AcceptModal>
        </div >
    );
}