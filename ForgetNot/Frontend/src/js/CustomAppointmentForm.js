import { useState, useEffect } from 'react';
import { CircularProgress } from '@mui/material';
import { AppointmentForm } from '@devexpress/dx-react-scheduler-material-ui';
import Button from "@mui/material/Button";
import * as React from "react";
import {Delete} from "@mui/icons-material";
import {IconButton} from "@mui/material";
import {Refresh} from "@mui/icons-material";
import {get,post} from "../utils/requests"



function CustomAppointmentForm({event_id,signal}) {
    const [loading, setLoading] = useState(true);
    const [invitedata,setInviteData] = useState({});

    useEffect(() => {
        handleSetInviteData()
    }, []);

    useEffect(()=>{
        if(signal){
            handleSetInviteData()
            signal = !signal
        }
    },[signal])

    const handleSetInviteData = () =>{
        setLoading(true)
        const param = {event_id:event_id}
        get("/api/event/invite_list",param)
            .then(function (res){
                console.log(res.data)
                const data = res.data
                let newData = []
                data.forEach(value=>{
                    if(value.status === 0){
                        value.status = "pending"
                    }
                    if(value.status === 1){
                        value.status = "accept"
                    }
                    if(value.status === 2){
                        value.status = "Rejection"
                    }
                    if(value.user.firstName !== "" || value.user.lastName !== ""){
                        value.name = value.user.firstName + " " + value.user.lastName
                    }else{
                        value.name = value.user.email
                    }
                    newData.push(value)
                })
                setInviteData(newData)
                setLoading(false)
            })
    }

    const handleRefresh = () =>{
        handleSetInviteData()
    }

    if(loading){
        return <CircularProgress style={{padding: '8px' }}></CircularProgress>
    }else


    return (
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
            <thead>
            <tr style={{ borderBottom: '1px solid #E5E5E5' }}>
                <th style={{ textAlign: 'left', padding: '8px', fontWeight: 'normal' }}>Name/Email</th>
                <th style={{ textAlign: 'center', padding: '8px', fontWeight: 'normal' }}>Status</th>
                <th style={{ textAlign: 'right', padding: '8px', fontWeight: 'normal' }}>Operation</th>
                <IconButton onClick={handleRefresh} >
                    <Refresh />
                </IconButton>
            </tr>
            </thead>
            <tbody>
            {
                invitedata.map((value)=>{
                    return (
                    <tr style={{ borderBottom: '1px solid #E5E5E5' }}>
                        <td style={{ padding: '8px' }}>{value.name}</td>
                        <td style={{ textAlign: 'center',padding: '8px' }}>{value.status}</td>
                        <td style={{ textAlign: 'right', padding: '8px' }}>
                            <button>
                                <Delete />
                            </button>
                        </td>
                    </tr>)
                })
            }
            </tbody>
        </table>
    );
}

export default CustomAppointmentForm;