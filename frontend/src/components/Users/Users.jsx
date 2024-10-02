import React, { Component } from "react";
import { useState, useEffect } from "react";
import "./Users.css";
import UserCard from "./UserCard/UserCard";
import Button from "../Button/Button";
import { apiGetUsers, apiAddUser, apiChangeUser, apiDeleteUser } from "../../services/apiUsers";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import Modal from "../Modal/Modal";
import AcceptModal from "../AcceptModal/AcceptModal";
import filterLogo from './filter.png'

export default function Users() {
    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();

    const [users, setUsers] = useState([])
    const [loading, setLoading] = useState('loading')
    const [pickedUser, setPickedUser] = useState({id: '', login: '', role: ''})
    const [newUser, setNewUser] = useState({login: '', auth_type: '', role: '', password: '', confirmPassword: ''})
    const [changedUser, setChangedUser] = useState({id:'', login: '', auth_type: '', role: '', password: '', confirmPassword: ''})
    
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isChangeModalOpen, setIsChangeModalOpen] = useState(false);
    const [isAcceptModalOpen, setIsAcceptModalOpen] = useState(false);

    const [actionFunction, setActionFunction] = useState(null);
    const [filterUsers, setFilterUsers] = useState({ login: '', role: '', auth_type: '' });

    const openAcceptModalWithAction = (action) => {
        setActionFunction(() => action);
        setIsAcceptModalOpen(true);
      };

    function closeAddModal(){
        setIsAddModalOpen(false);
        setNewUser({id:'', login: '', auth_type: '', role: '', password: '', confirmPassword: ''})
    } 

    function closeChangeModal(){
        setIsChangeModalOpen(false);
        setChangedUser({id:'', login: '', auth_type: '', role: '', password: '', confirmPassword: ''})
    } 

    function closeAcceptModal(){
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

    async function addUser(){
        if (!newUser.login) {
            setNotificationData({message:'Введите имя пользователя', type: 'error'})
            toggleNotificationFunc()
            return false
        }

        if (!newUser.role) {
            setNotificationData({message:'Выберете роль пользователя', type: 'error'})
            toggleNotificationFunc()
            return false
        }

        if (!newUser.auth_type) {
            setNotificationData({message:'Выберете тип авторизации пользователя', type: 'error'})
            toggleNotificationFunc()
            return false
        }
        
        if (!newUser.password && newUser.auth_type === 'local') {
            setNotificationData({message:'Введите пароль', type: 'error'})
            toggleNotificationFunc()
            return false
        }

        if (newUser.password != newUser.confirmPassword) {
            setNotificationData({message:'Пароли не совпадают', type: 'error'})
            toggleNotificationFunc()
            return false
        }

        
        const response = await apiAddUser(newUser.login, newUser.role, newUser.auth_type, newUser.password)
        if (response.status == 200) {
            getUsers()
            closeAddModal()
            setNotificationData({message:'Пользователь добавлен', type: 'success'})
            toggleNotificationFunc()

        } else {
            setNotificationData({message:'Не удалось добавить пользователя', type: 'error'})
            toggleNotificationFunc()
        }
    }

    async function changeUser(){

        if (changedUser.password != changedUser.confirmPassword) {
            setNotificationData({message:'Пароли не совпадают', type: 'error'})
            toggleNotificationFunc()
            closeAcceptModal()
            return false
        }

        const response = await apiChangeUser(changedUser.id, changedUser.login, changedUser.role, changedUser.auth_type, changedUser.password)
        if (response.status == 200) {
            getUsers()
            closeAcceptModal()
            closeChangeModal()
            setNotificationData({message:'Пользователь изменен', type: 'success'})
            toggleNotificationFunc()

        } else {
            closeAcceptModal()
            setNotificationData({message:'Не удалось изменить пользователя', type: 'error'})
            toggleNotificationFunc()
        }
    }

    async function deleteUser(){

        const response = await apiDeleteUser(changedUser.id)
        if (response.status == 200) {
            getUsers()
            closeAcceptModal()
            closeChangeModal()
            setNotificationData({message:'Пользователь изменен', type: 'success'})
            toggleNotificationFunc()

        } else {
            closeAcceptModal()
            setNotificationData({message:'Не удалось изменить пользователя', type: 'error'})
            toggleNotificationFunc()
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
        <div className="users">        
                <div className="usersHeader">
                    <Button 
                        style={'createUser'}
                        onClick={() => {setPickedUser({id: 0, login: '', role: ''}); setIsAddModalOpen(true)}}>Добавить пользователя
                    </Button>
                </div>  

                <div className="usersFilterContainer">
                    <img src={filterLogo} alt="" className="filterLogo"/>
                    <input type="text" className="usersFilter" placeholder="Пользователь" onChange={e => setFilterUsers({...filterUsers, login: e.target.value})} value={filterUsers.login}/>
                    <input type="text" className="usersFilter" placeholder="Роль" onChange={e => setFilterUsers({...filterUsers, role: e.target.value})} value={filterUsers.role}/>
                    <input type="text" className="usersFilter" placeholder="Авторизация" onChange={e => setFilterUsers({...filterUsers, auth_type: e.target.value})} value={filterUsers.auth_type}/>
                    <button onClick={() => setFilterUsers({ login: '', role: '', auth_type: '' })} className="clearFilter">Очистить</button>
                </div>

                {loading === 'loading' && <p> Loading ...</p>}
                {loading === 'error' && <p> бекенд отвалился</p>}
                {loading === 'loaded' && <>
                    {filteredUsers.map(user => 
                        <UserCard
                            id={user.id}
                            login={user.login}
                            authType={user.auth_type}
                            role={user.role}
                            picked={pickedUser.id === user.id && true || false}
                            onClick={() => {setPickedUser(user); setChangedUser({id:user.id, login: user.login, auth_type: user.auth_type, role: user.role, password: '', confirmPassword: ''}); setIsChangeModalOpen(true)}}>
                        </UserCard>  
                    )}
                </>}

                <Modal isOpen={isAddModalOpen} onClose={() => closeAddModal()}> 
                <div className="addModalUsers">

                    <div className="addModalUsersHeader">
                        Добавить пользователя
                    </div>
                     
                    <div className="addModalUsersParams">
                        <div className="addModalUsersParamsValues">
                            <input type="text" className="addModalUsers" placeholder="Имя пользователя" onChange={e => setNewUser({...newUser, login: e.target.value})} value={newUser.login}/>
                            <select className="addModalUsers" name="" id="" onChange={e => setNewUser({...newUser, role: e.target.value})}>
                                <option value="" disabled selected hidden>Роль</option>
                                <option value="admin">admin</option>
                                <option value="user">user</option>
                            </select>
                            <select className="addModalUsers" name="" id="" onChange={e => setNewUser({...newUser, auth_type: e.target.value, password: '', confirmPassword: ''})}>
                                <option value="" disabled selected hidden>Авторизация</option>
                                <option value="ldap">LDAP</option>
                                <option value="local">Local</option>
                            </select>
                            <input type="password" disabled={newUser.auth_type !== 'local'} className="addModalUsers" placeholder="Пароль" onChange={e => setNewUser({...newUser, password: e.target.value})} value={newUser.password}/>
                            <input type="password" disabled={newUser.auth_type !== 'local'} className="addModalUsers" placeholder="Подтвердите пароль" onChange={e => setNewUser({...newUser, confirmPassword: e.target.value})} value={newUser.confirmPassword}/>
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <Button style={"projectAccept"} onClick={() => addUser()}> Добавить </Button>
                        <Button style={"projectClose"} onClick={closeAddModal}> Закрыть </Button>
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
                            <input type="text" className="addModalUsers" placeholder="Имя пользователя" onChange={e => setChangedUser({...changedUser, login: e.target.value})} value={changedUser.login}/>
                            <select className="addModalUsers" name="" id="" onChange={e => setChangedUser({...changedUser, role: e.target.value})}>
                                <option value="" disabled selected hidden>Роль</option>
                                <option value="admin">admin</option>
                                <option value="user">user</option>
                            </select>
                            <select className="addModalUsers" disabled={true}name="" id="">
                                <option value="" disabled selected hidden>{changedUser.auth_type}</option>
                            </select>
                            <input type="password" disabled={changedUser.auth_type !== 'local'} className="addModalUsers" placeholder="Новый пароль" onChange={e => setChangedUser({...changedUser, password: e.target.value})} value={changedUser.password}/>
                            <input type="password" disabled={changedUser.auth_type !== 'local'} className="addModalUsers" placeholder="Подтвердите пароль" onChange={e => setChangedUser({...changedUser, confirmPassword: e.target.value})} value={changedUser.confirmPassword}/>
                        </div>
                    </div>

                    <div className="addModalUsersButtons">
                        <Button style={"projectAccept"} onClick={() => openAcceptModalWithAction(changeUser)}> Изменить </Button>
                        <Button style={"projectReject"} onClick={() => openAcceptModalWithAction(deleteUser)}> Удалить </Button>
                        <Button style={"projectClose"} onClick={closeChangeModal}> Закрыть </Button>
                    </div>
                </div>
            </Modal>

            <AcceptModal isOpen={isAcceptModalOpen} onClose={closeAcceptModal}>
                <div className="acceptModalProjects">
                    <div className="acceptModalProjectsText">
                        Вы уверены?
                    </div>
                    <div className="acceptModalProjectsButtons">
                        <Button style={"projectAccept"} onClick={() => { actionFunction(); closeAcceptModal(); }}> Да </Button>
                        <Button style={"projectReject"} onClick={closeAcceptModal}> Нет </Button>
                    </div>
                </div>
            </AcceptModal>
      </div>
    );
}