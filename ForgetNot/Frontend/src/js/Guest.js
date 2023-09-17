import React, { useState }  from 'react';


import {useLocation, useNavigate} from 'react-router-dom';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import { Avatar, Button, Container, Grid, TextField, Typography, AppBar, Toolbar } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import IconButton from '@mui/material/IconButton';
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';
import AccessAlarmsOutlinedIcon from '@mui/icons-material/AccessAlarmsOutlined';
import Box from '@mui/material/Box';

import Select,{ SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import parseISO from 'date-fns/parseISO'
import {format} from "date-fns";

import {appName} from './Globals.js';

import {get,post} from '../utils/requests'

import "../css/styles.css";
import {useEffect} from "react";

var publicPath=process.env.PUBLIC_URL;
var logoPath= 'assets/images/guestBg.jpg';



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


  
const Guest = (props) => {
    const location = useLocation();
    const ref_id = new URLSearchParams(location.search).get("ref_id");
  const [active, setActive] = useState(false);
  const navigate = useNavigate();
  const [labelsData, setlabelsData] = useState([
							   {  id: 0, value: "Add new" },
								{ id: 1, value: "Study" },
								{ id: 2, value: "Meetings" }
  ]);
    const [selectedLabel, setSelectedLabel] = useState('Add new');
    const [selectedLabelID, setSelectedLabelID] = useState('0');
    const [changePage,setChangePage] = useState(false);

  const [data,setData] = useState({
      "firstName":"",
      "lastName":"",
      "notes":"",
      "startDate":"",
      "endDate":"",
      "title":"",
      "status":"0",
  })

/* After DOM is loaded, hide cancel button */
	useEffect(() => {
        const param = {ref_id:ref_id}
        get("/api/event/get/",param)
            .then(function (res){
                const data = res.data
                let newData = {}
                console.log(data)
                newData['firstName'] = data.user.firstName
                newData['lastName'] = data.user.lastName
                newData['startDate'] = data.ref.event.startDate
                newData['endDate'] = data.ref.event.endDate
                newData['title'] = data.ref.event.title
                newData['notes'] = data.ref.event.notes
                newData['status'] = data.ref.status
                console.log(newData)
                setData(newData)
            })
    }, [changePage]);
  

  
  const handleHomeClick = () => {
	window.history.replaceState(null, null, "/"); //Clear history
    navigate('/');
  };

  const handleConfirmClick = () => {
      const param = {ref_id:ref_id}
      get('/api/invite/accept/',param).then(function (res){setChangePage(!changePage)})
  };
  const handleCancelClick = () => {
      const param = {ref_id:ref_id}
      get('/api/invite/reject/',param).then(function (res){setChangePage(!changePage)})
  };
 
  
  
  

  const textOnchange = (event) =>{
      console.log(event)
      const name = event.target.name;
      const value = event.target.value;
      setData({...data,[name] : value})
  }

  const AfterChoose = () =>{
      if(data.status === 1){
          return (
              <Grid item xs={12} sm={6}>
                  <Typography variant="body1" sx={{ color: "green" }}>
                      You have confirmed it.
                  </Typography>
              </Grid>
          )
      }else{
          return (
              <Grid item xs={12} sm={6}>
                  <Typography variant="body1" sx={{ color: "red" }}>
                      You have rejected it.
                  </Typography>
              </Grid>
          )
      }
  }

  return (
    <ThemeProvider theme={theme}>
	  <Box
          component="main"
          sx={{
            /*backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',*/
			backgroundImage: `url(${publicPath+logoPath})`,
			backgroundRepeat: 'no-repeat',
			backgroundPosition: 'center',
			backgroundSize: 'cover',
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
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
			
			{/*<IconButton color="inherit" onClick={handleLogoutClick}>
			<LogoutOutlinedIcon fontSize="large"/>
        </IconButton>*/}
			
  </Toolbar>
</AppBar>
      <ProfileContainer maxWidth="sm" sx={{ textAlign: 'center', backgroundColor: 'white', opacity: '1' }}>
		
		{/* <ProfileAvatar src="/path/to/user/photo.jpg" alt="User's profile photo" />*/}
		<AccountCircleOutlinedIcon fontSize="large"/>
        <Typography variant="h4" gutterBottom fontFamily="Baskerville" sx={{ fontWeight: 600, mb: 2, fontSize: '2rem', color: 'cobalt'}}>
          Event details
        </Typography>
		
        <ProfileForm >
          <Grid container spacing={2}>
		   <Grid item xs={12} sm={12}>
			<TextField fullWidth id="host" label="Hosted by" name="host" value={data.firstName+" " +data.lastName} 
			onChange={textOnchange} InputProps={{readOnly: true}}
            />
			
            </Grid>
            <Grid item xs={12} sm={12}>
			<TextField id="title" label="Title" name="firstName" value={data.title}
                       onChange={textOnchange} InputProps={{readOnly: true}} fullWidth
		/>
			
            </Grid>
			
			 <br/><Grid item xs={12} sm={6}>
              <TextField fullWidth id="startDate" label="Start Date" name="lastName" value={data.startDate} onChange={textOnchange}
			  InputProps={{readOnly: true}} />
			
            </Grid>
			<Grid item xs={12} sm={6}>
              <TextField fullWidth id="endDate" label="End Date" name="lastName" value={data.endDate} onChange={textOnchange}
			  InputProps={{readOnly: true}} />
			
            </Grid>
           
          
         
          </Grid>
		   <Grid item xs={12} sm={6}>
              <TextField fullWidth id="info" label="More Information" name="email" value={data.notes}
			  onChange={textOnchange} InputProps={{readOnly: true}} 
			  sx={{width: { sm: 200, md: 550 }, "& .MuiInputBase-root": {height: 150}}} multiline = {true} />
              
            </Grid>
			<br/>
            {data.status === 0?
                (
                    <Grid item xs={12} sm={6}>
                        <Button id="edit" variant="contained" color="primary" onClick={handleConfirmClick} >
                            CONFIRM
                        </Button>
                        <Button id="edit" sx={{ m: 2 }} variant="contained" color="primary" onClick={handleCancelClick} >
                            REJECT
                        </Button>
                    </Grid>
                ):
                (
                    <AfterChoose/>
                )
            }
         <div>
		 
 		
		</div>
	
		
	
		<br/>
        </ProfileForm>
		
      </ProfileContainer>
	  </Box>
    </ThemeProvider>
  );


}
export default Guest;

