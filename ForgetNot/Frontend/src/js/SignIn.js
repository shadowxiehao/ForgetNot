import * as React from 'react';
import { useNavigate } from 'react-router-dom';

import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';

import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import {post} from '../utils/requests'



import {appName} from '../js/Globals.js';
import './../css/signin.css';




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

export default function SignInSide() {
  const navigate = useNavigate();
  
  

/* Handle SignIn button click */
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const userEmail = data.get('email');
    const userPassword = data.get('password');
	
    	
      const requests_data = {
          'email':userEmail,
          'password':userPassword
      }
	  
	  // If the userEmail and userPassword field are not empty, call webservice. Otherwise display an alert to the user
	  if(userEmail.length!==0 && userPassword.length!==0)
	  {
		   post('api/user/login/', requests_data)
          .then(function (res){
			  
			  // If the response code is 200 -> sign in successful, proceed to home page. Otherwise display relevant alert to the user
              if(res.status === 200){
				 
                  navigate("/home",{ replace: true })
              }else if(res.status === 401){
				  alert("User cannot be found, Please register and try again!");
			  }else
				  alert("SignIn failed,Please try again!");
          })
          .catch(function (res){
              console.log(res);
				  alert("User cannot be found, Please register and try again!");
			  
          }) 
		  
	  }else
		  alert("Please enter the registered Email address and password!");
	  
    
  };

return (
  <ThemeProvider theme={theme}>
    <Grid container component="main" sx={{ height: '100vh' }}>
      <CssBaseline />
      <Grid item xs={12} sm={4} md={7} 
	className="background-image"
        style={{backgroundImage: `url(${publicPath+logoPath})`,  position: 'relative'}}>
      </Grid>
      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <Box className="box">
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
            </Grid>
            <Box sx={{ mt: 5 }}>
                     <Copyright sx={{ mt: 5 }} />

            </Box>
          </Box>
        </Box>
      </Grid>
    </Grid>
  </ThemeProvider>
);
}