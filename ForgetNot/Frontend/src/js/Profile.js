import React, { useState }  from 'react';


import { useNavigate } from 'react-router-dom';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import { Avatar, Button, Container, Grid, TextField, Typography, AppBar, Toolbar } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import IconButton from '@mui/material/IconButton';
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';
import AccessAlarmsOutlinedIcon from '@mui/icons-material/AccessAlarmsOutlined';

import Select,{ SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import ColorPicker from "./ColorPicker"
import parseISO from 'date-fns/parseISO'
import {format} from "date-fns";

import {appName} from './Globals.js';

import {get,post} from '../utils/requests'

import "../css/styles.css";
import {useEffect} from "react";



const theme = createTheme();

const ProfileContainer = styled(Container)({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: theme.spacing(4),
});

const ProfileAvatar = styled(Avatar)({
    width: theme.spacing(12),
    height: theme.spacing(12),
    marginBottom: theme.spacing(2),
});

const ProfileForm = styled('form')({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: theme.spacing(2),
    '& > *': {
        marginBottom: theme.spacing(2),
    },
});


  
const MyProfile = () => {

  const [active, setActive] = useState(false);
  const navigate = useNavigate();
    const [labelsData, setLabelsData] = useState([
							   {  id: 0, name: "Add new" , color:"#51e54f"}]);
    const [selectedLabel, setSelectedLabel] = useState('Add new');
    const [selectedLabelID, setSelectedLabelID] = useState(0);
    const [labelTextVal, setLabelTextVal] = useState('');
    const [color,setColor] = useState("#51e54f");


    useEffect(()=>{
        get('api/label/get/',{})
            .then(function (res){
                setLabelsData([...labelsData, ...res.data])
            })
    },[navigate])


  const [data,setData] = useState({
      "firstName":"",
      "lastName":"",
      "gender":"male",
      "birthday":"",
      "email":""
  })
  const [oldData,setOldData] = useState({
      "firstName":"",
      "lastName":"",
      "gender":"",
      "birthday":"",
      "email":""})

/* After DOM is loaded, hide cancel button */
	useEffect(() => {
        get("/api/user/get/",{})
            .then(function (res){
                let data = res.data
                setData(data)
            })
    }, []);
  
 
 const handleLabelListChange = (event: SelectChangeEvent) => {
    setSelectedLabel(event.target.value);
	setLabelTextVal(event.target.value);

  };
 
 

  const handleCancel = () => {
   // handle cancel button
   // Cancel editing
		if(active===true){
   	      setActive(!active);
		}
        setData(oldData);

  };

  const handleEdit = (event) => {

        setActive(!active);

		  if(active===false){ // Enable edit
                setOldData(data);
				setActive(!active);
		  }else{ // Save edits
              if(data.lastName==="" || data.firstName === "" || data.birthday === "" || data.email === ""){
                  alert("Please fill all fields");
                  handleCancel();
                  return;
              }
              console.log(data)
              post('/api/user/update/',data)
                  .then(function (res){
                      console.log("success");
					  alert("Saved!");
                  })  .catch(function (res){
					  console.log("Error : "+res)
					  alert("Saving failed, please try again !");

				  })
		  }

   
  };

  const handleHomeClick = () => {
    navigate('/home');
  };

  const handleLogoutClick = () => {
	  if (window.confirm('Are you sure you want to logout?')) 
	  {
		  window.history.replaceState(null, null, "/"); //Clear history
		 navigate('/',true);
	  } 
   
  };
  
  /* update changed label value to state variable */
  const updateSelectedLabel = (event) => {
		 
       setLabelTextVal(event.target.value);

  };
  
  /* Label update button click */
  const handleUpdate = (event) => {
	if(selectedLabel!=='Default' && selectedLabel!=='All') // To restrict modifying "Default" & check if not empty
	{
        console.log("labelText",labelTextVal)
        console.log("id",selectedLabelID)
        console.log("color:",color)
        console.log("id===add?",selectedLabelID===0)
		if(labelTextVal.length!==0)
		{
			if(selectedLabelID===0 ) //Add new
			{
				const param = {name:labelTextVal,color:color}
				post("/api/label/create/",param)
					.then(function (res){
						setLabelsData([...labelsData, res.data ])
						const data = res.data
						setSelectedLabel(data.name)
						setLabelTextVal(data.name)
						setSelectedLabelID(data.id)
						setColor(data.color)
					})
			}else { // Update existing label
				const param = {label_id:selectedLabelID,name:labelTextVal,color:color}
				post("/api/label/update/",param)
					.then(function (res){
						const data = labelsData.map(value => (
							value.id === res.data.id ? res.data : value
						))
						setSelectedLabel(res.data.name)
						setLabelsData(data)
						alert("Label updated!");

					})
			}
		}else	{
		alert("Please enter a label name!");
    }
	}else	
		alert("You cannot modify this label!");
    };
  
   
  const handleDelete = (e) => {
	  
	  if(selectedLabelID>1 && selectedLabel!=='Default' && selectedLabel!=='All') // To restrict deleting "Add new" and "Default"
	  {

		  if (window.confirm('Deleting a label will delete related events also.  Are you sure you want to delete this label?')) {
              const param ={label_id:selectedLabelID}
              post("/api/label/delete/",param)
                  .then(function (res){
                      let data = []
                      labelsData.forEach(value => {
                          if(value.id !== selectedLabelID){
                              data.push(value)
                          }
                      })
                      setLabelsData(data);
                      setSelectedLabel("Add new")
                      setLabelTextVal("")
                      setSelectedLabelID(0)
                      setColor("#51e54f")
                      alert("Label and events deleted!");
                  })
          }
	  }else alert("You cannot delete this label");

  };
  

  const textOnchange = (event) =>{
      const name = event.target.name;
      const value = event.target.value;
      setData({...data,[name] : value})
  }

  return (
    <ThemeProvider theme={theme}>
 <AppBar position="static">
  <Toolbar>
		<IconButton  color="inherit">
                <AccessAlarmsOutlinedIcon fontSize="large"/>
        </IconButton>
			
		<Typography
              component="h1"
			  fontFamily="Arial"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}>
            {appName}
        </Typography>
		
		<IconButton  color="inherit" onClick={handleHomeClick}>
            <HomeIcon fontSize="large"/>
        </IconButton>
			
		<IconButton color="inherit" onClick={handleLogoutClick}>
           <LogoutOutlinedIcon fontSize="large"/>
        </IconButton>
			
  </Toolbar>
</AppBar>
      <ProfileContainer maxWidth="sm" sx={{ textAlign: 'center' }}>
		
		{/* <ProfileAvatar src="/path/to/user/photo.jpg" alt="User's profile photo" />*/}
		<AccountCircleOutlinedIcon fontSize="large"/>
        <Typography variant="h4" gutterBottom fontFamily="Baskerville" sx={{ fontWeight: 600, mb: 2, fontSize: '2rem', color: 'cobalt'}}>
          My Profile
        </Typography>
		
        <ProfileForm onSubmit={handleEdit}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth id="firstName" label="Firstname" name="firstName" value={data.firstName} onChange={textOnchange} disabled={!active}/>
			
            </Grid>
			 <Grid item xs={12} sm={6}>
              <TextField fullWidth id="lastName" label="Lastname" name="lastName" value={data.lastName} onChange={textOnchange} disabled={!active}/>
			
            </Grid>
           
            <Grid item xs={12} sm={6}>
				<Select required fullWidth defaultValue='male' value={data.gender} name="gender" onChange={textOnchange} label="gender" disabled={!active}>
					  <MenuItem value='male' >Male</MenuItem>
					  <MenuItem value='female' >Female</MenuItem>
				</Select>
            </Grid>
          <Grid item xs={12} sm={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <DatePicker
                      id="birthday"
                      label="birthday"
					  maxDate={new Date()}
                      value={parseISO(data.birthday)}
                      onChange={(newValue) => setData({...data,birthday: format(newValue,"yyyy-MM-dd")})}
                      disabled={!active}
                   renderInput={(params) => <TextField {...params} />}/>
              </LocalizationProvider>
          </Grid>
          </Grid>
		   <Grid item xs={12} sm={6}>
              <TextField fullWidth id="email" label="Email" name="email" value={data.email} onChange={textOnchange} disabled={!active}/>
              
            </Grid>
			<br/>
         <div>
		 
 		 <Button id="edit" variant="contained" color="primary" fullWidth onClick={handleEdit} >
   		  { active ? "Save" : "Edit"}
 		 </Button>
             <Button id="cancel" variant="outlined" color="secondary" onClick={handleCancel} fullWidth style={{ borderColor: 'red', color: 'red', marginTop: '16px', display: active?'block':'none' }} >
  	 	 Cancel
  		</Button>

		</div>
	
		<div>
		-------------------------------------------------------------------------------------
			 <Typography variant="h6" gutterBottom fontFamily="Baskerville" sx={{ fontWeight: 400, mb: 2, fontSize: '2rem', color: 'cobalt'}}>
				Labels
			</Typography>
			
			   <Select sx={{ m: 1, width: 300 }}
				value={selectedLabel}
				onChange={handleLabelListChange}
               >
					{labelsData.map((label) => (
						<MenuItem
						key={label.id}
						value={label.name}
                        onClick={() => {setSelectedLabelID(label.id);setColor(label.color)}}
						>
                            {label.name}
						</MenuItem>
					))}
			  </Select> 
			<TextField sx={{ m: 1, width: 300 }} id="labelUpdate" value={labelTextVal} onChange={updateSelectedLabel} variant="outlined" />
			 <br/>
                <ColorPicker color={color} onColorChange={(newColor)=>{setColor(newColor);console.log(color)}} />
            <br/>
            <Button sx={{ m: 1, width: 150 }} variant="contained" color="primary" onClick={handleUpdate} >
				Update
			</Button>
			 <Button sx={{ m: 1, width: 150 }} variant="contained" color="primary" onClick={handleDelete} >
				Delete
			</Button>
			<br/>
		</div>
	
		<br/>
        </ProfileForm>
		
      </ProfileContainer>
    </ThemeProvider>
  );


}
export default MyProfile;

