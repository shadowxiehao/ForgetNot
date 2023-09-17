import * as React from 'react';
import { useNavigate } from 'react-router-dom';

import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import {get,post} from '../utils/requests'
import Home from '../js/Home.js';
import {root} from '../index.js';
import {appName} from './Globals';
import '../css/landing.css';


var publicPath=process.env.PUBLIC_URL;
var logoPath="assets/images/loginBg.jpg";


/* Copyright label */
function Copyright(props) {
	const navigate = useNavigate();
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" onClick={() => navigate('/contact', false)}>
	  {appName}
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}


const theme = createTheme();

function ButtonGroup() {
	
  const navigate = useNavigate();

  /* <--- Load signUP page ---> */
  const loadSignUp = () => {
	  
    navigate('/signup');
  };

  /* <--- Load signIn page ---> */
  const loadSignIn = () => {
    navigate('/signin');
  };
  
  

  return (
    <>
      <Button  onClick={loadSignUp} variant="contained" fullWidth className="buttons">
        Sign Up
      </Button>

     <br/> <Button onClick={loadSignIn} variant="contained" fullWidth className="buttons">
        Log In
      </Button>
    </>
  );
};

export default function Landing() {
  const navigate = useNavigate();

/* Handle eventID button click */
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const ref_id = data.get('ref_id');

    // Proceed if all the fields are entered. Otherwise, display an alert to the user
    if (ref_id.length !== 0) {

     navigate('/guest?ref_id='+ref_id,{ replace: true })


    } else {
      alert("Please enter a reference ID !");
    }
  };

return (
  <ThemeProvider theme={theme} >
    <Grid container component="main" className="main">
      <CssBaseline />
      <Grid item xs={12} sm={4} md={7} 
		className="background-image"
        style={{backgroundImage: `url(${publicPath+logoPath})`,  position: 'relative'}}>
      </Grid>
      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <Box className="main">
         <Box >
          <Typography component="h1" variant="h2" align="center" fontFamily="Baskerville" className="title1">
            Welcome to ForgetNot
          </Typography>

          <Typography component="h2" variant="h5" align="center" fontFamily="Baskerville" className="title2">
            The easy to use online planner
          </Typography>

          <Box  align="center" sx={{ mt: 4, width: 400}}>
            <ButtonGroup  />
			<Box className="guestbox" component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }} align="center">
			 <Grid container spacing={2}>
			  <Grid item xs={14}>
				<TextField
				  name="ref_id"
				  required
				  fontFamily="Baskerville"
				  label="Got a reference ID? Enter here"
				  autoFocus
				  fullWidth
				/>
			  </Grid>
			  <Grid item xs={14}>
				<Button 
				  type="submit"
				  fullWidth
				  variant="contained"
				  sx={{ mt: 3, mb: 2 }}
				>
				  Submit
				</Button>
			  </Grid>
			</Grid>
          </Box>
		  </Box>			
			<Link className="landinglink"  onClick={() => navigate('/contact', false)} >Contact us</Link>
        </Box>
        </Box>
      </Grid>
    </Grid>
  </ThemeProvider>
);
}